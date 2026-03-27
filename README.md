# getvpn_bot

Телеграм-бот для роздачі VPN-ключів. Перед тим як отримати ключ, юзер підтверджує акаунт через номер телефону — приймаються тільки українські номери (+380). Всі дані пишуться в MySQL.

---

## Структура

```
getvpn_bot/
├── app/
│   ├── config.py       — змінні з .env
│   ├── database.py     — робота з MySQL
│   ├── handlers.py     — обробка повідомлень і callback
│   └── keyboards.py    — кнопки
├── db/
│   └── schema.sql      — схема БД
├── .github/
│   └── workflows/
│       └── deploy.yml  — CI перевірка синтаксису
├── main.py             — запуск бота
├── requirements.txt
└── .env.example
```

---

## Як запустити

**1. Клонувати і зайти в папку**
```bash
git clone https://github.com/sliine/getvpn_bot.git
cd getvpn_bot
```

**2. Створити віртуальне середовище**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

**3. Встановити залежності**
```bash
pip install -r requirements.txt
```

**4. Підготувати базу даних**
```bash
mysql -u root -p < db/schema.sql
```

**5. Налаштувати `.env`**
```bash
cp .env.example .env
# далі заповнити своїми даними
```

**6. Запустити**
```bash
python main.py
```

---

## Змінні середовища

| Змінна | Опис |
|---|---|
| `BOT_TOKEN` | Токен від @BotFather |
| `DB_HOST` | Хост MySQL |
| `DB_PORT` | Порт (за замовчуванням 3306) |
| `DB_USER` | Користувач БД |
| `DB_PASSWORD` | Пароль БД |
| `DB_NAME` | Назва бази |
| `KEY_BULGARIA` | VPN ключ — сервер Болгарія |
| `KEY_GEORGIA` | VPN ключ — сервер Грузія |
| `SUPPORT_BOT_URL` | Посилання на бота підтримки |

---

## Ліцензія

MIT
