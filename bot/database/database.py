"""Работа с базой данных."""

import asyncio
import json
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, update, delete
from contextlib import asynccontextmanager

from config import settings
from .models import Base, User, UserLog, TestResult, PremiumAccess, Consultation, AIAnalysis


class Database:
    """Класс для работы с базой данных."""
    
    def __init__(self):
        """Инициализация подключения к БД."""
        self.engine = create_async_engine(settings.db_dsn, echo=settings.debug)
        self.async_session = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
    
    async def create_tables(self):
        """Создание всех таблиц."""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    @asynccontextmanager
    async def get_session(self):
        """Получение сессии БД."""
        async with self.async_session() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
    
    async def get_or_create_user(
        self, 
        telegram_id: int, 
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
    ) -> User:
        """Получение или создание пользователя."""
        async with self.get_session() as session:
            # Поиск существующего пользователя
            result = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            user = result.scalar_one_or_none()
            
            if user is None:
                # Создание нового пользователя
                user = User(
                    telegram_id=telegram_id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name
                )
                session.add(user)
                await session.flush()
                await session.refresh(user)
            else:
                # Обновление существующего пользователя
                user.username = username
                user.first_name = first_name
                user.last_name = last_name
                user.updated_at = asyncio.get_event_loop().time()
            
            return user
    
    async def log_user_action(
        self, 
        user_id: int, 
        action: str, 
        details: Optional[str] = None
    ):
        """Логирование действия пользователя."""
        async with self.get_session() as session:
            log = UserLog(
                user_id=user_id,
                action=action,
                details=details
            )
            session.add(log)
    
    async def save_test_result(
        self, 
        user_id: int, 
        test_type: str, 
        result_data: Dict[str, Any]
    ) -> TestResult:
        """Сохранение результата теста."""
        async with self.get_session() as session:
            result = TestResult(
                user_id=user_id,
                test_type=test_type,
                result_data=json.dumps(result_data, ensure_ascii=False)
            )
            session.add(result)
            await session.flush()
            await session.refresh(result)
            return result
    
    async def get_user_premium_access(self, user_id: int) -> List[PremiumAccess]:
        """Получение премиум доступа пользователя."""
        async with self.get_session() as session:
            result = await session.execute(
                select(PremiumAccess).where(
                    PremiumAccess.user_id == user_id,
                    PremiumAccess.is_active == True
                )
            )
            return result.scalars().all()
    
    async def check_subscription_status(self, user_id: int) -> bool:
        """Проверка статуса подписки."""
        async with self.get_session() as session:
            result = await session.execute(
                select(PremiumAccess).where(
                    PremiumAccess.user_id == user_id,
                    PremiumAccess.access_type == "subscription",
                    PremiumAccess.is_active == True
                )
            )
            return result.scalar_one_or_none() is not None
    
    async def check_package_balance(self, user_id: int) -> int:
        """Проверка баланса пакетов."""
        async with self.get_session() as session:
            result = await session.execute(
                select(PremiumAccess).where(
                    PremiumAccess.user_id == user_id,
                    PremiumAccess.access_type == "package",
                    PremiumAccess.is_active == True
                )
            )
            packages = result.scalars().all()
            return sum(pkg.remaining_uses or 0 for pkg in packages)
    
    async def get_consultation_info(self, user_id: int) -> Optional[Consultation]:
        """Получение информации о консультации пользователя."""
        async with self.get_session() as session:
            result = await session.execute(
                select(Consultation).where(Consultation.user_id == user_id)
            )
            return result.scalar_one_or_none()
    
    async def create_or_update_consultation(
        self, 
        user_id: int, 
        message_count: int = 1
    ) -> Consultation:
        """Создание или обновление консультации."""
        async with self.get_session() as session:
            result = await session.execute(
                select(Consultation).where(Consultation.user_id == user_id)
            )
            consultation = result.scalar_one_or_none()
            
            if consultation is None:
                consultation = Consultation(
                    user_id=user_id,
                    message_count=message_count
                )
                session.add(consultation)
            else:
                consultation.message_count += message_count
                consultation.last_message_at = asyncio.get_event_loop().time()
            
            await session.flush()
            await session.refresh(consultation)
            return consultation
    
    async def save_ai_analysis(
        self, 
        user_id: int, 
        media_type: str, 
        file_id: str, 
        analysis_result: Dict[str, Any]
    ) -> AIAnalysis:
        """Сохранение результата ИИ-анализа."""
        async with self.get_session() as session:
            analysis = AIAnalysis(
                user_id=user_id,
                media_type=media_type,
                file_id=file_id,
                analysis_result=json.dumps(analysis_result, ensure_ascii=False)
            )
            session.add(analysis)
            await session.flush()
            await session.refresh(analysis)
            return analysis
    
    async def close(self):
        """Закрытие соединения с БД."""
        await self.engine.dispose()


# Глобальный экземпляр БД
db = Database()
