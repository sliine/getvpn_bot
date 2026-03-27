from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


def share_phone_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [[KeyboardButton("📱 Поділитися номером телефону", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔑 Ключі", callback_data="menu_keys")],
        [InlineKeyboardButton("📖 Як підключити", callback_data="menu_info")],
        [InlineKeyboardButton("💬 Підтримка", url="https://t.me/karasiqsupport_bot")],
    ])


def locations_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🇧🇬 Болгарія", callback_data="key_bulgaria"),
            InlineKeyboardButton("🇬🇪 Грузія", callback_data="key_georgia"),
        ],
        [InlineKeyboardButton("🏠 Головне меню", callback_data="back_main")],
    ])


def key_actions_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📖 Як підключити", callback_data="menu_info")],
        [InlineKeyboardButton("🔙 До локацій", callback_data="menu_keys")],
    ])


def back_to_main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏠 Головне меню", callback_data="back_main")],
    ])
