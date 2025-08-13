# 🖥️ Локальная разработка

## 🚀 Быстрый старт

### 1. Клонирование проекта
```bash
git clone https://github.com/aleshaio/humanology_telegram-bot.git
cd humanology_telegram-bot
```

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Настройка окружения
```bash
# Создайте .env файл на основе .env.example
cp .env.example .env

# Отредактируйте .env и добавьте ваш BOT_TOKEN
nano .env
```

### 4. Запуск бота
```bash
python simple_working_bot.py
```

## 🔧 Структура проекта

```
humanology_telegram-bot/
├── app/                    # Основное приложение
│   ├── main.py            # Главный файл бота (для продакшена)
│   └── requirements.txt   # Зависимости Python
├── bot/                    # Модули бота
│   ├── handlers/          # Обработчики сообщений
│   ├── services/          # Бизнес-логика
│   └── data/              # Модели данных
├── simple_working_bot.py  # Простой бот для локального тестирования
├── docker-compose.yml      # Docker Compose
├── Dockerfile              # Docker образ
└── .env                    # Переменные окружения (создать)
```

## 📱 Тестирование

### Локальный бот
- Запустите `python simple_working_bot.py`
- Найдите вашего бота в Telegram
- Отправьте `/start`
- Протестируйте все 9 кнопок меню

### Продакшен бот
- Бот уже развернут на сервере
- Найдите `@humanologybot` в Telegram
- Отправьте `/start`
- Протестируйте функционал

## 🛠️ Разработка

### Добавление новых функций

1. **Создайте обработчик в `bot/handlers/`**
```python
# bot/handlers/new_feature.py
from aiogram import types
from aiogram.filters import Command

@dp.message(Command("newcommand"))
async def handle_new_command(message: types.Message):
    await message.answer("Новая функция!")
```

2. **Добавьте логику в `bot/services/`**
```python
# bot/services/new_service.py
class NewService:
    async def process_data(self, data):
        return f"Обработано: {data}"
```

3. **Обновите меню в `app/main.py`**
```python
# Добавьте новую кнопку в keyboard
[KeyboardButton(text="Новая функция")]
```

4. **Протестируйте локально**
```bash
python simple_working_bot.py
```

5. **Задеплойте на сервер**
```bash
# На сервере
cd /opt/humanology-bot
git pull origin main
docker compose down
docker compose up -d --build
```

## 🔍 Отладка

### Логи
```bash
# Локально
python simple_working_bot.py

# На сервере
docker logs -f humanology_app
```

### Переменные окружения
```bash
# Проверьте .env файл
cat .env

# На сервере
docker exec humanology_app env | grep BOT_TOKEN
```

## 📦 Зависимости

### Основные
- `aiogram==3.4.1` - Telegram Bot API
- `python-dotenv` - Переменные окружения

### Для разработки
```bash
pip install black flake8 mypy pytest
```

### Форматирование кода
```bash
black .
flake8 .
mypy .
```

## 🚨 Частые проблемы

### Бот не запускается
- Проверьте `BOT_TOKEN` в `.env`
- Убедитесь, что установлены все зависимости
- Проверьте логи на ошибки

### Бот не отвечает
- Проверьте статус бота в Telegram
- Убедитесь, что бот не заблокирован
- Проверьте логи на сервере

### Ошибки импорта
- Убедитесь, что все модули существуют
- Проверьте структуру проекта
- Установите недостающие зависимости

## 🔄 Обновление

### Локально
```bash
git pull origin main
pip install -r requirements.txt
```

### На сервере
```bash
cd /opt/humanology-bot
git pull origin main
docker compose down
docker compose up -d --build
```

## 📚 Полезные ссылки

- [aiogram v3 Documentation](https://docs.aiogram.dev/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**🎯 Готово к разработке! Создавайте новые функции и тестируйте их локально!**
