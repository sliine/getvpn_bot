import logging
from datetime import datetime

import aiomysql

from app.config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

logger = logging.getLogger(__name__)

_pool: aiomysql.Pool | None = None


async def create_pool() -> None:
    global _pool
    _pool = await aiomysql.create_pool(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME,
        autocommit=True,
        charset="utf8mb4",
    )
    logger.info("Пул з'єднань з базою даних створено.")


async def close_pool() -> None:
    if _pool:
        _pool.close()
        await _pool.wait_closed()
        logger.info("Пул з'єднань з базою даних закрито.")


async def init_db() -> None:
    """Створює таблицю users, якщо вона ще не існує."""
    async with _pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SET sql_notes = 0;")
            await cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id           BIGINT        NOT NULL PRIMARY KEY COMMENT 'Telegram user ID',
                    username     VARCHAR(255)  DEFAULT NULL          COMMENT 'Telegram @username',
                    full_name    VARCHAR(255)  NOT NULL              COMMENT 'Ім''я та прізвище',
                    phone_number VARCHAR(20)   NOT NULL              COMMENT 'Номер телефону (+380...)',
                    is_confirmed BOOLEAN       NOT NULL DEFAULT FALSE,
                    confirmed_at DATETIME      DEFAULT NULL,
                    created_at   DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """)
            await cur.execute("SET sql_notes = 1;")
    logger.info("Таблицю users ініціалізовано.")


async def get_user(user_id: int) -> dict | None:
    """Повертає запис користувача або None."""
    async with _pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(
                "SELECT * FROM users WHERE id = %s",
                (user_id,),
            )
            return await cur.fetchone()


async def save_confirmed_user(
    user_id: int,
    username: str | None,
    full_name: str,
    phone_number: str,
) -> None:
    """Зберігає або оновлює підтвердженого користувача."""
    async with _pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                INSERT INTO users (id, username, full_name, phone_number, is_confirmed, confirmed_at)
                VALUES (%s, %s, %s, %s, TRUE, %s)
                ON DUPLICATE KEY UPDATE
                    username     = VALUES(username),
                    full_name    = VALUES(full_name),
                    phone_number = VALUES(phone_number),
                    is_confirmed = TRUE,
                    confirmed_at = VALUES(confirmed_at)
            """, (user_id, username, full_name, phone_number, datetime.now()))
