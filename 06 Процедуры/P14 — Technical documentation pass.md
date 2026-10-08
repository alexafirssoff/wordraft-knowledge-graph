---
id: P14
record_type: editorial_procedure
title: Technical documentation pass
current_status: active
domain: technical_docs
uses_assertions: []
uses_practices:
- '[[K03 — Grounding продуктовых утверждений]]'
- '[[K06 — Структура должна поддерживать сканирование]]'
- '[[K09 — Один смысл — один термин]]'
- '[[K14 — Абстрактное объяснять примерами и edge cases]]'
- '[[K20 — Сначала определить тип документа]]'
- '[[K21 — Документация не должна спекулировать о продукте]]'
- '[[K22 — Инструкции： обращаться прямо и давать действие]]'
- '[[K23 — Descriptive headings, labels и links]]'
- '[[K32 — Разводить tutorial ／ how-to ／ reference ／ explanation]]'
consult_resources:
- '[[R05 — Google Developer Documentation Style Guide]]'
- '[[R10 — GitLab Documentation Style Guide]]'
- '[[R11 — GitLab AI agent instruction files for documentation]]'
- '[[R12 — MDN Writing Style Guide]]'
- '[[R13 — Diátaxis]]'
---

# Technical documentation pass

## Цель

Процедурный узел: определяет **когда и в каком порядке** применять знания. Он не создаёт языковую норму сам по себе.

## Шаги

1. Определить тип документа по Diátaxis.
2. Сверить product facts с SSoT.
3. Использовать consistent terminology и явных actors.
4. Добавить examples/edge cases там, где они снимают ambiguity.
5. Разделить task steps и conceptual explanation.

## Stop / escalation condition

Не генерировать API/UI details из памяти модели, если они не подтверждены.

## Основания и справочники

### Advisory K
- [[K03 — Grounding продуктовых утверждений]]
- [[K06 — Структура должна поддерживать сканирование]]
- [[K09 — Один смысл — один термин]]
- [[K14 — Абстрактное объяснять примерами и edge cases]]
- [[K20 — Сначала определить тип документа]]
- [[K21 — Документация не должна спекулировать о продукте]]
- [[K22 — Инструкции： обращаться прямо и давать действие]]
- [[K23 — Descriptive headings, labels и links]]
- [[K32 — Разводить tutorial ／ how-to ／ reference ／ explanation]]

### External R
- [[R05 — Google Developer Documentation Style Guide]]
- [[R10 — GitLab Documentation Style Guide]]
- [[R11 — GitLab AI agent instruction files for documentation]]
- [[R12 — MDN Writing Style Guide]]
- [[R13 — Diátaxis]]
