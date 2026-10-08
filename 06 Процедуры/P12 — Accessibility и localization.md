---
id: P12
record_type: editorial_procedure
title: Accessibility и localization
current_status: active
domain: accessibility
uses_assertions:
- '[[A29 — Говорить на языке клиента]]'
- '[[A33 — Расшифровывать незнакомые и сложные аббревиатуры]]'
- '[[A34 — Простые аббревиатуры желательно расшифровывать]]'
uses_practices:
- '[[K10 — Объяснять jargon, uncommon words и abbreviations]]'
- '[[K12 — Писать так, чтобы текст переносился между культурами и локалями]]'
- '[[K13 — Проверять inclusive language по контексту]]'
- '[[K23 — Descriptive headings, labels и links]]'
- '[[K24 — Когнитивная доступность： clear words, short blocks, simple tense]]'
consult_resources:
- '[[R05 — Google Developer Documentation Style Guide]]'
- '[[R08 — W3C Cognitive Accessibility Guidance]]'
- '[[R09 — WCAG 2.2]]'
- '[[R10 — GitLab Documentation Style Guide]]'
- '[[R12 — MDN Writing Style Guide]]'
- '[[R15 — Atlassian Content Design]]'
---

# Accessibility и localization

## Цель

Процедурный узел: определяет **когда и в каком порядке** применять знания. Он не создаёт языковую норму сам по себе.

## Шаги

1. Проверить понятность headings/labels/link text.
2. Убрать unnecessary ambiguity, unexplained acronyms и culture-bound phrasing в global content.
3. Для инструкций/форм проверить clear words, chunks и step order.
4. Не снижать техническую точность “ради accessibility”.

## Stop / escalation condition

Если требуется formal WCAG conformance, editor делает content pass, но не заменяет полный accessibility audit интерфейса.

## Основания и справочники

### Active A
- [[A29 — Говорить на языке клиента]]
- [[A33 — Расшифровывать незнакомые и сложные аббревиатуры]]
- [[A34 — Простые аббревиатуры желательно расшифровывать]]

### Advisory K
- [[K10 — Объяснять jargon, uncommon words и abbreviations]]
- [[K12 — Писать так, чтобы текст переносился между культурами и локалями]]
- [[K13 — Проверять inclusive language по контексту]]
- [[K23 — Descriptive headings, labels и links]]
- [[K24 — Когнитивная доступность： clear words, short blocks, simple tense]]

### External R
- [[R05 — Google Developer Documentation Style Guide]]
- [[R08 — W3C Cognitive Accessibility Guidance]]
- [[R09 — WCAG 2.2]]
- [[R10 — GitLab Documentation Style Guide]]
- [[R12 — MDN Writing Style Guide]]
- [[R15 — Atlassian Content Design]]
