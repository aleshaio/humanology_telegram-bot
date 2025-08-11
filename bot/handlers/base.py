"""Базовый обработчик для бота."""

from typing import Any, Dict, Optional
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from bot.database.database import db
from bot.data.messages import ERROR_MESSAGES


class BaseHandler:
    """Базовый класс для всех обработчиков."""
    
    def __init__(self, router: Router):
        """Инициализация обработчика."""
        self.router = router
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Настройка обработчиков. Переопределяется в наследниках."""
        pass
    
    async def _get_or_create_user(self, message: Message) -> int:
        """Получение или создание пользователя в БД."""
        try:
            user = await db.get_or_create_user(
                telegram_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name
            )
            return user.id
        except Exception as e:
            print(f"Ошибка получения пользователя: {e}")
            return 0
    
    async def _log_user_action(
        self, 
        user_id: int, 
        action: str, 
        details: Optional[str] = None
    ):
        """Логирование действия пользователя."""
        try:
            await db.log_user_action(user_id, action, details)
        except Exception as e:
            print(f"Ошибка логирования: {e}")
    
    async def _handle_error(
        self, 
        message: Message, 
        error: str = "general"
    ):
        """Обработка ошибок."""
        error_text = ERROR_MESSAGES.get(error, ERROR_MESSAGES["general"])
        await message.answer(error_text)
    
    async def _handle_callback_error(
        self, 
        callback: CallbackQuery, 
        error: str = "general"
    ):
        """Обработка ошибок в callback."""
        error_text = ERROR_MESSAGES.get(error, ERROR_MESSAGES["general"])
        await callback.answer(error_text, show_alert=True)
