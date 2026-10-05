# Fly Client — secure version

## Важно
GitHub Pages запускает только frontend. Настоящая регистрация и защищённая админка работают через backend.

### 1. Backend
Папка `backend` рассчитана на Render/Railway/VPS:
- установите Python 3.11+
- `pip install -r requirements.txt`
- задайте переменные окружения из `.env.example`
- запустите `python server.py`

### 2. Frontend
В `frontend/script.js` замените:
`https://YOUR-BACKEND-URL.example.com/api`
на URL вашего backend.

После этого содержимое `frontend` можно разместить на GitHub Pages.

### 3. Админ
Логин по умолчанию: `noabot5`.
Пароль обязательно задайте через `ADMIN_PASS` на сервере. Не храните настоящий пароль в GitHub.

### 4. Мод
Fly Client предназначен только для компьютера. В интерфейсе есть кнопки для скачивания лаунчера и мода для ПК. Сам файл мода нужно будет подключить после его загрузки на сервер.
