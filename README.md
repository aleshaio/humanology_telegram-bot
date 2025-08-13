# 🤖 Humanology Telegram Bot

**Производственный Telegram-бот на aiogram v3 с PostgreSQL**

## 🎯 Статус проекта

✅ **Бот успешно развернут и работает на VDS**
- Контейнеры запущены и функционируют
- Бот отвечает на сообщения
- Меню с 9 кнопками работает корректно

## 🚀 Быстрый старт

### Локальная разработка
```bash
# Клонируйте репозиторий
git clone https://github.com/aleshaio/humanology_telegram-bot.git
cd humanology_telegram-bot

# Установите зависимости
pip install -r requirements.txt

# Создайте .env файл
cp .env.example .env
# Отредактируйте .env и добавьте BOT_TOKEN

# Запустите бота
python simple_working_bot.py
```

### Развертывание на сервер
```bash
# Подключитесь к серверу
ssh root@141.8.198.171

# Перейдите в директорию проекта
cd /opt/humanology-bot

# Остановите контейнеры (если нужно)
docker compose down

# Запустите контейнеры
docker compose up -d --build

# Проверьте статус
docker ps
docker logs humanology_app
```

## 🏗️ Архитектура

```
humanology_telegram-bot/
├── app/                    # Основное приложение
│   ├── main.py            # Главный файл бота
│   └── requirements.txt   # Зависимости Python
├── bot/                    # Модули бота
│   ├── handlers/          # Обработчики сообщений
│   ├── services/          # Бизнес-логика
│   └── data/              # Модели данных
├── docker/                 # Docker конфигурация
│   └── nginx.conf         # Конфигурация Nginx
├── docker-compose.yml      # Docker Compose
├── Dockerfile              # Docker образ
├── .env.example           # Пример переменных окружения
└── README.md              # Документация
```

## 🔧 Функционал бота

### Главное меню (9 кнопок)
- **Справочник** - WebView справочника
- **Тесты (сайт)** - Список доступных тестов
- **Наш тест** - Интерактивный тест
- **Консультация** - Персональные рекомендации
- **ИИ-Определение** - Анализ фото
- **Подписка** - Управление подпиской
- **Пакеты** - Пакеты услуг
- **Курсы** - Образовательные курсы
- **Карты** - Карты развития

### Технические особенности
- **aiogram v3** - Современная библиотека для Telegram ботов
- **PostgreSQL** - Надежная база данных
- **Docker** - Контейнеризация для простого развертывания
- **Async/await** - Асинхронная обработка сообщений
- **Логирование** - Подробные логи всех действий

## 🐳 Docker

### Запуск
```bash
docker compose up -d --build
```

### Остановка
```bash
docker compose down
```

### Логи
```bash
docker logs -f humanology_app
```

### Перезапуск
```bash
docker compose restart app
```

## 🔐 Переменные окружения

Создайте файл `.env` на основе `.env.example`:

```bash
BOT_TOKEN=your_bot_token_here
DB_DSN=postgresql+asyncpg://bot:botpass@postgres:5432/botdb
SITE_API_URL=your_site_api_url
SITE_API_KEY=your_site_api_key
OPENAI_API_KEY=your_openai_api_key
WEBHOOK_URL=your_webhook_url
MODE=polling
```

## 📱 Тестирование

1. Найдите бота `@humanologybot` в Telegram
2. Отправьте команду `/start`
3. Проверьте работу всех кнопок меню
4. Убедитесь, что бот логирует действия

## 🚀 Разработка

### Добавление новых функций
1. Создайте обработчик в `bot/handlers/`
2. Добавьте логику в `bot/services/`
3. Обновите меню в `app/main.py`
4. Протестируйте локально
5. Задеплойте на сервер

### Структура обработчика
```python
@dp.message()
async def handle_new_feature(message: types.Message):
    # Ваша логика здесь
    await message.answer("Ответ пользователю")
```

## 📊 Мониторинг

### Проверка статуса
```bash
# Статус контейнеров
docker ps

# Логи приложения
docker logs humanology_app --tail 50

# Использование ресурсов
docker stats
```

### Перезапуск при сбоях
```bash
docker compose restart app
```

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Создайте Pull Request

## 📄 Лицензия

MIT License

## 👨‍💻 Автор

**aleshaio** - [GitHub](https://github.com/aleshaio)

---

**🎉 Бот готов к продакшену и активно развивается!**
