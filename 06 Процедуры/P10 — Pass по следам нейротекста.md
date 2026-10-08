---
id: P10
record_type: editorial_procedure
title: Pass по следам нейротекста
current_status: active
domain: ai_text
uses_assertions:
- '[[A20 — Удалять усилители]]'
- '[[A25 — Оценку заменять фактами]]'
- '[[A47 — Чек-лист: авторский стиль не равен мусорным словам]]'
uses_practices:
- '[[K27 — Отдельный pass по AI-patterns]]'
consult_resources:
- '[[R01 — redaktura-skills]]'
- '[[R10 — GitLab Documentation Style Guide]]'
---

# Pass по следам нейротекста

## Цель

Процедурный узел: определяет **когда и в каком порядке** применять знания. Он не создаёт языковую норму сам по себе.

## Шаги

1. Искать концентрацию повторяющихся AI-patterns, а не отдельные “подозрительные” слова.
2. Убирать vague self-commentary, repetitive summaries, шаблонные антитезы и claims без grounding.
3. Сохранять авторские особенности, если они функциональны.

## Stop / escalation condition

Не объявлять текст “написанным AI” по стилю; задача — качество, не атрибуция автора.

## Основания и справочники

### Active A
- [[A20 — Удалять усилители]]
- [[A25 — Оценку заменять фактами]]
- [[A47 — Чек-лист: авторский стиль не равен мусорным словам]]

### Advisory K
- [[K27 — Отдельный pass по AI-patterns]]

### External R
- [[R01 — redaktura-skills]]
- [[R10 — GitLab Documentation Style Guide]]
