import logging

from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from app import database
from app.config import KEY_BULGARIA, KEY_GEORGIA
from app.keyboards import (
    share_phone_keyboard,
    main_menu_keyboard,
    locations_keyboard,
    key_actions_keyboard,
    back_to_main_keyboard,
)

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def _normalize_phone(phone: str) -> str:
    return phone if phone.startswith("+") else "+" + phone


def _is_ukrainian_number(phone: str) -> bool:
    return phone.startswith("+380")


# ──────────────────────────────────────────────
# Command handlers
# ──────────────────────────────────────────────

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    db_user = await database.get_user(user.id)

    if db_user and db_user["is_confirmed"]:
        await update.message.reply_text(
            f"👋 Вітаємо, <b>{user.first_name}</b>!\n\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "Оберіть потрібний розділ 👇",
            parse_mode="HTML",
            reply_markup=main_menu_keyboard(),
        )
        return

    await update.message.reply_text(
        "👋 <b>Вітаємо!</b>\n\n"
        "Для підтвердження акаунту натисніть кнопку нижче та поділіться своїм номером телефону.\n\n"
        "🔒 <i>Ми не зберігаємо ваші дані без вашої згоди.</i>",
        parse_mode="HTML",
        reply_markup=share_phone_keyboard(),
    )


# ──────────────────────────────────────────────
# Message handlers
# ──────────────────────────────────────────────

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    contact = update.message.contact

    if contact.user_id and contact.user_id != user.id:
        await update.message.reply_text(
            "⚠️ <b>Помилка!</b>\n\n"
            "Будь ласка, поділіться <b>власним</b> номером телефону, а не чужим.",
            parse_mode="HTML",
            reply_markup=share_phone_keyboard(),
        )
        return

    phone = _normalize_phone(contact.phone_number)

    if not _is_ukrainian_number(phone):
        await update.message.reply_text(
            "🚫 <b>Недоступна можливість підтвердження акаунту</b>\n\n"
            "Підтвердження доступне лише для українських номерів <b>(+380)</b>.",
            parse_mode="HTML",
            reply_markup=ReplyKeyboardRemove(),
        )
        return

    full_name = f"{user.first_name} {user.last_name or ''}".strip()

    await database.save_confirmed_user(
        user_id=user.id,
        username=user.username,
        full_name=full_name,
        phone_number=phone,
    )

    await update.message.reply_text(
        "✅ Акаунт підтверджено!",
        reply_markup=ReplyKeyboardRemove(),
    )
    await update.message.reply_text(
        "🏠 <b>Головне меню</b>\n\n"
        "Оберіть потрібний розділ 👇",
        parse_mode="HTML",
        reply_markup=main_menu_keyboard(),
    )
    logger.info("Акаунт підтверджено: user_id=%s, phone=%s", user.id, phone)


async def handle_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🤖 Скористайтеся командою /start для підтвердження акаунту.",
    )


# ──────────────────────────────────────────────
# Callback handler
# ──────────────────────────────────────────────

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    user = update.effective_user
    db_user = await database.get_user(user.id)

    if query.data != "back_main" and not (db_user and db_user["is_confirmed"]):
        await query.answer(
            "⚠️ Спочатку підтвердіть акаунт командою /start",
            show_alert=True,
        )
        return

    if query.data == "menu_keys":
        await query.edit_message_text(
            "🔑 <b>Ключі доступу</b>\n\n"
            "Оберіть локацію сервера 🌍",
            parse_mode="HTML",
            reply_markup=locations_keyboard(),
        )

    elif query.data == "key_bulgaria":
        key = KEY_BULGARIA or "<i>Ключ ще не налаштовано</i>"
        await query.edit_message_text(
            f"🇧🇬 <b>Сервер — Болгарія</b>\n\n"
            f"Ваш ключ для підключення:\n"
            f"<code>{key}</code>\n\n"
            "📋 Натисніть на ключ, щоб скопіювати, та імпортуйте у свій VPN-клієнт.",
            parse_mode="HTML",
            reply_markup=key_actions_keyboard(),
        )

    elif query.data == "key_georgia":
        key = KEY_GEORGIA or "<i>Ключ ще не налаштовано</i>"
        await query.edit_message_text(
            f"🇬🇪 <b>Сервер — Грузія</b>\n\n"
            f"Ваш ключ для підключення:\n"
            f"<code>{key}</code>\n\n"
            "📋 Натисніть на ключ, щоб скопіювати, та імпортуйте у свій VPN-клієнт.",
            parse_mode="HTML",
            reply_markup=key_actions_keyboard(),
        )

    elif query.data == "menu_info":
        await query.edit_message_text(
            "📖 <b>Як підключити VPN</b>\n\n"
            "Оберіть інструкцію для свого клієнта:\n\n"
            "〰 <a href='https://telegra.ph/Hiddify-instruction'>Hiddify</a>\n"
            "〰 <a href='https://telegra.ph/V2rayNG-instruction'>V2rayNG</a>",
            parse_mode="HTML",
            disable_web_page_preview=True,
            reply_markup=back_to_main_keyboard(),
        )

    elif query.data == "back_main":
        await query.edit_message_text(
            "🏠 <b>Головне меню</b>\n\n"
            "Оберіть потрібний розділ 👇",
            parse_mode="HTML",
            reply_markup=main_menu_keyboard(),
        )
