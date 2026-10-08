---
id: K03
record_type: external_practice
title: Grounding продуктовых утверждений
current_status: advisory
strength: advisory
domains:
- fact_integrity
- technical_writing
grounded_in:
- '[[R10 — GitLab Documentation Style Guide]]'
- '[[R11 — GitLab AI agent instruction files for documentation]]'
related_assertions: []
may_be_reported_as_violation: false
---

# Grounding продуктовых утверждений

## Рабочая практика

Утверждения о продукте, интерфейсе, API, команде или процессе должны опираться на доступный source of truth: код, документацию, бриф, данные или подтверждённый источник. Не infer-ить продуктовые факты из правдоподобия.

## Границы

Редактор может улучшить форму неподтверждённой фразы, но не должен повышать её степень уверенности.

## Статус

Это **advisory practice**, а не active canonical assertion. В ревью её можно использовать как «рекомендацию», но не как нарушение политики. При конфликте с active A действует [[J02 — Локальная активная норма сильнее advisory-практики]].

## Источники

- [[R10 — GitLab Documentation Style Guide]]
- [[R11 — GitLab AI agent instruction files for documentation]]
