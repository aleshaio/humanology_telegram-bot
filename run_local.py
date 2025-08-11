#!/usr/bin/env python3
"""
Локальный режим отладки Telegram-бота

Запуск: python run_local.py

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

MOCK_AI_RESPONSES = [
    "Спасибо за ваш вопрос! Я проанализирую ситуацию и дам рекомендации.",
    "Интересный вопрос. Позвольте мне подумать об этом с точки зрения психологии.",
    "Это очень важная тема. Давайте разберем её пошагово.",
    "Отличный вопрос! У меня есть несколько идей по этому поводу.",
    "Спасибо, что обратились за консультацией. Я готов помочь вам разобраться в этом вопросе.",
    "Это интересная проблема. Позвольте мне предложить несколько решений.",
    "Я понимаю вашу ситуацию. Давайте вместе найдем оптимальное решение.",
    "Спасибо за доверие. Я постараюсь дать максимально полезный совет."
]

# Мок-конфигурация
class MockSettings:
    """Мок-настройки для локального режима."""
    
    def __init__(self):
        # Обязательный токен бота
        self.bot_token = os.getenv("BOT_TOKEN")
        if not self.bot_token:
            raise ValueError("BOT_TOKEN обязателен для работы бота!")
        
        # Остальные настройки - заглушки
        self.webhook_url = "http://localhost:8000"
        self.webhook_path = "/webhook"
        self.db_dsn = "postgresql://user:pass@localhost:5432/bot_db"
        self.site_api_url = "https://example.com/api"
        self.site_api_key = "mock_api_key"
        self.openai_api_key = "mock_openai_key"
        self.storage_path = "./storage"
        self.free_consultation_limit = 5
        self.host = "0.0.0.0"
        self.port = 8000
        self.debug = True

# Мок-сервис для работы с API сайта
class MockSiteAPIService:
    """Мок-сервис для работы с API сайта."""
    
    async def get_tests_list(self):
        """Возвращает список из 4 фиктивных тестов."""
        logger.info("Mock: get_tests_list() вызван")
        return MOCK_TESTS
    
    async def get_test_questions(self, test_id: int):
        """Возвращает фиктивные вопросы для теста."""
        logger.info(f"Mock: get_test_questions({test_id}) вызван")
        return MOCK_QUESTIONS
    
    async def submit_test_result(self, test_id: int, user_id: int, answers: list):
        """Мок-отправка результатов теста."""
        logger.info(f"Mock: submit_test_result({test_id}, {user_id}, {answers})")
        return {"success": True, "message": "Результаты сохранены"}
    
    async def check_subscription_status(self, telegram_user_id: int):
        """Всегда возвращает True для подписки."""
        logger.info(f"Mock: check_subscription_status({telegram_user_id}) - всегда True")
        return {"active": True, "expires_at": "2025-12-31"}
    
    async def check_package_balance(self, telegram_user_id: int):
        """Всегда возвращает 999 для баланса пакетов."""
        logger.info(f"Mock: check_package_balance({telegram_user_id}) - всегда 999")
        return {"balance": 999, "packages": ["premium", "vip"]}
    
    async def get_user_profile(self, telegram_user_id: int):
        """Возвращает пустой фиктивный профиль."""
        logger.info(f"Mock: get_user_profile({telegram_user_id}) - пустой профиль")
        return {"id": telegram_user_id, "name": "", "email": "", "phone": ""}
    
    async def is_api_available(self):
        """Всегда возвращает True."""
        return True
    
    def get_webview_url(self, section: str, user_id: int = None):
        """Возвращает фиктивные URL для WebView."""
        base_url = "https://example.com"
        if section == "handbook":
            return f"{base_url}/handbook?user_id={user_id}"
        elif section == "tests":
            return f"{base_url}/tests?user_id={user_id}"
        elif section == "subscription":
            return f"{base_url}/subscription?user_id={user_id}"
        elif section == "packages":
            return f"{base_url}/packages?user_id={user_id}"
        elif section == "courses":
            return f"{base_url}/courses?user_id={user_id}"
        elif section == "cards":
            return f"{base_url}/cards?user_id={user_id}"
        else:
            return f"{base_url}/?user_id={user_id}"

# Мок-сервис для ИИ-анализа
class MockAIService:
    """Мок-сервис для ИИ-анализа."""
    
    async def analyze_media(self, user_id: int, file_id: str, media_type: str):
        """Всегда возвращает фиктивный отчёт."""
        logger.info(f"Mock: analyze_media({user_id}, {file_id}, {media_type})")
        return {
            "type": media_type,
            "analysis": "Анализ выполнен успешно. Определен тип личности: Аналитик (INTJ). Квадра: Альфа. Роль: Исследователь.",
            "model": "mock_ai_model",
            "status": "success",
            "confidence": 0.95
        }
    
    async def analyze_photo(self, file_path: str):
        """Мок-анализ фото."""
        return {
            "type": "photo",
            "analysis": "Анализ фото: определен тип личности Аналитик (INTJ)",
            "model": "mock_vision",
            "status": "success"
        }
    
    async def analyze_video(self, file_path: str):
        """Мок-анализ видео."""
        return {
            "type": "video",
            "analysis": "Анализ видео: определен тип личности Аналитик (INTJ)",
            "model": "mock_vision",
            "status": "success"
        }
    
    async def analyze_voice(self, file_path: str):
        """Мок-анализ голоса."""
        return {
            "type": "voice",
            "analysis": "Анализ голоса: определен тип личности Аналитик (INTJ)",
            "model": "mock_whisper",
            "status": "success"
        }
    
    async def save_media_file(self, file_id: str, media_type: str):
        """Мок-сохранение медиа файла."""
        return f"/tmp/mock_{file_id}_{media_type}.tmp"
    
    async def cleanup_temp_file(self, file_path: str):
        """Мок-очистка временного файла."""
        logger.info(f"Mock: cleanup_temp_file({file_path})")

# Мок-сервис для консультаций
class MockConsultationService:
    """Мок-сервис для консультаций."""
    
    def __init__(self):
        self.free_limit = 5
    
    async def check_user_limit(self, user_id: int):
        """Всегда разрешает консультации."""
        logger.info(f"Mock: check_user_limit({user_id}) - всегда разрешено")
        return {
            "can_consult": True,
            "remaining_messages": 999,
            "is_first_time": False
        }
    
    async def start_consultation(self, user_id: int):
        """Мок-начало консультации."""
        logger.info(f"Mock: start_consultation({user_id})")
        return {
            "success": True,
            "message": "Консультация начата",
            "remaining_messages": 999,
            "consultation_id": 12345
        }
    
    async def send_message(self, user_id: int, message: str):
        """Возвращает случайный предопределенный ответ."""
        logger.info(f"Mock: send_message({user_id}, '{message}')")
        response = random.choice(MOCK_AI_RESPONSES)
        return {
            "success": True,
            "ai_response": response,
            "remaining_messages": 999
        }
    
    async def end_consultation(self, user_id: int):
        """Мок-завершение консультации."""
        logger.info(f"Mock: end_consultation({user_id})")
        return True
    
    def get_consultation_welcome_message(self, remaining_messages: int):
        """Приветственное сообщение для консультации."""
        return f"💬 Добро пожаловать в консультацию с ИИ! У вас {remaining_messages} бесплатных сообщений в месяц."
    
    def get_limit_reached_message(self):
        """Сообщение о достижении лимита."""
        return f"❌ Достигнут лимит бесплатных консультаций ({self.free_limit} в месяц). Для продолжения оформите подписку."

# Мок-база данных
class MockDatabase:
    """Мок-база данных для локального режима."""
    
    async def create_tables(self):
        """Мок-создание таблиц."""
        logger.info("Mock: create_tables() - таблицы созданы")
        return True
    
    async def get_or_create_user(self, user_id: int, username: str = None, first_name: str = None):
        """Мок-создание/получение пользователя."""
        logger.info(f"Mock: get_or_create_user({user_id}, {username}, {first_name})")
        return {"id": user_id, "username": username, "first_name": first_name}
    
    async def log_user_action(self, user_id: int, action: str, data: dict = None):
        """Логирование действий пользователя в консоль."""
        logger.info(f"USER ACTION: user_id={user_id}, action={action}, data={data}")
    
    async def save_test_result(self, user_id: int, test_type: str, result_data: dict):
        """Мок-сохранение результатов теста."""
        logger.info(f"Mock: save_test_result({user_id}, {test_type}, {result_data})")
        return True
    
    async def get_user_premium_access(self, user_id: int):
        """Всегда возвращает премиум-доступ."""
        logger.info(f"Mock: get_user_premium_access({user_id}) - всегда премиум")
        return {"has_access": True, "expires_at": "2025-12-31"}
    
    async def check_subscription_status(self, user_id: int):
        """Всегда возвращает активную подписку."""
        logger.info(f"Mock: check_subscription_status({user_id}) - всегда активно")
        return {"active": True, "expires_at": "2025-12-31"}
    
    async def check_package_balance(self, user_id: int):
        """Всегда возвращает баланс 999."""
        logger.info(f"Mock: check_package_balance({user_id}) - всегда 999")
        return {"balance": 999, "packages": ["premium", "vip"]}
    
    async def get_consultation_info(self, user_id: int):
        """Мок-информация о консультации."""
        return {"id": 12345, "user_id": user_id, "message_count": 0}
    
    async def create_or_update_consultation(self, user_id: int, message_count: int):
        """Мок-создание/обновление консультации."""
        return {"id": 12345, "user_id": user_id, "message_count": message_count}
    
    async def save_ai_analysis(self, user_id: int, media_type: str, file_id: str, analysis_result: dict):
        """Мок-сохранение ИИ-анализа."""
        logger.info(f"Mock: save_ai_analysis({user_id}, {media_type}, {file_id}, {analysis_result})")
        return True
    
    async def close(self):
        """Мок-закрытие соединения."""
        logger.info("Mock: close() - соединение закрыто")

# Мок-тестовый сервис
class MockTestService:
    """Мок-сервис для тестов."""
    
    def __init__(self):
        self.test_data = {
            "questions": MOCK_QUESTIONS,
            "types": {
                "Аналитик": {
                    "description": "Логичный и аналитичный тип",
                    "square": "Альфа",
                    "role": "Исследователь"
                },
                "Дипломат": {
                    "description": "Эмпатичный и творческий тип",
                    "square": "Бета",
                    "role": "Наставник"
                }
            }
        }
    
    def get_question(self, question_id: int):
        """Получение вопроса по ID."""
        if 1 <= question_id <= len(self.test_data["questions"]):
            return self.test_data["questions"][question_id - 1]
        return None
    
    def get_total_questions(self):
        """Общее количество вопросов."""
        return len(self.test_data["questions"])
    
    def calculate_test_result(self, answers: list):
        """Расчет результатов теста."""
        logger.info(f"Mock: calculate_test_result({answers})")
        return {
            "type_name": "Аналитик",
            "type_percent": 85,
            "square": "Альфа",
            "role": "Исследователь",
            "description": "Вы относитесь к типу Аналитик",
            "all_scores": {"Аналитик": 3, "Дипломат": 1, "Прагматик": 0, "Социал": 0}
        }
    
    async def save_test_result(self, user_id: int, answers: list, result: dict):
        """Мок-сохранение результатов теста."""
        logger.info(f"Mock: save_test_result({user_id}, {answers}, {result})")
        return True
    
    def get_test_progress_text(self, current: int, total: int):
        """Текст прогресса теста."""
        return f"Вопрос {current} из {total}"
    
    def get_test_welcome_text(self):
        """Приветственный текст для теста."""
        return "Добро пожаловать в наш тест! Ответьте на 4 вопроса для определения типа личности."
    
    def get_test_completion_text(self, result: dict):
        """Текст завершения теста."""
        return f"Тест завершен! Ваш тип: {result['type_name']} ({result['type_percent']}%)"

async def main():
    """Основная функция запуска."""
    try:
        # Проверяем токен бота
        if not os.getenv("BOT_TOKEN"):
            logger.error("Ошибка: BOT_TOKEN не найден в переменных окружения!")
            logger.error("Создайте файл .env с вашим токеном бота от @BotFather")
            logger.error("Пример: cp env.local.example .env")
            return
        
        logger.info("🚀 Запуск бота в локальном режиме отладки...")
        
        # Создаем мок-объекты
        mock_settings = MockSettings()
        mock_db = MockDatabase()
        mock_site_api = MockSiteAPIService()
        mock_ai_service = MockAIService()
        mock_consultation = MockConsultationService()
        mock_test_service = MockTestService()
        
        # Заменяем глобальные экземпляры сервисов на моки
        import bot.services.site_api_service
        import bot.services.ai_service
        import bot.services.consultation_service
        import bot.services.test_service
        import bot.database.database
        
        # Заменяем сервисы
        bot.services.site_api_service.site_api_service = mock_site_api
        bot.services.ai_service.ai_service = mock_ai_service
        bot.services.consultation_service.consultation_service = mock_consultation
        bot.services.test_service.test_service = mock_test_service
        bot.database.database.db = mock_db
        
        # Импортируем основные модули бота
        from bot.bot import TelegramBot
        
        # Создаем экземпляр бота
        bot = TelegramBot()
        
        # Создаем таблицы (мок)
        await mock_db.create_tables()
        
        logger.info("✅ Бот готов к работе!")
        logger.info("📱 Откройте Telegram и найдите вашего бота")
        logger.info("🔍 Все действия пользователей будут логироваться в консоль")
        logger.info("⏹️  Для остановки нажмите Ctrl+C")
        
        # Запускаем бота в режиме polling
        await bot.dp.start_polling(bot.bot)
        
    except KeyboardInterrupt:
        logger.info("🛑 Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"❌ Ошибка запуска: {e}")
        raise

if __name__ == "__main__":
    # Запускаем асинхронную функцию
    asyncio.run(main())
