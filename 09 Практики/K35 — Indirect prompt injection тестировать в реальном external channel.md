---
id: K35
record_type: external_practice
title: Indirect prompt injection тестировать в реальном external channel
current_status: advisory
strength: security
domains:
- agent_security
- evaluation
grounded_in:
- '[[R17 — OWASP LLM Prompt Injection Prevention Cheat Sheet]]'
related_assertions: []
may_be_reported_as_violation: false
---

# Indirect prompt injection тестировать в реальном external channel

## Рабочая практика

Security eval должен помещать атакующий текст именно в внешний канал (web/doc/email), который тестируется, и проверять observable outcome, а не только response wording.

## Границы

Использовать sandbox/dummy data; не превращать security eval в реальное опасное действие.

## Статус

Это **advisory practice**, а не active canonical assertion. В ревью её можно использовать как «рекомендацию», но не как нарушение политики. При конфликте с active A действует [[J02 — Локальная активная норма сильнее advisory-практики]].

## Источники

- [[R17 — OWASP LLM Prompt Injection Prevention Cheat Sheet]]
