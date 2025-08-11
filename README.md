# 🤖 Humanology Telegram Bot

**Telegram-бот для определения соционического типа личности с использованием ИИ-технологий**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![aiogram](https://img.shields.io/badge/aiogram-3.x-green.svg)](https://aiogram.dev)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-red.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-20.10+-blue.svg)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📋 Описание проекта

Humanology Telegram Bot - это интеллектуальный бот для определения соционического типа личности. Бот использует современные ИИ-технологии для анализа фотографий, видео и голосовых сообщений, а также предоставляет интерактивные тесты и консультации.

### 🌟 Основные возможности

- **🎯 Определение типа личности** через ИИ-анализ медиа
- **🧠 Интерактивные тесты** с детальными результатами
- **💬 ИИ-консультации** на основе OpenAI GPT
- **📚 Справочник по соционике** с WebView интеграцией
- **💳 Система подписок и пакетов** для премиум функций
- **📊 Детальная аналитика** и статистика пользователей

## 🚀 Быстрый старт

### Локальный режим (рекомендуется для разработки)

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/aleshaio/humanology_telegram-bot.git
cd humanology_telegram-bot
```

2. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

3. **Настройте конфигурацию:**
```bash
cp env.local.example .env
# Отредактируйте .env и добавьте BOT_TOKEN
```

4. **Запустите бота:**
```bash
python run_local_simple.py
```

### Продакшн режим

1. **Настройте переменные окружения:**
```bash
cp env.example .env
# Заполните все необходимые ключи
```

2. **Запустите через Docker Compose:**
```bash
docker-compose up -d
```

## 🔧 Технологический стек

- **Python 3.8+** - основной язык разработки
- **aiogram 3.x** - современная библиотека для Telegram ботов
- **FastAPI** - веб-фреймворк для webhook
- **SQLAlchemy 2.0** - ORM для работы с базой данных
- **PostgreSQL** - основная СУБД
- **Docker** - контейнеризация

## 📱 Функциональность

### 🆓 Бесплатные функции
- **Справочник** - базовая информация по соционике
- **Тесты (сайт)** - доступ к внешним тестам
- **Наш тест** - 16 вопросов для определения типа
- **Консультация** - 5 бесплатных сообщений в месяц

### 💎 Премиум функции
- **ИИ-Определение** - анализ фото/видео/голоса
- **Расширенные отчеты** - детальная аналитика
- **Неограниченные консультации** - без лимитов

## 📖 Документация

- **[Подробная документация](PROJECT_DOCUMENTATION.md)** - полное описание проекта
- **[Инструкции по запуску](LAUNCH_INSTRUCTIONS.md)** - пошаговые инструкции
- **[Локальный режим](README_LOCAL.md)** - отладка без деплоя
- **[Настройка GitHub](GITHUB_SETUP.md)** - создание репозитория

## 🧪 Тестирование

```bash
# Демо-режим (без Telegram API)
python demo_bot.py

# Локальный режим с моками
python run_local_simple.py

# Запуск тестов
pytest tests/
```

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения и закоммитьте
4. Создайте Pull Request

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. См. файл [LICENSE](LICENSE) для подробностей.

## 🔗 Полезные ссылки

- [aiogram документация](https://aiogram.dev/)
- [FastAPI документация](https://fastapi.tiangolo.com/)
- [SQLAlchemy документация](https://docs.sqlalchemy.org/)
- [PostgreSQL документация](https://www.postgresql.org/docs/)

---

**Разработано с ❤️ для сообщества социоников**

*Если проект вам понравился, поставьте ⭐ звездочку!*
