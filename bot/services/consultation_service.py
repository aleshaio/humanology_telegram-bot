"""Сервис для работы с консультациями."""

import asyncio
from typing import Dict, Any, Optional
from openai import AsyncOpenAI

from config import settings
from bot.database.database import db


class ConsultationService:
    """Сервис для работы с консультациями."""
    
    def __init__(self):
        """Инициализация сервиса."""
        self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.free_limit = settings.free_consultation_limit
    
    async def check_user_limit(self, user_id: int) -> Dict[str, Any]:
        """Проверка лимита консультаций пользователя."""
        try:
            consultation = await db.get_consultation_info(user_id)
            
            if consultation is None:
                # Первая консультация
                return {
                    "can_consult": True,
                    "remaining_messages": self.free_limit,
                    "is_first_time": True
                }
            
            if consultation.message_count >= self.free_limit:
                return {
                    "can_consult": False,
                    "remaining_messages": 0,
                    "message": "Достигнут лимит бесплатных консультаций"
                }
            
            remaining = self.free_limit - consultation.message_count
            return {
                "can_consult": True,
                "remaining_messages": remaining,
                "is_first_time": False
            }
            
        except Exception as e:
            print(f"Ошибка проверки лимита: {e}")
            return {
                "can_consult": False,
                "remaining_messages": 0,
                "message": "Ошибка проверки лимита"
            }
    
    async def start_consultation(self, user_id: int) -> Dict[str, Any]:
        """Начало консультации."""
        try:
            limit_check = await self.check_user_limit(user_id)
            
            if not limit_check["can_consult"]:
                return {
                    "success": False,
                    "message": limit_check.get("message", "Консультация недоступна"),
                    "remaining_messages": limit_check["remaining_messages"]
                }
            
            # Создаем или обновляем запись о консультации
            consultation = await db.create_or_update_consultation(user_id, 0)
            
            return {
                "success": True,
                "message": "Консультация начата",
                "remaining_messages": limit_check["remaining_messages"],
                "consultation_id": consultation.id
            }
            
        except Exception as e:
            print(f"Ошибка начала консультации: {e}")
            return {
                "success": False,
                "message": "Ошибка начала консультации"
            }
    
    async def send_message(
        self, 
        user_id: int, 
        message: str
    ) -> Dict[str, Any]:
        """Отправка сообщения в консультации."""
        try:
            # Проверяем лимит
            limit_check = await self.check_user_limit(user_id)
            if not limit_check["can_consult"]:
                return {
                    "success": False,
                    "message": "Достигнут лимит сообщений"
                }
            
            # Отправляем сообщение в OpenAI
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": """Ты - эксперт по психологии и соционике. 
                        Отвечай на вопросы пользователя профессионально, но понятно. 
                        Используй русский язык. Будь дружелюбным и полезным."""
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Увеличиваем счетчик сообщений
            await db.create_or_update_consultation(user_id, 1)
            
            return {
                "success": True,
                "ai_response": ai_response,
                "remaining_messages": limit_check["remaining_messages"] - 1
            }
            
        except Exception as e:
            print(f"Ошибка отправки сообщения: {e}")
            return {
                "success": False,
                "message": "Ошибка обработки сообщения"
            }
    
    async def end_consultation(self, user_id: int) -> bool:
        """Завершение консультации."""
        try:
            # В реальном проекте здесь можно добавить логику завершения
            # Пока просто возвращаем True
            return True
        except Exception as e:
            print(f"Ошибка завершения консультации: {e}")
            return False
    
    def get_consultation_welcome_message(self, remaining_messages: int) -> str:
        """Получение приветственного сообщения для консультации."""
        if remaining_messages == self.free_limit:
            return f"💬 Добро пожаловать в консультацию с ИИ! У вас {remaining_messages} бесплатных сообщений в месяц."
        else:
            return f"💬 Продолжаем консультацию! Осталось сообщений: {remaining_messages}"
    
    def get_limit_reached_message(self) -> str:
        """Получение сообщения о достижении лимита."""
        return f"❌ Достигнут лимит бесплатных консультаций ({self.free_limit} в месяц). Для продолжения оформите подписку."


# Глобальный экземпляр сервиса
consultation_service = ConsultationService()
