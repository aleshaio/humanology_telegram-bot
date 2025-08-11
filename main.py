"""Главный файл приложения."""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from bot.bot import telegram_bot


# Настройка логирования
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения."""
    # Запуск
    await telegram_bot.on_startup(app)
    logger.info("Приложение запущено")
    
    yield
    
    # Остановка
    await telegram_bot.on_shutdown(app)
    logger.info("Приложение остановлено")


# Создание FastAPI приложения
app = FastAPI(
    title="Humanology Telegram Bot",
    description="Telegram бот для психологии и соционики",
    version="1.0.0",
    lifespan=lifespan
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
async def health_check():
    """Проверка здоровья приложения."""
    return {"status": "ok", "message": "Bot is running"}


@app.get("/")
async def root():
    """Корневой endpoint."""
    return {
        "message": "Humanology Telegram Bot API",
        "version": "1.0.0",
        "status": "running"
    }


@app.post(settings.webhook_path)
async def webhook_handler(request: Request):
    """Обработчик webhook от Telegram."""
    try:
        # Получаем обработчик webhook от бота
        webhook_handler = await telegram_bot.get_webhook_handler()
        
        # Обрабатываем запрос
        return await webhook_handler.handle(request)
        
    except Exception as e:
        logger.error(f"Ошибка обработки webhook: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error"}
        )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Глобальный обработчик исключений."""
    logger.error(f"Необработанное исключение: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info" if not settings.debug else "debug"
    )
