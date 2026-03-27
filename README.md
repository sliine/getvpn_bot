# 🔐 GetVPN Bot

Telegram-бот для видачі VPN-ключів користувачам з підтвердженням акаунту за українським номером телефону (+380). Дані зберігаються у MySQL.

---

## 🗂 Структура проєкту

```
getvpn_bot/
├── app/
│   ├── __init__.py
│   ├── config.py        # Зчитування змінних середовища
│   ├── database.py      # Підключення та операції з MySQL
│   ├── handlers.py      # Обробники повідомлень та callback
│   └── keyboards.py     # Клавіатури та кнопки
├── .github/
│   └── workflows/
│       └── deploy.yml   # GitHub Actions — автодеплой
├── main.py              # Точка входу — запуск бота
├── requirements.txt     # Залежності Python
├── schema.sql           # SQL-схема бази даних
├── .env.example         # Шаблон файлу конфігурації
└── .gitignore
```

---

## ⚙️ Вимоги

- Python **3.11+**
- MySQL **8.0+**
- Telegram Bot Token (отримати у [@BotFather](https://t.me/BotFather))

---

## 🚀 Запуск локально

### 1. Клонувати репозиторій

```bash
git clone https://github.com/sliine/getvpn_bot.git
cd getvpn_bot
```

### 2. Створити та активувати віртуальне середовище

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

### 3. Встановити залежності

```bash
pip install -r requirements.txt
```

### 4. Налаштувати базу даних

Виконати SQL-схему у своїй MySQL:

```bash
mysql -u root -p < schema.sql
```

### 5. Створити файл `.env`

Скопіювати шаблон і заповнити своїми даними:

```bash
cp .env.example .env
```

Відкрити `.env` та вказати значення:

```env
BOT_TOKEN=токен_від_BotFather

DB_HOST=localhost
DB_PORT=3306
DB_USER=користувач_бд
DB_PASSWORD=пароль_бд
DB_NAME=vpnbot

KEY_BULGARIA=vless://твій-ключ-болгарія
KEY_GEORGIA=vless://твій-ключ-грузія
```

### 6. Запустити бота

```bash
python main.py
```

---

## 🤖 Функціонал бота

| Дія | Опис |
|---|---|
| `/start` | Запуск бота, запит підтвердження акаунту |
| Поділитися номером | Перевірка: лише +380, запис у БД |
| 🔑 Ключі | Вибір локації (Болгарія / Грузія) та отримання ключа |
| 📖 Як підключити | Інструкції для Hiddify та V2rayNG |
| 💬 Підтримка | Посилання на бота підтримки |

---

## 🐳 Запуск у Docker (опційно)

```bash
docker build -t getvpn-bot .
docker run --env-file .env getvpn-bot
```

---

## 📋 Змінні середовища

| Змінна | Опис |
|---|---|
| `BOT_TOKEN` | Токен Telegram-бота |
| `DB_HOST` | Хост MySQL |
| `DB_PORT` | Порт MySQL (за замовчуванням `3306`) |
| `DB_USER` | Користувач MySQL |
| `DB_PASSWORD` | Пароль MySQL |
| `DB_NAME` | Назва бази даних |
| `KEY_BULGARIA` | VPN-ключ для сервера в Болгарії |
| `KEY_GEORGIA` | VPN-ключ для сервера в Грузії |

---

## 📄 Ліцензія

MIT
