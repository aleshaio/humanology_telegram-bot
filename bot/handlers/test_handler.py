"""Обработчик тестов."""

from typing import Dict, Any
from aiogram import Router, F
from aiogram.types import CallbackQuery

from .base import BaseHandler
from bot.data.messages import FREE_ZONE_MESSAGES, TEST_MESSAGES
from bot.data.keyboards import get_test_answer_keyboard, get_back_keyboard
from bot.services.test_service import test_service


class TestHandler(BaseHandler):
    """Обработчик тестов."""
    
    def __init__(self, router: Router):
        """Инициализация обработчика."""
        super().__init__(router)
        self.user_tests: Dict[int, Dict[str, Any]] = {}  # user_id -> test_state
    
    def _setup_handlers(self):
        """Настройка обработчиков."""
        # Ответы на вопросы теста
        self.router.callback_query.register(
            self._handle_test_answer,
            F.data.startswith("test_answer:")
        )
        
        # Начало теста
        self.router.callback_query.register(
            self._handle_start_test,
            F.data == "start_test"
        )
    
    async def start_test(self, callback: CallbackQuery):
        """Начало теста."""
        try:
            user_id = await self._get_or_create_user(callback.message)
            
            # Инициализируем состояние теста
            self.user_tests[user_id] = {
                "current_question": 1,
                "answers": [],
                "total_questions": test_service.get_total_questions()
            }
            
            await self._show_question(callback, user_id)
            
        except Exception as e:
            await self._handle_callback_error(callback, "general")
    
    async def _handle_start_test(self, callback: CallbackQuery):
        """Обработка кнопки начала теста."""
        try:
            user_id = await self._get_or_create_user(callback.message)
            await self._log_user_action(user_id, "test_started")
            
            # Инициализируем состояние теста
            self.user_tests[user_id] = {
                "current_question": 1,
                "answers": [],
                "total_questions": test_service.get_total_questions()
            }
            
            await self._show_question(callback, user_id)
            
        except Exception as e:
            await self._handle_callback_error(callback, "general")
    
    async def _handle_test_answer(self, callback: CallbackQuery):
        """Обработка ответа на вопрос теста."""
        try:
            user_id = await self._get_or_create_user(callback.message)
            
            # Парсим данные callback
            data = callback.data.split(":")
            question_id = int(data[1])
            answer_index = int(data[2])
            
            # Сохраняем ответ
            if user_id in self.user_tests:
                test_state = self.user_tests[user_id]
                test_state["answers"].append(answer_index)
                
                # Переходим к следующему вопросу или завершаем тест
                if test_state["current_question"] < test_state["total_questions"]:
                    test_state["current_question"] += 1
                    await self._show_question(callback, user_id)
                else:
                    await self._complete_test(callback, user_id)
            
            await callback.answer()
            
        except Exception as e:
            await self._handle_callback_error(callback, "general")
    
    async def _show_question(self, callback: CallbackQuery, user_id: int):
        """Показ вопроса теста."""
        try:
            test_state = self.user_tests[user_id]
            current_question = test_state["current_question"]
            
            # Получаем вопрос
            question_data = test_service.get_question(current_question)
            if not question_data:
                await self._handle_callback_error(callback, "general")
                return
            
            # Формируем текст вопроса
            question_text = FREE_ZONE_MESSAGES["test_question"].format(
                current=current_question,
                total=test_state["total_questions"],
                question=question_data["question"]
            )
            
            # Создаем клавиатуру с вариантами ответов
            keyboard = get_test_answer_keyboard(
                question_data["answers"], 
                current_question
            )
            
            # Обновляем сообщение
            await callback.message.edit_text(
                question_text,
                reply_markup=keyboard
            )
            
        except Exception as e:
            await self._handle_callback_error(callback, "general")
    
    async def _complete_test(self, callback: CallbackQuery, user_id: int):
        """Завершение теста."""
        try:
            test_state = self.user_tests[user_id]
            
            # Показываем сообщение о завершении
            await callback.message.edit_text(
                FREE_ZONE_MESSAGES["test_complete"],
                reply_markup=get_back_keyboard()
            )
            
            # Рассчитываем результат
            result = test_service.calculate_test_result(test_state["answers"])
            
            # Сохраняем результат в БД
            await test_service.save_test_result(
                user_id=user_id,
                answers=test_state["answers"],
                result=result
            )
            
            # Логируем завершение теста
            await self._log_user_action(
                user_id, 
                "test_completed", 
                f"Result: {result.get('type_name', 'Unknown')}"
            )
            
            # Показываем результат
            result_text = FREE_ZONE_MESSAGES["test_result"].format(
                type_name=result.get("type_name", "Не определено"),
                type_percent=result.get("type_percent", 0),
                square=result.get("square", "Не определено"),
                role=result.get("role", "Не определено")
            )
            
            await callback.message.answer(
                result_text,
                reply_markup=get_back_keyboard()
            )
            
            # Очищаем состояние теста
            if user_id in self.user_tests:
                del self.user_tests[user_id]
            
        except Exception as e:
            await self._handle_callback_error(callback, "general")


# Создание экземпляра обработчика
test_handler = TestHandler(Router())
