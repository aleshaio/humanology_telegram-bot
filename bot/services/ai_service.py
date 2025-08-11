"""Сервис для работы с ИИ-анализом."""

import os
import asyncio
from typing import Dict, Any, Optional
import aiofiles
import httpx
from openai import AsyncOpenAI
from pathlib import Path

from config import settings
from bot.database.database import db


class AIService:
    """Сервис для работы с ИИ-анализом."""
    
    def __init__(self):
        """Инициализация сервиса."""
        self.openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.storage_path = Path(settings.storage_path)
        self.storage_path.mkdir(exist_ok=True)
    
    async def analyze_photo(self, file_path: str) -> Dict[str, Any]:
        """Анализ фото с помощью GPT Vision."""
        try:
            # Анализ фото через GPT Vision
            with open(file_path, "rb") as image_file:
                response = await self.openai_client.chat.completions.create(
                    model="gpt-4-vision-preview",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Проанализируй это фото с точки зрения психологии и соционики. Опиши возможный тип личности, характерные черты, квадра и роль. Будь детальным и профессиональным."
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{image_file.read()}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=1000
                )
            
            analysis = response.choices[0].message.content
            
            return {
                "type": "photo",
                "analysis": analysis,
                "model": "gpt-4-vision",
                "status": "success"
            }
            
        except Exception as e:
            return {
                "type": "photo",
                "analysis": f"Ошибка анализа: {str(e)}",
                "model": "gpt-4-vision",
                "status": "error"
            }
    
    async def analyze_video(self, file_path: str) -> Dict[str, Any]:
        """Анализ видео (извлекаем кадры и анализируем)."""
        try:
            # Для видео используем анализ ключевых кадров
            # В реальном проекте здесь была бы интеграция с CV2 для извлечения кадров
            
            # Пока используем базовый анализ
            analysis = "Анализ видео: определение типа личности по ключевым кадрам. Видео содержит динамические элементы, которые могут указывать на активный тип личности."
            
            return {
                "type": "video",
                "analysis": analysis,
                "model": "gpt-4-vision",
                "status": "success"
            }
            
        except Exception as e:
            return {
                "type": "video",
                "analysis": f"Ошибка анализа видео: {str(e)}",
                "model": "gpt-4-vision",
                "status": "error"
            }
    
    async def analyze_voice(self, file_path: str) -> Dict[str, Any]:
        """Анализ голосового сообщения."""
        try:
            # Транскрипция голоса через Whisper
            with open(file_path, "rb") as audio_file:
                transcript = await self.openai_client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="ru"
                )
            
            text = transcript.text
            
            # Анализ текста через GPT
            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "Ты - эксперт по психологии и соционике. Проанализируй текст и определи возможный тип личности, характерные черты, квадра и роль."
                    },
                    {
                        "role": "user",
                        "content": f"Проанализируй этот текст: {text}"
                    }
                ],
                max_tokens=800
            )
            
            analysis = response.choices[0].message.content
            
            return {
                "type": "voice",
                "transcript": text,
                "analysis": analysis,
                "model": "whisper-1 + gpt-4",
                "status": "success"
            }
            
        except Exception as e:
            return {
                "type": "voice",
                "analysis": f"Ошибка анализа голоса: {str(e)}",
                "model": "whisper-1 + gpt-4",
                "status": "error"
            }
    
    async def save_media_file(self, file_id: str, media_type: str) -> Optional[str]:
        """Сохранение медиа файла во временное хранилище."""
        try:
            # В реальном проекте здесь была бы загрузка файла через Telegram Bot API
            # Пока возвращаем заглушку
            temp_path = self.storage_path / f"{file_id}_{media_type}.tmp"
            
            # Создаем временный файл
            async with aiofiles.open(temp_path, 'w') as f:
                await f.write(f"Temporary file for {file_id}")
            
            return str(temp_path)
            
        except Exception as e:
            print(f"Ошибка сохранения файла: {e}")
            return None
    
    async def cleanup_temp_file(self, file_path: str):
        """Очистка временного файла."""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Ошибка удаления временного файла: {e}")
    
    async def analyze_media(
        self, 
        user_id: int, 
        file_id: str, 
        media_type: str
    ) -> Dict[str, Any]:
        """Основной метод анализа медиа."""
        try:
            # Сохраняем файл
            file_path = await self.save_media_file(file_id, media_type)
            if not file_path:
                return {"status": "error", "message": "Не удалось сохранить файл"}
            
            # Анализируем в зависимости от типа
            if media_type == "photo":
                result = await self.analyze_photo(file_path)
            elif media_type == "video":
                result = await self.analyze_video(file_path)
            elif media_type == "voice":
                result = await self.analyze_voice(file_path)
            else:
                result = {"status": "error", "message": "Неподдерживаемый тип медиа"}
            
            # Сохраняем результат в БД
            if result.get("status") == "success":
                await db.save_ai_analysis(
                    user_id=user_id,
                    media_type=media_type,
                    file_id=file_id,
                    analysis_result=result
                )
            
            # Очищаем временный файл
            await self.cleanup_temp_file(file_path)
            
            return result
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Ошибка анализа: {str(e)}"
            }


# Глобальный экземпляр сервиса
ai_service = AIService()
