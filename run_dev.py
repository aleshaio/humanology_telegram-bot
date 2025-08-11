#!/usr/bin/env python3
"""Скрипт для запуска бота в development режиме."""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Добавляем корневую директорию в PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent))

from bot.database.database import db
from bot.bot import telegram_bot


async def main():
    """Основная функция запуска."""
    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Запуск бота в development режиме...")
        
        # Создаем таблицы БД
        await db.create_tables()
        logger.info("Таблицы БД созданы/проверены")
        
        # Запускаем бота в polling режиме
        logger.info("Запуск бота в polling режиме...")
        await telegram_bot.dp.start_polling(telegram_bot.bot)
        
    except KeyboardInterrupt:
        logger.info("Получен сигнал остановки...")
    except Exception as e:
        logger.error(f"Ошибка запуска: {e}")
    finally:
        # Закрываем соединения
        await db.close()
        logger.info("Бот остановлен")


if __name__ == "__main__":
    # Проверяем наличие .env файла
    if not os.path.exists(".env"):
        print("❌ Файл .env не найден!")
        print("Скопируйте env.example в .env и настройте переменные окружения")
        sys.exit(1)
    
    # Запускаем бота
    asyncio.run(main())
