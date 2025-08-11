"""Модели базы данных."""

from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """Модель пользователя."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String(100), nullable=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    logs = relationship("UserLog", back_populates="user")
    test_results = relationship("TestResult", back_populates="user")
    premium_access = relationship("PremiumAccess", back_populates="user")


class UserLog(Base):
    """Модель логов действий пользователя."""
    
    __tablename__ = "user_logs"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(200), nullable=False)
    details = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    user = relationship("User", back_populates="logs")


class TestResult(Base):
    """Модель результатов тестов."""
    
    __tablename__ = "test_results"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    test_type = Column(String(50), nullable=False)  # "our_test", "site_test"
    result_data = Column(Text, nullable=False)  # JSON с результатами
    completed_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    user = relationship("User", back_populates="test_results")


class PremiumAccess(Base):
    """Модель премиум доступа пользователя."""
    
    __tablename__ = "premium_access"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    access_type = Column(String(50), nullable=False)  # "subscription", "package"
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime, nullable=True)
    remaining_uses = Column(Integer, nullable=True)  # Для пакетов
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    user = relationship("User", back_populates="premium_access")


class Consultation(Base):
    """Модель консультаций с ИИ."""
    
    __tablename__ = "consultations"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message_count = Column(Integer, default=0)
    last_message_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    user = relationship("User")


class AIAnalysis(Base):
    """Модель результатов ИИ-анализа."""
    
    __tablename__ = "ai_analyses"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    media_type = Column(String(20), nullable=False)  # "photo", "video", "voice"
    file_id = Column(String(200), nullable=False)
    analysis_result = Column(Text, nullable=False)  # JSON с результатом
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    user = relationship("User")
