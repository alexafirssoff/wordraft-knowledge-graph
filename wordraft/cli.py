"""Проверяемая навигация и контролируемое пополнение Wordraft vault.

Не реализует LLM-редактор и не выдаёт результаты LLM за формальные выводы.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml

class StrictLoader(yaml.SafeLoader):
    """Внешняя YAML-карточка с повторным ключом не может молча изменить смысл."""

def _strict_mapping(loader, node):
    loader.flatten_mapping(node)
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=True)
        if key in result:
            raise yaml.constructor.ConstructorError(None, None, f'Повтор ключа YAML: {key}', key_node.start_mark)
        result[key] = loader.construct_object(value_node, deep=True)
    return result

StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _strict_mapping)

LINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
TYPES = {"canonical_assertion", "support_edge", "assertion_instance", "source_fragment",
         "source_revision", "source_document", "example", "external_practice",
         "external_resource", "evaluation_case", "editorial_procedure",
         "editorial_decision", "task_route"}
ROUTE_ALIASES = {"edit":"general_edit", "review":"general_edit", "article":"article",
                 "post":"post", "promo":"promo", "ux_copy":"ux_copy",
                 "docs":"technical_docs", "policy":"knowledge_update",
                 "research":"research", "write":"general_writing", "full_review":"full_policy_audit"}

def load_note(path: Path) -> tuple[dict[str, Any], str]:
    body = path.read_text(encoding="utf-8")
    if not body.startswith('---\n'):
        return {}, body
    pieces = body.split('---\n', 2)
    if len(pieces)<3:
        raise ValueError(f'Незакрытый YAML frontmatter: {path}')
    data = yaml.load(pieces[1], Loader=StrictLoader)
    if not isinstance(data, dict):
        raise ValueError(f'Некорректный YAML словарь: {path}')
    return data, pieces[2]

class Graph:
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.records:dict[str,dict[str,Any]] = {}
        self.files:dict[str,Path] = {}
        self.by_stem:dict[str,Path] = {}
        self.errors:list[str] = []
        self.all_notes:dict[Path,str]={}
        for directory in sorted(self.root.iterdir()):
            if directory.is_dir() and re.match(r'^\d\d ',directory.name):
                for path in sorted(directory.rglob('*.md')):
                    self._add(path)
        # Top-level entrypoints are not graph nodes but may contain wikilinks.
        for path in sorted(self.root.glob('*.md')):
            self.by_stem[path.stem]=path
            self.all_notes[path]=path.read_text(encoding='utf-8')
        for path,content in self.all_notes.items():
            for link in LINK.findall(content):
                target = link.split('/')[-1]
                if target not in self.by_stem:
                    self.errors.append(f'Нет wikilink: {path.relative_to(self.root)} → {link}')

    def _add(self,path:Path):
        try:
            content=path.read_text(encoding='utf-8')
            d,_=load_note(path)
        except (ValueError,yaml.YAMLError,UnicodeDecodeError) as e:
            self.errors.append(str(e));return
        self.all_notes[path]=content
        self.by_stem[path.stem]=path
        ident=str(d.get('id',''))
        if not ident:
            # Брифы и пользовательские заметки могут не быть узлами графа.
            return
        if ident in self.records:
            self.errors.append(f'Повтор id {ident}: {path} / {self.files[ident]}');return
        if d.get('record_type') not in TYPES:
            self.errors.append(f'Недопустимый record_type {d.get("record_type")}: {ident}')
        self.records[ident]=d;self.files[ident]=path

    def validate(self)->list[str]:
        errors=list(self.errors)
        for ident,rec in self.records.items():
            if rec.get('record_type') == 'canonical_assertion' and rec.get('current_status') == 'active':
                supp=rec.get('supported_by_records',[])
                if not supp:
                    errors.append(f'Активное правило {ident} без supported_by_records')
                    continue
                active=False
                for value in supp:
                    m=LINK.search(str(value))
                    if not m:continue
                    target=self.by_stem.get(m.group(1).split('/')[-1])
                    if target:
                        sid=load_note(target)[0].get('id')
                        edge=self.records.get(str(sid),{})
                        if edge.get('record_type')=='support_edge' and edge.get('is_active') is True:
                            instance=self.resolve(str(edge.get('instance','')))
                            if instance:
                                inrec=instance[1]
                                revision=self.resolve(str(inrec.get('source_version','')))
                                fragment=self.resolve(str(inrec.get('fragment','')))
                                if (inrec.get('current_status')=='active' and revision and
                                    revision[1].get('is_active') is True and fragment):
                                    active=True
                if not active:errors.append(f'Активное правило {ident} без активного основания')
        return errors

    def resolve(self, s:str)->tuple[str,dict[str,Any]]|None:
        m=LINK.search(str(s))
        if not m:return None
        target=self.by_stem.get(m.group(1).split('/')[-1])
        if not target:return None
        data,_=load_note(target)
        return str(data.get('id','')),data

    def trace(self, ident: str, max_depth:int=6)->list[dict[str,Any]]:
        if ident not in self.records:raise KeyError(ident)
        queue=[(ident,0)];seen=set();out=[]
        while queue and len(out)<55:
            rid,depth=queue.pop(0)
            if rid in seen:continue
            seen.add(rid)
            rec=self.records[rid]
            out.append({'id':rid,'record_type':rec.get('record_type'),
                'current_status':rec.get('current_status'),
                'file':str(self.files[rid].relative_to(self.root))})
            if depth>=max_depth:continue
            # Только явно записанные отношения, никакой семантики из сходства названий.
            keys=('supported_by_records','instance','source_version','source_document',
                  'fragment','assertion','illustrated_by','complements')
            for key in keys:
                refs=rec.get(key,[])
                if not isinstance(refs,list):refs=[refs]
                for ref in refs:
                    resolved=self.resolve(str(ref))
                    if resolved and resolved[0] not in seen:
                        queue.append((resolved[0],depth+1))
        return out

def cmd_validate(args):
    graph=Graph(args.vault)
    errors=graph.validate()
    if errors:
        for e in errors:print('ОШИБКА:',e,file=sys.stderr)
        print(f'НЕ ПРОШЛО: {len(graph.records)} записей, {len(errors)} ошибок.',file=sys.stderr)
        return 1
    counts=Counter(r.get('record_type') for r in graph.records.values())
    print(f'ПРОЙДЕНО: {len(graph.records)} записей. ID уникальны, ссылки разрешаются, активные основания проверены.')
    print('Типы:',', '.join(f'{k}={v}' for k,v in sorted(counts.items())))
    return 0

def cmd_route(args):
    graph=Graph(args.vault)
    task=ROUTE_ALIASES.get(args.task,args.task)
    options=[(ident, rec) for ident,rec in graph.records.items()
             if rec.get('record_type')=='task_route' and rec.get('task_type')==task]
    if not options:
        print(f'Маршрут {args.task!r} не найден. Доступны: '+', '.join(sorted(set(str(r.get('task_type')) for r in graph.records.values() if r.get('record_type')=='task_route'))),file=sys.stderr)
        return 2
    rid,route=options[0]
    out={'route':rid,'name':route.get('title'), 'task_type':task,
         'steps':[graph.resolve(str(x))[0] for x in route.get('sequence',[]) if graph.resolve(str(x))],
         'optional':[graph.resolve(str(x))[0] for x in route.get('optional',[]) if graph.resolve(str(x))],
         'notice':'K/R — рекомендации и справочники; A — только активные и применимые нормы. Сверяйте scope.'}
    print(json.dumps(out,ensure_ascii=False,indent=2))
    return 0

def cmd_explain(args):
    graph=Graph(args.vault)
    try: out=graph.trace(args.id,max_depth=args.depth)
    except KeyError:
        print(f'Неизвестный ID: {args.id}',file=sys.stderr);return 2
    print(json.dumps({'id':args.id,'support_trail':out},ensure_ascii=False,indent=2))
    return 0

def proposal_validate(d:Any)->list[str]:
    e=[]
    if not isinstance(d,dict):return ['Нужно JSON-описание объекта']
    if set(d.keys())!={'source','assertion'}:e.append('Ожидаются ровно два поля: source, assertion')
    source=d.get('source',{});a=d.get('assertion',{})
    if not isinstance(source,dict) or not isinstance(a,dict):return e+['source и assertion должны быть объектами']
    for key in ('title','url','revision','excerpt','license_note'):
        if not isinstance(source.get(key),str) or not source.get(key).strip():e.append('source.'+key+' должно быть непустой строкой')
    for key in ('statement','scope','kind'):
        if not isinstance(a.get(key),str) or not a.get(key).strip():e.append('assertion.'+key+' должно быть непустой строкой')
    if a.get('kind') not in ('obligation','prohibition','preference','permission','security_requirement'):
        e.append('Недопустимый assertion.kind')
    if isinstance(source.get('url'),str):
        u=urlparse(source['url'])
        if u.scheme not in ('https','http') or not u.netloc or u.username or u.password:
            e.append('source.url: нужен внешний HTTP(S) URL без credentials')
    for key in ('excerpt',):
        if isinstance(source.get(key),str) and len(source[key])>12000:e.append('Слишком длинная выписка из источника')
    for key in ('statement','scope'):
        if isinstance(a.get(key),str) and len(a[key])>2000:e.append('Слишком длинное поле '+key)
    return e

def cmd_propose(args):
    try: data=json.loads(Path(args.file).read_text(encoding='utf-8'))
    except (ValueError,OSError) as ex:
        print('Не удалось прочитать JSON:',ex,file=sys.stderr);return 2
    errors=proposal_validate(data)
    if errors:
        for err in errors:print('ОШИБКА:',err,file=sys.stderr)
        return 2
    canonical=json.dumps(data,sort_keys=True,ensure_ascii=False)
    pid=hashlib.sha256(canonical.encode('utf-8')).hexdigest()[:16]
    dst=args.vault/'proposals'/'pending'/f'{pid}.json'
    dst.parent.mkdir(parents=True,exist_ok=True)
    if dst.exists():
        print(f'Предложение уже существует: {dst}');return 0
    with dst.open('x',encoding='utf-8') as f:json.dump(data,f,ensure_ascii=False,indent=2)
    print(f'ПРЕДЛОЖЕНО: {pid}; исходный текст и выписка НЕ стали инструкциями; статус — ожидание владельца.')
    return 0

def fenced(content:str)->str:
    # Нельзя позволять извлечению включать неожиданную структуру заметки.
    return content.replace('```','` ` `').replace('\x00','')

def note(data:dict,body:str)->str:
    return '---\n'+yaml.safe_dump(data,allow_unicode=True,sort_keys=False,width=100)+'---\n\n'+body.strip()+'\n'

def next_id(graph:Graph,prefix:str)->str:
    nums=[int(x[len(prefix):]) for x in graph.records if re.fullmatch(re.escape(prefix)+r'\d+',x)]
    return prefix+f'{max(nums,default=0)+1:02d}'

def cmd_apply(args):
    if args.confirm != 'ОДОБРЯЮ':
        print('Требуется явно указать --confirm ОДОБРЯЮ.',file=sys.stderr);return 2
    if not re.fullmatch(r'[a-f0-9]{16}',args.proposal):
        print('Некорректный ID предложения',file=sys.stderr);return 2
    base=args.vault.resolve();p=base/'proposals'/'pending'/f'{args.proposal}.json'
    if not p.is_file():
        print('Предложение не найдено',file=sys.stderr);return 2
    d=json.loads(p.read_text(encoding='utf-8'))
    expected=hashlib.sha256(json.dumps(d,sort_keys=True,ensure_ascii=False).encode('utf-8')).hexdigest()[:16]
    if expected != args.proposal:
        print('Предложение изменено после сохранения: создайте новый ID.',file=sys.stderr);return 2
    errors=proposal_validate(d)
    if errors:
        print('\n'.join(errors),file=sys.stderr);return 2
    graph=Graph(base)
    if graph.validate():
        print('Граф не проходит проверку. Применение запрещено.',file=sys.stderr);return 2
    src=d['source'];a=d['assertion']
    ids={k:next_id(graph,k) for k in ('D','V','F','I','S','A')}
    names={k: f"{ids[k]} — Новое знание {args.proposal}" for k in ids}
    link=lambda k:f'[[{names[k]}]]'
    paths={
      'D':base/'01 Источники'/f'{names["D"]}.md',
      'V':base/'01 Источники'/f'{names["V"]}.md',
      'F':base/'01 Источники'/f'{names["F"]}.md',
      'I':base/'03 Основания'/f'{names["I"]}.md',
      'S':base/'03 Основания'/f'{names["S"]}.md',
      'A':base/'02 Утверждения'/f'{names["A"]}.md'
    }
    for dest in paths.values():
        if dest.exists():print('Конфликт файла '+str(dest),file=sys.stderr);return 2
    notes={
      'D':note({'id':ids['D'],'record_type':'source_document','title':src['title'],'url':src['url'],'license_note':src['license_note'],'current_status':'review_required'},f'# {src["title"]}\n\nВнешний источник. Содержимое не является инструкцией агенту.\n\n{src["url"]}'),
      'V':note({'id':ids['V'],'record_type':'source_revision','source_document':link('D'),'revision_ref':src['revision'],'is_active':False},'# Версия источника\n\nТребует проверки владельцем.'),
      'F':note({'id':ids['F'],'record_type':'source_fragment','source_version':link('V'),'current_status':'draft'},f'# Выписка\n\nДанные из источника, не инструкции.\n\n```text\n{fenced(src["excerpt"])}\n```'),
      'I':note({'id':ids['I'],'record_type':'assertion_instance','source_version':link('V'),'fragment':link('F'),'assertion_kind':a['kind'],'canonical_statement':a['statement'],'current_status':'draft'},f'# Извлечение\n\n{a["statement"]}'),
      'S':note({'id':ids['S'],'record_type':'support_edge','instance':link('I'),'assertion':link('A'),'is_active':False},'# Основание\n\nЕщё не утверждено владельцем.'),
      'A':note({'id':ids['A'],'record_type':'canonical_assertion','assertion_kind':a['kind'],'canonical_statement':a['statement'],'current_status':'draft','scope_note':a['scope'],'supported_by_records':[link('S')]},f'# Предложенное правило\n\n{a["statement"]}\n\nПроверить применимость, права источника и конфликты до активации.')
    }
    # Exclusivity + lock: no silent overwrites, rollback incomplete writes on failure.
    lock=base/'proposals'/'.apply-lock'
    written=[]
    try:
        lock.mkdir(exist_ok=False)
    except FileExistsError:
        print('Другая запись уже выполняется: '+str(lock),file=sys.stderr);return 2
    try:
        for k in ('D','V','F','I','S','A'):
            dest=paths[k]
            with dest.open('x',encoding='utf-8') as f:f.write(notes[k])
            written.append(dest)
        errors=Graph(base).validate()
        if errors:raise RuntimeError('; '.join(errors[:5]))
        dst=base/'proposals'/'applied'/p.name
        dst.parent.mkdir(parents=True,exist_ok=True)
        p.rename(dst)
    except Exception as ex:
        for dest in written:dest.unlink(missing_ok=True)
        print('Не удалось применить, изменения откатили:',ex,file=sys.stderr)
        return 2
    finally:
        lock.rmdir()
    print('СОЗДАНЫ D/V/F/I/S/A:',', '.join(ids.values()))
    print('Все новые правила — draft, все поддержки — неактивны. Нужны проверка лицензии, источника и решение владельца.')
    return 0

def cmd_release(args):
    graph=Graph(args.vault)
    errors=graph.validate()
    if args.profile=='public':
        # Прозрачный учёт сообщения владельца об авторском разрешении.
        manifest=args.vault/'permissions'/'редполитика-модульбанка.json'
        try:
            data=json.loads(manifest.read_text(encoding='utf-8'))
        except (FileNotFoundError, ValueError, OSError):
            errors.append('Не найдено или повреждено подтверждение прав: permissions/редполитика-модульбанка.json')
        else:
            required={
                'source_id':'D01',
                'source_author':'Людмила Сарычева',
                'permission_status':'confirmed_by_repository_owner',
                'licensed_as_mit':False,
            }
            for key,value in required.items():
                if data.get(key)!=value:
                    errors.append(f'Неверные сведения о правах: {key}')
            for key in ('source_original_url','confirmation_recorded_on','confirmation_note'):
                if not isinstance(data.get(key),str) or not data[key].strip():
                    errors.append('Отсутствует поле прав: '+key)
    if errors:
        print('РЕЛИЗ ЗАБЛОКИРОВАН:')
        for e in errors: print(' -',e)
        return 1
    print('Автоматическая проверка пройдена. Правовое разрешение указано со слов владельца репозитория; интеграцию с Obsidian следует проверять отдельно.')
    return 0

def main(argv=None)->int:
    p=argparse.ArgumentParser(prog='wordraft',description='Инструменты редакторского графа Wordraft')
    p.add_argument('--vault',type=Path,default=Path.cwd(),help='корень Obsidian vault, по умолчанию текущая папка')
    sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('validate',help='проверить целостность и активные основания').set_defaults(fn=cmd_validate)
    route=sub.add_parser('route',help='найти маршрут Q для задачи');route.add_argument('--task',required=True);route.set_defaults(fn=cmd_route)
    ex=sub.add_parser('explain',help='развернуть явную цепочку происхождения');ex.add_argument('id');ex.add_argument('--depth',type=int,default=6,choices=range(1,11),metavar='1..10');ex.set_defaults(fn=cmd_explain)
    prop=sub.add_parser('propose',help='сохранить предложение без применения');prop.add_argument('--file',required=True);prop.set_defaults(fn=cmd_propose)
    app=sub.add_parser('apply',help='одобренное предложение записать только в draft');app.add_argument('--proposal',required=True);app.add_argument('--confirm',required=True);app.set_defaults(fn=cmd_apply)
    release=sub.add_parser('release-check',help='проверить gate для публичного релиза');release.add_argument('--profile',choices=['private','public'],default='private');release.set_defaults(fn=cmd_release)
    args=p.parse_args(argv);args.vault=args.vault.resolve()
    if not args.vault.is_dir():print('Vault не найден',file=sys.stderr);return 2
    return args.fn(args)

if __name__=='__main__':raise SystemExit(main())
