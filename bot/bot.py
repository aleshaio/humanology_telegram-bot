"""Основной файл бота."""

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from config import settings
from bot.database.database import db
from bot.handlers.main_menu import main_menu_handler
from bot.handlers.test_handler import test_handler
from bot.handlers.ai_analysis_handler import ai_analysis_handler
from bot.handlers.consultation_handler import consultation_handler


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class TelegramBot:
    """Основной класс бота."""
    
    def __init__(self):
        """Инициализация бота."""
        self.bot = Bot(token=settings.bot_token)
        self.dp = Dispatcher()
        
        # Регистрируем обработчики
        self._setup_handlers()
        
        # Настройка webhook
        self.webhook_url = f"{settings.webhook_url}{settings.webhook_path}"
    
    def _setup_handlers(self):
        """Настройка всех обработчиков."""
        # Главное меню
        self.dp.include_router(main_menu_handler.router)
        
        # Тесты
        self.dp.include_router(test_handler.router)
        
        # ИИ-анализ
        self.dp.include_router(ai_analysis_handler.router)
        
        # Консультации
        self.dp.include_router(consultation_handler.router)
    
    async def on_startup(self, app: web.Application):
        """Действия при запуске."""
        logger.info("Запуск бота...")
        
        # Создаем таблицы БД
        try:
            await db.create_tables()
            logger.info("Таблицы БД созданы/проверены")
        except Exception as e:
            logger.error(f"Ошибка создания таблиц БД: {e}")
        
        # Устанавливаем webhook
        try:
            await self.bot.set_webhook(
                url=self.webhook_url,
                drop_pending_updates=True
            )
            logger.info(f"Webhook установлен: {self.webhook_url}")
        except Exception as e:
            logger.error(f"Ошибка установки webhook: {e}")
    
    async def on_shutdown(self, app: web.Application):
        """Действия при остановке."""
        logger.info("Остановка бота...")
        
        # Удаляем webhook
        try:
            await self.bot.delete_webhook()
            logger.info("Webhook удален")
        except Exception as e:
            logger.error(f"Ошибка удаления webhook: {e}")
        
        # Закрываем соединение с БД
        try:
            await db.close()
            logger.info("Соединение с БД закрыто")
        except Exception as e:
            logger.error(f"Ошибка закрытия БД: {e}")
        
        # Закрываем сессию бота
        try:
            await self.bot.session.close()
            logger.info("Сессия бота закрыта")
        except Exception as e:
            logger.error(f"Ошибка закрытия сессии бота: {e}")
    
    async def get_webhook_handler(self) -> SimpleRequestHandler:
        """Получение обработчика webhook."""
        return SimpleRequestHandler(
            dispatcher=self.dp,
            bot=self.bot
        )


# Создание экземпляра бота
telegram_bot = TelegramBot()


async def get_bot() -> TelegramBot:
    """Получение экземпляра бота."""
    return telegram_bot
