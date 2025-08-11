#!/usr/bin/env python3
"""Скрипт для запуска бота в production режиме."""

import asyncio
import logging
import os
import sys
from pathlib import Path

# Добавляем корневую директорию в PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent))

from config import settings
from main import app
import uvicorn


def setup_logging():
    """Настройка логирования для production."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("logs/bot.log"),
        ]
    )


def create_directories():
    """Создание необходимых директорий."""
    directories = ["logs", "storage"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)


def check_environment():
    """Проверка переменных окружения."""
    required_vars = [
        "BOT_TOKEN",
        "WEBHOOK_URL", 
        "DB_DSN",
        "SITE_API_URL",
        "SITE_API_KEY",
        "OPENAI_API_KEY"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not getattr(settings, var.lower(), None):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Отсутствуют обязательные переменные окружения: {', '.join(missing_vars)}")
        print("Проверьте файл .env")
        sys.exit(1)
    
    print("✅ Все обязательные переменные окружения установлены")


def main():
    """Основная функция запуска."""
    print("🚀 Запуск Humanology Bot в production режиме...")
    
    # Создаем директории
    create_directories()
    
    # Настраиваем логирование
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Проверяем окружение
    check_environment()
    
    logger.info("Запуск FastAPI приложения...")
    logger.info(f"Host: {settings.host}")
    logger.info(f"Port: {settings.port}")
    logger.info(f"Debug: {settings.debug}")
    logger.info(f"Webhook URL: {settings.webhook_url}")
    
    # Запускаем FastAPI приложение
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info" if not settings.debug else "debug",
        access_log=True
    )


if __name__ == "__main__":
    main()
