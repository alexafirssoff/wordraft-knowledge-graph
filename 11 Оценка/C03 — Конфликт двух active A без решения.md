---
id: C03
record_type: evaluation_case
title: Конфликт двух active A без решения
current_status: active
route: '[[Q08 — Полный нормативный аудит]]'
hidden_from_runtime_context: true
---

# Конфликт двух active A без решения

## Вход

Два active A одинаковой области явно conflicts_with друг друга.

## Ожидаемое решение

Сообщить конфликт и запросить owner decision.

## Недопустимое решение

Самостоятельно выбрать более новое/строгое правило.

## Процедура теста

Запустить задачу без чтения этой карточки. Сохранить ответ. Затем сравнить с expected outcome и проверить provenance/semantic preservation отдельно.
