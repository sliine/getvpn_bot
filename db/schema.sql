-- Схема бази даних для give-vpnbot
-- Виконати один раз перед запуском бота

CREATE DATABASE IF NOT EXISTS vpnbot
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE vpnbot;

CREATE TABLE IF NOT EXISTS users (
    id           BIGINT        NOT NULL PRIMARY KEY COMMENT 'Telegram user ID',
    username     VARCHAR(255)  DEFAULT NULL          COMMENT 'Telegram @username',
    full_name    VARCHAR(255)  NOT NULL              COMMENT 'Ім''я та прізвище',
    phone_number VARCHAR(20)   NOT NULL              COMMENT 'Номер телефону (+380...)',
    is_confirmed BOOLEAN       NOT NULL DEFAULT FALSE,
    confirmed_at DATETIME      DEFAULT NULL,
    created_at   DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
