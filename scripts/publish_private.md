# Подготовка приватного репозитория на GitHub

Убедитесь, что вы распаковали архив и открыли терминал в папке с `README.md`. Не переводите репозиторий в публичный режим, пока не выполнены требования `docs/Публикация.md`.

Вариант через GitHub CLI (`gh` должен быть установлен и авторизован):

```bash
git init -b main
git add .
git commit -m "Prepare Wordraft vault and agent workflows"
gh repo create alexafirssoff/wordraft-knowledge-graph --private --source . --remote origin --push
```

Альтернатива: создайте на github.com пустой **Private** репозиторий с таким названием, без автоматических README и `.gitignore`. Затем выполните команды `git init`, `git add`, `git commit` и `git remote add origin <адрес>` / `git push -u origin main`.

Проверка перед открытием доступа:

```bash
python -m wordraft release-check --profile public
```

В текущем полном корпусе она ожидаемо не пройдёт. Причина подробно описана в `NOTICE-CONTENT.md`.
