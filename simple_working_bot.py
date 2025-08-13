#!/usr/bin/env python3
"""
Простой рабочий бот для локального тестирования
"""

import asyncio
import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Загружаем переменные окружения
load_dotenv()

# Инициализация бота
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

# Создание клавиатуры
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Справочник"), KeyboardButton(text="Тесты (сайт)")],
        [KeyboardButton(text="Наш тест"), KeyboardButton(text="Консультация")],
        [KeyboardButton(text="ИИ-Определение"), KeyboardButton(text="Подписка")],
        [KeyboardButton(text="Пакеты"), KeyboardButton(text="Курсы")],
        [KeyboardButton(text="Карты")]
    ],
    resize_keyboard=True
)

# Обработчики команд
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    logger.info(f"Пользователь {user_id} отправил /start")
    
    await message.answer(
        "Привет! Я бот-человековед. Выберите действие:",
        reply_markup=keyboard
    )

@dp.message()
async def handle_messages(message: types.Message):
    text = message.text
    user_id = message.from_user.id
    
    logger.info(f"Пользователь {user_id}: {text}")
    
    if text == "Справочник":
        await message.answer("WebView: Справочник (мок)")
    elif text == "Тесты (сайт)":
        await message.answer("Доступные тесты:\n1. Тест на определение типа личности\n2. Тест на эмоциональный интеллект\n3. Тест на коммуникативные навыки\n4. Тест на лидерские качества")
    elif text == "Наш тест":
        await message.answer("Начинаем тест! Вопрос 1: Как вы обычно реагируете на стресс?\n\nA) Активно решаю проблему\nB) Беру паузу для размышлений\nC) Ищу поддержку у других\nD) Игнорирую и продолжаю работать")
    elif text == "Консультация":
        await message.answer("Консультация: Рекомендую обратиться к специалисту для получения персональных рекомендаций по развитию ваших навыков.")
    elif text == "ИИ-Определение":
        await message.answer("Анализ фото выполнен успешно (мок)")
    elif text == "Подписка":
        await message.answer("WebView: Подписка (мок)")
    elif text == "Пакеты":
        await message.answer("WebView: Пакеты (мок)")
    elif text == "Курсы":
        await message.answer("WebView: Курсы (мок)")
    elif text == "Карты":
        await message.answer("WebView: Карты (мок)")
    else:
        await message.answer("Выберите действие из меню ниже:", reply_markup=keyboard)

async def main():
    logger.info("Starting Humanology Bot...")
    logger.info(f"BOT_TOKEN: {os.getenv('BOT_TOKEN')}")
    
    try:
        logger.info("Bot started successfully!")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        exit(1)
