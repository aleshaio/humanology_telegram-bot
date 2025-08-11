#!/usr/bin/env python3
"""
Локальный режим отладки Telegram-бота (упрощенная версия)

Запуск: python run_local_simple.py (предварительно установить aiogram и python-dotenv)

Этот скрипт запускает бота в режиме polling для локальной отладки
без необходимости деплоя на сервер. Все внешние зависимости заменены моками.
"""

import asyncio
import logging
import os
import random
import sys
from pathlib import Path

# Добавляем корневую папку проекта в путь
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Настройка логирования для отладки
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Мок-данные для тестов
MOCK_TESTS = [
    {"id": 1, "name": "Тест на определение типа личности", "description": "16 вопросов для определения соционического типа"},
    {"id": 2, "name": "Тест на определение квадра", "description": "Определение принадлежности к одной из 4 квадр"},
    {"id": 3, "name": "Тест на определение роли", "description": "Определение роли в социуме"},
    {"id": 4, "name": "Тест на определение подтипа", "description": "Определение подтипа личности"}
]

MOCK_QUESTIONS = [
    {"id": 1, "question": "Как вы предпочитаете проводить свободное время?", "answers": ["В одиночестве", "В компании друзей", "Зависит от настроения"]},
    {"id": 2, "question": "Что для вас важнее в работе?", "answers": ["Результат", "Процесс", "Команда", "Признание"]},
    {"id": 3, "question": "Как вы принимаете решения?", "answers": ["Быстро, интуитивно", "Медленно, анализируя", "Советуюсь с другими"]},
    {"id": 4, "question": "Что вас больше мотивирует?", "answers": ["Достижение целей", "Новые впечатления", "Помощь другим", "Признание"]}
]

MOCK_CONSULT_ANSWERS = [
    "Спасибо за ваш вопрос! Я проанализирую ситуацию и дам рекомендации.",
    "Интересный вопрос. Позвольте мне подумать об этом с точки зрения психологии.",
    "Это очень важная тема. Давайте разберем её пошагово.",
    "Отличный вопрос! У меня есть несколько идей по этому поводу.",
    "Спасибо, что обратились за консультацией. Я готов помочь вам разобраться в этом вопросе.",
    "Это интересная проблема. Позвольте мне предложить несколько решений.",
    "Я понимаю вашу ситуацию. Давайте вместе найдем оптимальное решение.",
    "Спасибо за доверие. Я постараюсь дать максимально полезный совет."
]

