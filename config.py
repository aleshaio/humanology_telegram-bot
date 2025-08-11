"""Конфигурация приложения."""

from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения."""
    
    # Telegram Bot
    bot_token: str = Field(..., env="BOT_TOKEN")
    
    # Webhook
    webhook_url: str = Field(..., env="WEBHOOK_URL")
    webhook_path: str = Field("/webhook", env="WEBHOOK_PATH")
    
    # База данных
    db_dsn: str = Field(..., env="DB_DSN")
    
    # API сайта
    site_api_url: str = Field(..., env="SITE_API_URL")
    site_api_key: str = Field(..., env="SITE_API_KEY")
    
    # OpenAI
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    
    # Пути
    storage_path: str = Field("./storage", env="STORAGE_PATH")
    
    # Лимиты
    free_consultation_limit: int = Field(5, env="FREE_CONSULTATION_LIMIT")
    
    # Настройки сервера
    host: str = Field("0.0.0.0", env="HOST")
    port: int = Field(8000, env="PORT")
    debug: bool = Field(False, env="DEBUG")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Глобальный экземпляр настроек
settings = Settings()
