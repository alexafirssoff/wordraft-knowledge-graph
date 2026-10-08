---
id: P19
record_type: editorial_procedure
title: Regression evaluation после изменения графа
current_status: active
domain: evaluation
uses_assertions: []
uses_practices:
- '[[K15 — Тестировать понимание, а не только грамотность]]'
- '[[K35 — Indirect prompt injection тестировать в реальном external channel]]'
- '[[K36 — Управлять редактором через Govern → Map → Measure → Manage]]'
consult_resources:
- '[[R03 — Digital.gov Plain Language Guide]]'
- '[[R17 — OWASP LLM Prompt Injection Prevention Cheat Sheet]]'
- '[[R19 — NIST AI Risk Management Framework (AI RMF)]]'
- '[[R20 — NIST Generative AI Profile (NIST AI 600-1)]]'
---

# Regression evaluation после изменения графа

## Цель

Процедурный узел: определяет **когда и в каком порядке** применять знания. Он не создаёт языковую норму сам по себе.

## Шаги

1. Запустить релевантные C cases без чтения expected outcomes.
2. Сохранить фактические ответы.
3. Сравнить с expected отдельно.
4. Измерить regressions: factual preservation, unsupported claims, unnecessary edits, exception accuracy, provenance, security boundary.
5. Документировать изменение качества.

## Stop / escalation condition

Не объявлять улучшение по одной удачной демонстрации.

## Основания и справочники

### Advisory K
- [[K15 — Тестировать понимание, а не только грамотность]]
- [[K35 — Indirect prompt injection тестировать в реальном external channel]]
- [[K36 — Управлять редактором через Govern → Map → Measure → Manage]]

### External R
- [[R03 — Digital.gov Plain Language Guide]]
- [[R17 — OWASP LLM Prompt Injection Prevention Cheat Sheet]]
- [[R19 — NIST AI Risk Management Framework (AI RMF)]]
- [[R20 — NIST Generative AI Profile (NIST AI 600-1)]]
