---
id: P13
record_type: editorial_procedure
title: UX-copy pass
current_status: active
domain: ux_copy
uses_assertions: []
uses_practices:
- '[[K16 — Ошибка： что случилось + что делать]]'
- '[[K17 — Button label должен предсказывать действие]]'
- '[[K18 — Сценарий впереди экрана]]'
- '[[K19 — Hint text — только короткая помощь большинству]]'
- '[[K31 — UX-copy： сценарий → элемент → состояние → уведомление → tone]]'
- '[[K37 — Нельзя раскрывать наличие аккаунта]]'
consult_resources:
- '[[R01 — redaktura-skills]]'
- '[[R07 — GOV.UK Design System — content patterns]]'
- '[[R15 — Atlassian Content Design]]'
- '[[R16 — IBM Carbon Content Guidelines]]'
---

# UX-copy pass

## Цель

Процедурный узел: определяет **когда и в каком порядке** применять знания. Он не создаёт языковую норму сам по себе.

## Шаги

1. Описать user scenario: before / now / after.
2. Определить работу каждого элемента: heading, label, button, hint, error, notification.
3. Для error дать problem + recoverable action.
4. Для button сделать outcome/action предсказуемым.
5. Проверить, нужен ли notification вообще.

## Stop / escalation condition

Не выдумывать system behavior, SLA, channel, срок ответа или последствия действия.

## Основания и справочники

### Advisory K
- [[K16 — Ошибка： что случилось + что делать]]
- [[K17 — Button label должен предсказывать действие]]
- [[K18 — Сценарий впереди экрана]]
- [[K19 — Hint text — только короткая помощь большинству]]
- [[K31 — UX-copy： сценарий → элемент → состояние → уведомление → tone]]

### External R
- [[R01 — redaktura-skills]]
- [[R07 — GOV.UK Design System — content patterns]]
- [[R15 — Atlassian Content Design]]
- [[R16 — IBM Carbon Content Guidelines]]

### Расширение OWASP для учебного кейса

- [[K37 — Нельзя раскрывать наличие аккаунта]]
