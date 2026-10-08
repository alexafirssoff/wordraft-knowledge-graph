---
id: K34
record_type: external_practice
title: Persistent memory и knowledge graph нельзя пополнять сырым внешним текстом
current_status: advisory
strength: security
domains:
- agent_security
- memory
grounded_in:
- '[[R18 — OWASP AI Agent Security Cheat Sheet]]'
related_assertions: []
may_be_reported_as_violation: false
---

# Persistent memory и knowledge graph нельзя пополнять сырым внешним текстом

## Рабочая практика

Перед persistence внешние данные валидировать, нормализовать и привязывать к provenance. Сырые инструкции/текст не становятся памятью или активным правилом автоматически.

## Границы

Promotion в A выполняется только через controlled knowledge-update flow.

## Статус

Это **advisory practice**, а не active canonical assertion. В ревью её можно использовать как «рекомендацию», но не как нарушение политики. При конфликте с active A действует [[J02 — Локальная активная норма сильнее advisory-практики]].

## Источники

- [[R18 — OWASP AI Agent Security Cheat Sheet]]
