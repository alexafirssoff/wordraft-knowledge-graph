#!/usr/bin/env python3
"""Копирует авторские Wordraft Skills. Не включает сторонние redaktura-skills."""
from __future__ import annotations
import argparse,shutil,sys
from pathlib import Path

def main(argv=None):
    parser=argparse.ArgumentParser(description='Подключить Wordraft Skills к CLI-агенту')
    parser.add_argument('--agent',required=True,choices=['claude','codex'])
    parser.add_argument('--scope',required=True,choices=['project','user'])
    parser.add_argument('--force',action='store_true',help='обновить уже установленные наши скиллы')
    args=parser.parse_args(argv)
    root=Path(__file__).resolve().parent.parent
    src=root/'copilot'/'skills'
    if args.scope=='user':target=Path.home()/('.claude/skills' if args.agent=='claude' else '.codex/skills')
    else:target=root/('.claude/skills' if args.agent=='claude' else '.agents/skills')
    target.mkdir(parents=True,exist_ok=True)
    for item in sorted(src.glob('wordraft-*')):
        dest=target/item.name
        if dest.exists() and not args.force:
            print('Пропуск, уже существует:',dest)
            continue
        if dest.exists() and args.force:shutil.rmtree(dest)
        shutil.copytree(item,dest)
        print('Установлен:',dest)
    return 0

if __name__=='__main__':raise SystemExit(main())