async def main():
    """Основная функция запуска."""
    try:
        # Проверяем токен бота
        bot_token = os.getenv("BOT_TOKEN")
        if not bot_token or bot_token == "your_bot_token_here":
            logger.error("❌ Ошибка: BOT_TOKEN не найден в переменных окружения!")
            logger.error("📝 Создайте файл .env с вашим токеном бота от @BotFather")
            logger.error("💡 Пример: BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz")
            logger.error("🔗 Получите токен у @BotFather в Telegram")
            return
        
        logger.info("🚀 Запуск бота в локальном режиме отладки...")
        logger.info(f"🤖 Токен бота: {bot_token[:10]}...")
        
        # Импортируем aiogram
        from aiogram import Bot, Dispatcher, types
        from aiogram.filters import Command
        from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
        
        # Создаем бота и диспетчер
        bot = Bot(token=bot_token)
        dp = Dispatcher()
        
        # Создаем клавиатуру главного меню
        main_keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Справочник"),
                    KeyboardButton(text="Тесты (сайт)")
                ],
                [
                    KeyboardButton(text="Наш тест"),
                    KeyboardButton(text="Консультация")
                ],
                [
                    KeyboardButton(text="ИИ-Определение"),
                    KeyboardButton(text="Подписка")
                ],
                [
                    KeyboardButton(text="Пакеты"),
                    KeyboardButton(text="Курсы")
                ],
                [
                    KeyboardButton(text="Карты")
                ]
            ],
            resize_keyboard=True,
            input_field_placeholder="Выберите действие"
        )
        
        # Обработчик команды /start
        @dp.message(Command("start"))
        async def cmd_start(message: types.Message):
            user_id = message.from_user.id
            user_name = message.from_user.first_name or "Пользователь"
            
            logger.info(f"USER ACTION: user_id={user_id}, action=start_command, data=user_name={user_name}")
            
            welcome_text = f"""
🤖 Добро пожаловать в бота для определения типа личности!

👋 Привет, {user_name}! Я помогу вам определить ваш соционический тип.

📋 Выберите действие из меню ниже:
            """
            
            await message.answer(welcome_text, reply_markup=main_keyboard)
        
        # Обработчик кнопки "Справочник"
        @dp.message(lambda message: message.text == "Справочник")
        async def handle_handbook(message: types.Message):
            user_id = message.from_user.id
            logger.info(f"USER ACTION: user_id={user_id}, action=handbook_button, data=None")
            
            await message.answer("🌐 WebView: Справочник (мок)\n\n📚 Здесь будет открываться справочник по соционике в WebView.")
        
        # Обработчик кнопки "Тесты (сайт)"
        @dp.message(lambda message: message.text == "Тесты (сайт)")
        async def handle_tests_site(message: types.Message):
            user_id = message.from_user.id
            logger.info(f"USER ACTION: user_id={user_id}, action=tests_site_button, data=None")
            
            tests_text = "📝 Список доступных тестов:\n\n"
            for test in MOCK_TESTS:
                tests_text += f"🔸 {test['name']}\n"
                tests_text += f"   {test['description']}\n\n"
            
            tests_text += "🌐 WebView: Тесты (мок)"
            
            await message.answer(tests_text)
        
        # Обработчик кнопки "Наш тест"
        @dp.message(lambda message: message.text == "Наш тест")
        async def handle_our_test(message: types.Message):
            user_id = message.from_user.id
            logger.info(f"USER ACTION: user_id={user_id}, action=our_test_button, data=None")
            
            # Начинаем тест
            test_text = "🧠 Наш тест на определение типа личности!\n\n"
            test_text += "📋 Вопросы:\n\n"
            
            for i, question in enumerate(MOCK_QUESTIONS, 1):
                test_text += f"{i}. {question['question']}\n"
                for j, answer in enumerate(question['answers']):
                    test_text += f"   {chr(65+j)}) {answer}\n"
                test_text += "\n"
            
            # Мок-результат
            result_text = "🎯 Результаты теста (мок):\n\n"
            result_text += "📊 Гипотеза 1: Аналитик (INTJ) - 85%\n"
            result_text += "   • Квадра: Альфа\n"
            result_text += "   • Роль: Исследователь\n\n"
            result_text += "📊 Гипотеза 2: Дипломат (INFJ) - 15%\n"
            result_text += "   • Квадра: Бета\n"
            result_text += "   • Роль: Наставник"
            
            await message.answer(test_text + "\n" + result_text)
        
        # Обработчик кнопки "Консультация"
        @dp.message(lambda message: message.text == "Консультация")
        async def handle_consultation(message: types.Message):
            user_id = message.from_user.id
            logger.info(f"USER ACTION: user_id={user_id}, action=consultation_button, data=None")
            
            # Выбираем случайный ответ
            random_answer = random.choice(MOCK_CONSULT_ANSWERS)
            
            consultation_text = f"💬 ИИ-Консультация (мок)\n\n"
            consultation_text += f"🤖 {random_answer}\n\n"
            consultation_text += "💡 Это мок-ответ. В реальном режиме здесь был бы ответ от OpenAI."
            
            await message.answer(consultation_text)
        
        # Обработчик кнопки "ИИ-Определение"
        @dp.message(lambda message: message.text == "ИИ-Определение")
        async def handle_ai_analysis(message: types.Message):
            user_id = message.from_user.id
            logger.info(f"USER ACTION: user_id={user_id}, action=ai_analysis_button, data=None")
            
            ai_text = "🔍 ИИ-Определение типа личности (мок)\n\n"
            ai_text += "✅ Анализ фото выполнен успешно (мок)\n\n"
            ai_text += "📊 Результаты:\n"
            ai_text += "• Тип личности: Аналитик (INTJ)\n"
            ai_text += "• Квадра: Альфа\n"
            ai_text += "• Роль: Исследователь\n"
            ai_text += "• Уверенность: 95%\n\n"
            ai_text += "💡 В реальном режиме здесь был бы анализ через InsightFace + GPT Vision."
            
            await message.answer(ai_text)
        
        # Обработчик кнопки "Подписка"
        @dp.message(lambda message: message.text == "Подписка")
        async def handle_subscription(message: types.Message):
            user_id = message.from_user.id
            logger.info(f"USER ACTION: user_id={user_id}, action=subscription_button, data=None")
            
            await message.answer("💳 WebView: Подписка (мок)\n\n🔐 Здесь будет открываться страница подписки в WebView.")
        
        # Обработчик кнопки "Пакеты"
        @dp.message(lambda message: message.text == "Пакеты")
        async def handle_packages(message: types.Message):
            user_id = message.from_user.id
            logger.info(f"USER ACTION: user_id={user_id}, action=packages_button, data=None")
            
            await message.answer("📦 WebView: Пакеты (мок)\n\n🎁 Здесь будет открываться страница пакетов в WebView.")
        
        # Обработчик кнопки "Курсы"
        @dp.message(lambda message: message.text == "Курсы")
        async def handle_courses(message: types.Message):
            user_id = message.from_user.id
            logger.info(f"USER ACTION: user_id={user_id}, action=courses_button, data=None")
            
            await message.answer("📚 WebView: Курсы (мок)\n\n🎓 Здесь будет открываться страница курсов в WebView.")
        
        # Обработчик кнопки "Карты"
        @dp.message(lambda message: message.text == "Карты")
        async def handle_cards(message: types.Message):
            user_id = message.from_user.id
            logger.info(f"USER ACTION: user_id={user_id}, action=cards_button, data=None")
            
            await message.answer("🃏 WebView: Карты (мок)\n\n🎴 Здесь будет открываться страница карт в WebView.")
        
        # Обработчик всех остальных сообщений
        @dp.message()
        async def handle_any_message(message: types.Message):
            user_id = message.from_user.id
            text = message.text or "без текста"
            logger.info(f"USER ACTION: user_id={user_id}, action=any_message, data=text={text}")
            
            await message.answer("❓ Неизвестная команда. Используйте кнопки меню или команду /start")
        
        logger.info("✅ Бот готов к работе!")
        logger.info("📱 Откройте Telegram и найдите вашего бота")
        logger.info("🔍 Все действия пользователей будут логироваться в консоль")
        logger.info("⏹️  Для остановки нажмите Ctrl+C")
        
        # Запускаем бота в режиме polling
        await dp.start_polling(bot)
        
    except KeyboardInterrupt:
        logger.info("🛑 Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"❌ Ошибка запуска: {e}")
        raise

if __name__ == "__main__":
    # Запускаем асинхронную функцию
    asyncio.run(main())
