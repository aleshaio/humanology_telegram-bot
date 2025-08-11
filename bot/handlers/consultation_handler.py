"""Обработчик консультаций."""

from typing import Dict, Any
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from .base import BaseHandler
from bot.data.messages import FREE_ZONE_MESSAGES, ERROR_MESSAGES
from bot.data.keyboards import get_back_keyboard
from bot.services.consultation_service import consultation_service


class ConsultationStates(StatesGroup):
    """Состояния консультации."""
    waiting_for_message = State()


class ConsultationHandler(BaseHandler):
    """Обработчик консультаций."""
    
    def __init__(self, router: Router):
        """Инициализация обработчика."""
        super().__init__(router)
        self.active_consultations: Dict[int, bool] = {}  # user_id -> is_active
    
    def _setup_handlers(self):
        """Настройка обработчиков."""
        # Начало консультации
        self.router.callback_query.register(
            self._handle_start_consultation,
            F.data == "start_consultation"
        )
        
        # Сообщения в консультации
        self.router.message.register(
            self._handle_consultation_message,
            F.text,
            ConsultationStates.waiting_for_message
        )
        
        # Завершение консультации
        self.router.callback_query.register(
            self._handle_end_consultation,
            F.data == "end_consultation"
        )
    
    async def _handle_start_consultation(self, callback: CallbackQuery, state: FSMContext):
        """Начало консультации."""
        try:
            user_id = await self._get_or_create_user(callback.message)
            
            # Проверяем лимит
            limit_check = await consultation_service.check_user_limit(user_id)
            
            if not limit_check["can_consult"]:
                await callback.message.edit_text(
                    consultation_service.get_limit_reached_message(),
                    reply_markup=get_back_keyboard()
                )
                await callback.answer()
                return
            
            # Начинаем консультацию
            result = await consultation_service.start_consultation(user_id)
            
            if result["success"]:
                # Активируем консультацию
                self.active_consultations[user_id] = True
                
                # Переходим в состояние ожидания сообщения
                await state.set_state(ConsultationStates.waiting_for_message)
                
                # Показываем приветственное сообщение
                welcome_text = consultation_service.get_consultation_welcome_message(
                    limit_check["remaining_messages"]
                )
                
                await callback.message.edit_text(
                    f"{welcome_text}\n\n💬 Отправьте ваш вопрос:",
                    reply_markup=get_back_keyboard()
                )
                
                await self._log_user_action(user_id, "consultation_started")
            else:
                await callback.message.edit_text(
                    result["message"],
                    reply_markup=get_back_keyboard()
                )
            
            await callback.answer()
            
        except Exception as e:
            await self._handle_callback_error(callback, "general")
    
    async def _handle_consultation_message(self, message: Message, state: FSMContext):
        """Обработка сообщения в консультации."""
        try:
            user_id = await self._get_or_create_user(message)
            
            # Проверяем, активна ли консультация
            if user_id not in self.active_consultations or not self.active_consultations[user_id]:
                return
            
            # Логируем сообщение
            await self._log_user_action(user_id, "consultation_message_sent", message.text)
            
            # Показываем индикатор набора
            await message.answer("🤖 ИИ печатает...")
            
            # Отправляем сообщение в OpenAI
            result = await consultation_service.send_message(user_id, message.text)
            
            if result["success"]:
                # Показываем ответ ИИ
                ai_response = result["ai_response"]
                remaining = result["remaining_messages"]
                
                response_text = f"🤖 {ai_response}\n\n💬 Осталось сообщений: {remaining}"
                
                await message.answer(response_text)
                
                # Если достигнут лимит, завершаем консультацию
                if remaining <= 0:
                    await self._end_consultation(user_id, state)
                    await message.answer(
                        "❌ Достигнут лимит сообщений. Консультация завершена.",
                        reply_markup=get_back_keyboard()
                    )
            else:
                await message.answer(
                    result["message"],
                    reply_markup=get_back_keyboard()
                )
                await self._end_consultation(user_id, state)
            
        except Exception as e:
            await self._handle_error(message, "general")
            await self._end_consultation(user_id, state)
    
    async def _handle_end_consultation(self, callback: CallbackQuery, state: FSMContext):
        """Завершение консультации."""
        try:
            user_id = await self._get_or_create_user(callback.message)
            
            await self._end_consultation(user_id, state)
            
            await callback.message.edit_text(
                "💬 Консультация завершена. Спасибо за обращение!",
                reply_markup=get_back_keyboard()
            )
            
            await callback.answer()
            
        except Exception as e:
            await self._handle_callback_error(callback, "general")
    
    async def _end_consultation(self, user_id: int, state: FSMContext):
        """Внутреннее завершение консультации."""
        try:
            # Завершаем консультацию в сервисе
            await consultation_service.end_consultation(user_id)
            
            # Деактивируем консультацию
            if user_id in self.active_consultations:
                del self.active_consultations[user_id]
            
            # Сбрасываем состояние
            await state.clear()
            
            # Логируем завершение
            await self._log_user_action(user_id, "consultation_ended")
            
        except Exception as e:
            print(f"Ошибка завершения консультации: {e}")


# Создание экземпляра обработчика
consultation_handler = ConsultationHandler(Router())
