# 🚀 Развертывание Humanology Bot

## 🎯 Статус

✅ **Бот успешно развернут на VDS и работает!**

- **Сервер:** 141.8.198.171
- **Статус:** Контейнеры запущены, бот отвечает
- **Telegram:** @humanologybot

## 🏗️ Архитектура развертывания

```
VDS (141.8.198.171)
├── /opt/humanology-bot/          # Рабочая директория
├── Docker + Docker Compose        # Контейнеризация
├── PostgreSQL 16                  # База данных
└── UFW + fail2ban                 # Безопасность
```

## 🔧 Требования к серверу

- **ОС:** Ubuntu/Debian
- **RAM:** Минимум 1GB
- **Диск:** Минимум 10GB
- **Порты:** 22 (SSH), 80 (HTTP), 443 (HTTPS)

## 📋 Подготовка сервера

### 1. Базовые пакеты
```bash
apt update && apt upgrade -y
apt install -y git curl ufw fail2ban docker.io docker-compose-plugin
```

### 2. Настройка безопасности
```bash
# UFW
ufw allow 22
ufw allow 80
ufw allow 443
ufw enable

# fail2ban
systemctl enable fail2ban
systemctl start fail2ban
```

### 3. Docker
```bash
systemctl enable docker
systemctl start docker
```

## 🚀 Развертывание

### 1. Подключение к серверу
```bash
ssh root@141.8.198.171
# Пароль: Дшмукзщщдас1!
```

### 2. Создание рабочей директории
```bash
mkdir -p /opt/humanology-bot
cd /opt/humanology-bot
```

### 3. Клонирование проекта
```bash
git clone https://github.com/aleshaio/humanology_telegram-bot.git .
```

### 4. Создание .env файла
```bash
cat > .env << 'EOF'
BOT_TOKEN=7755199130:AAGQjQvQ3wSFu5-853jxa4kU8rvM30VE-E4
DB_DSN=postgresql+asyncpg://bot:botpass@postgres:5432/botdb
SITE_API_URL=placeholder_url
SITE_API_KEY=placeholder_key
OPENAI_API_KEY=placeholder_key
WEBHOOK_URL=
MODE=polling
EOF
```

### 5. Запуск контейнеров
```bash
docker compose up -d --build
```

### 6. Проверка статуса
```bash
docker ps
docker logs humanology_app
```

## 🔄 Обновление

### Автоматическое обновление
```bash
cd /opt/humanology-bot
git pull origin main
docker compose down
docker compose up -d --build
```

### Ручное обновление
```bash
cd /opt/humanology-bot
git fetch origin
git reset --hard origin/main
docker compose down
docker compose up -d --build
```

## 📊 Мониторинг

### Статус контейнеров
```bash
docker ps -a
docker stats
```

### Логи приложения
```bash
# Последние 50 строк
docker logs humanology_app --tail 50

# Следить за логами в реальном времени
docker logs -f humanology_app

# Логи с определенного времени
docker logs humanology_app --since "2024-01-01T00:00:00"
```

### Состояние базы данных
```bash
docker exec -it humanology_pg psql -U bot -d botdb -c "\dt"
```

## 🚨 Устранение неполадок

### Проблема: Контейнер не запускается
```bash
# Проверить логи
docker logs humanology_app

# Перезапустить
docker compose restart app

# Пересобрать образ
docker compose up -d --build --force-recreate
```

### Проблема: Бот не отвечает
```bash
# Проверить статус
docker ps

# Проверить логи
docker logs humanology_app --tail 100

# Проверить переменные окружения
docker exec humanology_app env | grep BOT_TOKEN
```

### Проблема: Ошибки в коде
```bash
# Остановить контейнеры
docker compose down

# Исправить код
nano app/main.py

# Запустить заново
docker compose up -d --build
```

## 🔒 Безопасность

### SSH ключи (рекомендуется)
```bash
# На локальной машине
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
ssh-copy-id root@141.8.198.171

# Отключить парольную аутентификацию
nano /etc/ssh/sshd_config
# PasswordAuthentication no
systemctl restart ssh
```

### Firewall
```bash
ufw status
ufw allow from your_ip to any port 22
```

### Обновления
```bash
# Автоматические обновления безопасности
apt install unattended-upgrades
dpkg-reconfigure unattended-upgrades
```

## 📈 Масштабирование

### Увеличение ресурсов
```bash
# Остановить контейнеры
docker compose down

# Изменить docker-compose.yml (добавить limits)
# Запустить с новыми настройками
docker compose up -d
```

### Балансировка нагрузки
```bash
# Добавить nginx контейнер
# Настроить reverse proxy
# Добавить health checks
```

## 🎯 Тестирование развертывания

### 1. Проверка контейнеров
```bash
docker ps
# Должны быть: humanology_app (Up), humanology_pg (Up)
```

### 2. Проверка логов
```bash
docker logs humanology_app
# Должно быть: "Bot starting..."
```

### 3. Тест в Telegram
- Найдите @humanologybot
- Отправьте `/start`
- Проверьте все 9 кнопок меню

### 4. Проверка базы данных
```bash
docker exec -it humanology_pg psql -U bot -d botdb -c "SELECT version();"
```

## 📚 Полезные команды

### Docker
```bash
# Очистка неиспользуемых образов
docker system prune -a

# Просмотр использования диска
docker system df

# Остановка всех контейнеров
docker stop $(docker ps -q)
```

### Система
```bash
# Мониторинг ресурсов
htop
df -h
free -h

# Проверка логов системы
journalctl -u docker
journalctl -u ssh
```

---

**🎉 Бот успешно развернут и готов к работе!**
