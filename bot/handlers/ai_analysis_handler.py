"""Обработчик ИИ-анализа."""

from typing import Dict, Any
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from .base import BaseHandler
from bot.data.messages import PREMIUM_MESSAGES, ERROR_MESSAGES
from bot.data.keyboards import get_back_keyboard
from bot.services.ai_service import ai_service


class AIAnalysisHandler(BaseHandler):
    """Обработчик ИИ-анализа."""
    
    def __init__(self, router: Router):
        """Инициализация обработчика."""
        super().__init__(router)
        self.user_states: Dict[int, Dict[str, Any]] = {}  # user_id -> state
    
    def _setup_handlers(self):
        """Настройка обработчиков."""
        # Выбор типа медиа
        self.router.callback_query.register(
            self._handle_media_type_selection,
            F.data.startswith("ai_")
        )
        
        # Обработка медиа файлов
        self.router.message.register(
            self._handle_photo,
            F.photo
        )
        
        self.router.message.register(
            self._handle_video,
            F.video
        )
        
        self.router.message.register(
            self._handle_voice,
            F.voice
        )
    
    async def _handle_media_type_selection(self, callback: CallbackQuery):
        """Обработка выбора типа медиа."""
        try:
            user_id = await self._get_or_create_user(callback.message)
            data = callback.data
            
            if data == "ai_photo":
                media_type = "photo"
                message = PREMIUM_MESSAGES["ai_analysis_photo"]
            elif data == "ai_video":
                media_type = "video"
                message = PREMIUM_MESSAGES["ai_analysis_video"]
            elif data == "ai_voice":
                media_type = "voice"
                message = PREMIUM_MESSAGES["ai_analysis_voice"]
            else:
                await self._handle_callback_error(callback, "general")
                return
            
            # Сохраняем состояние пользователя
            self.user_states[user_id] = {
                "waiting_for_media": True,
                "media_type": media_type
            }
            
            await callback.message.edit_text(
                message,
                reply_markup=get_back_keyboard()
            )
            await callback.answer()
            
        except Exception as e:
            await self._handle_callback_error(callback, "general")
    
    async def _handle_photo(self, message: Message):
        """Обработка фото."""
        try:
            user_id = await self._get_or_create_user(message)
            
            # Проверяем, ждет ли пользователь фото
            if user_id not in self.user_states or not self.user_states[user_id].get("waiting_for_media"):
                return
            
            state = self.user_states[user_id]
            if state["media_type"] != "photo":
                return
            
            await self._process_media(message, user_id, "photo")
            
        except Exception as e:
            await self._handle_error(message, "general")
    
    async def _handle_video(self, message: Message):
        """Обработка видео."""
        try:
            user_id = await self._get_or_create_user(message)
            
            # Проверяем, ждет ли пользователь видео
            if user_id not in self.user_states or not self.user_states[user_id].get("waiting_for_media"):
                return
            
            state = self.user_states[user_id]
            if state["media_type"] != "video":
                return
            
            await self._process_media(message, user_id, "video")
            
        except Exception as e:
            await self._handle_error(message, "general")
    
    async def _handle_voice(self, message: Message):
        """Обработка голосового сообщения."""
        try:
            user_id = await self._get_or_create_user(message)
            
            # Проверяем, ждет ли пользователь голос
            if user_id not in self.user_states or not self.user_states[user_id].get("waiting_for_media"):
                return
            
            state = self.user_states[user_id]
            if state["media_type"] != "voice":
                return
            
            await self._process_media(message, user_id, "voice")
            
        except Exception as e:
            await self._handle_error(message, "general")
    
    async def _process_media(self, message: Message, user_id: int, media_type: str):
        """Обработка медиа файла."""
        try:
            # Логируем действие
            await self._log_user_action(user_id, f"ai_analysis_{media_type}_uploaded")
            
            # Показываем сообщение о обработке
            processing_msg = await message.answer(
                PREMIUM_MESSAGES["ai_analysis_processing"]
            )
            
            # Получаем file_id
            if media_type == "photo":
                file_id = message.photo[-1].file_id
            elif media_type == "video":
                file_id = message.video.file_id
            elif media_type == "voice":
                file_id = message.voice.file_id
            else:
                await processing_msg.edit_text(ERROR_MESSAGES["invalid_media"])
                return
            
            # Анализируем медиа
            result = await ai_service.analyze_media(
                user_id=user_id,
                file_id=file_id,
                media_type=media_type
            )
            
            # Удаляем сообщение о обработке
            await processing_msg.delete()
            
            # Показываем результат
            if result.get("status") == "success":
                analysis_text = PREMIUM_MESSAGES["ai_analysis_result"].format(
                    result=result.get("analysis", "Анализ недоступен")
                )
                
                await message.answer(
                    analysis_text,
                    reply_markup=get_back_keyboard()
                )
            else:
                await message.answer(
                    ERROR_MESSAGES["processing_failed"],
                    reply_markup=get_back_keyboard()
                )
            
            # Очищаем состояние пользователя
            if user_id in self.user_states:
                del self.user_states[user_id]
            
        except Exception as e:
            await self._handle_error(message, "general")
            # Очищаем состояние пользователя в случае ошибки
            if user_id in self.user_states:
                del self.user_states[user_id]


# Создание экземпляра обработчика
ai_analysis_handler = AIAnalysisHandler(Router())
