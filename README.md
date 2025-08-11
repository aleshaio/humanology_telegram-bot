# Humanology Telegram Bot

Production-ready Telegram бот на aiogram v3 с FastAPI (webhook) и PostgreSQL для психологии и соционики.

## 🚀 Возможности

### Бесплатная зона
- **📚 Справочник** - WebView на сайт с передачей user_id
- **🧪 Тесты (сайт)** - WebView на раздел тестов
- **🎯 Наш тест** - Синтетический тест из 16 вопросов с определением типа личности
- **💬 Консультация** - Чат с ИИ (лимит 5 сообщений в месяц)

### Платная зона
- **🤖 ИИ-Определение** - Анализ фото/видео/голоса через AI сервисы
- **⭐ Подписка** - WebView на оформление подписки
- **📦 Пакеты** - WebView на покупку пакетов
- **🎓 Курсы** - WebView на раздел курсов
- **🃏 Карты** - WebView на раздел карт

## 🏗️ Архитектура

```
humanology_telegram-bot/
├── bot/
│   ├── handlers/          # Обработчики команд и кнопок
│   ├── services/          # Бизнес-логика
│   ├── data/              # Локальные данные (CSV/JSON)
│   └── database/          # Модели и работа с БД
├── config.py              # Конфигурация через pydantic
├── main.py                # Точка входа FastAPI
├── requirements.txt       # Зависимости
├── Dockerfile            # Docker образ
├── docker-compose.yml    # Развертывание
└── README.md             # Документация
```

## 🛠️ Технологии

- **Python 3.11+**
- **aiogram v3** - Telegram Bot API
- **FastAPI** - Web framework для webhook
- **SQLAlchemy + asyncpg** - Асинхронная работа с PostgreSQL
- **Pydantic** - Валидация данных и конфигурация
- **OpenAI API** - GPT для анализа и консультаций
- **Docker + Docker Compose** - Контейнеризация

## 📋 Требования

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- SSL сертификат для webhook

## 🚀 Установка и запуск

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd humanology_telegram-bot
```

### 2. Настройка переменных окружения
```bash
cp env.example .env
# Отредактируйте .env файл с вашими данными
```

### 3. Запуск через Docker Compose
```bash
# Создание SSL сертификатов (для разработки)
mkdir ssl
openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes

# Запуск всех сервисов
docker-compose up -d
```

### 4. Инициализация базы данных
База данных автоматически инициализируется при первом запуске через `init_db.sql`.

## 🔧 Конфигурация

### Основные переменные окружения

| Переменная | Описание | Пример |
|------------|----------|---------|
| `BOT_TOKEN` | Токен Telegram бота | `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11` |
| `WEBHOOK_URL` | URL для webhook | `https://your-domain.com` |
| `DB_DSN` | Строка подключения к БД | `postgresql+asyncpg://user:pass@host:5432/db` |
| `SITE_API_URL` | URL API сайта | `https://your-site.com/api` |
| `OPENAI_API_KEY` | Ключ OpenAI API | `sk-...` |

### Настройка webhook

1. Убедитесь, что у вас есть SSL сертификат
2. Установите `WEBHOOK_URL` на ваш домен
3. Бот автоматически установит webhook при запуске

## 📊 База данных

### Основные таблицы

- **users** - Пользователи бота
- **user_logs** - Логи действий пользователей
- **test_results** - Результаты тестов
- **premium_access** - Премиум доступ
- **consultations** - Консультации с ИИ
- **ai_analyses** - Результаты ИИ-анализа

### Представления

- **user_stats** - Статистика пользователей
- **active_subscriptions** - Активные подписки

## 🔒 Безопасность

- Все API endpoints защищены CORS
- SSL/TLS шифрование
- Валидация входных данных через Pydantic
- Логирование всех действий пользователей
- Безопасные заголовки HTTP

## 📝 API Endpoints

- `GET /` - Информация о боте
- `GET /ping` - Health check
- `POST /webhook` - Webhook для Telegram

## 🐳 Docker

### Сборка образа
```bash
docker build -t humanology-bot .
```

### Запуск контейнеров
```bash
docker-compose up -d
```

### Просмотр логов
```bash
docker-compose logs -f app
```

## 🧪 Тестирование

### Запуск тестов
```bash
# Установка зависимостей для тестирования
pip install -r requirements.txt

# Запуск тестов
python -m pytest tests/
```

### Проверка работоспособности
```bash
# Health check
curl https://your-domain.com/ping

# Проверка webhook
curl -X POST https://your-domain.com/webhook
```

## 📈 Мониторинг

- Логирование в файлы и консоль
- Health check endpoint `/ping`
- Метрики PostgreSQL
- Мониторинг Redis

## 🔄 Развертывание

### Production
1. Настройте SSL сертификаты
2. Установите переменные окружения
3. Запустите через Docker Compose
4. Настройте мониторинг и логирование

### Development
1. Установите зависимости: `pip install -r requirements.txt`
2. Настройте локальную БД
3. Запустите: `python main.py`

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте feature branch
3. Внесите изменения
4. Создайте Pull Request

## 📄 Лицензия

MIT License

## 🆘 Поддержка

При возникновении проблем:
1. Проверьте логи: `docker-compose logs app`
2. Проверьте статус БД: `docker-compose logs postgres`
3. Создайте Issue с описанием проблемы

## 🔗 Полезные ссылки

- [aiogram документация](https://docs.aiogram.dev/)
- [FastAPI документация](https://fastapi.tiangolo.com/)
- [SQLAlchemy документация](https://docs.sqlalchemy.org/)
- [Docker документация](https://docs.docker.com/)
