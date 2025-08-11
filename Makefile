.PHONY: help install dev test lint format clean docker-build docker-up docker-down

help: ## Показать справку
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Установить зависимости
	pip install -r requirements.txt

dev: ## Запустить в development режиме
	python run_dev.py

test: ## Запустить тесты
	pytest tests/ -v

lint: ## Проверить код линтерами
	black --check .
	isort --check-only .
	mypy .

format: ## Отформатировать код
	black .
	isort .

clean: ## Очистить временные файлы
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

docker-build: ## Собрать Docker образ
	docker build -t humanology-bot .

docker-up: ## Запустить через Docker Compose
	docker-compose up -d

docker-down: ## Остановить Docker Compose
	docker-compose down

docker-logs: ## Показать логи Docker
	docker-compose logs -f

docker-restart: ## Перезапустить Docker Compose
	docker-compose restart

setup-dev: ## Настройка development окружения
	@echo "Настройка development окружения..."
	@if [ ! -f .env ]; then \
		cp env.example .env; \
		echo "Создан файл .env из env.example"; \
		echo "Отредактируйте .env с вашими настройками"; \
	else \
		echo "Файл .env уже существует"; \
	fi
	@echo "Установка зависимостей..."
	pip install -r requirements.txt
	@echo "Development окружение настроено!"

check-env: ## Проверить переменные окружения
	@if [ ! -f .env ]; then \
		echo "❌ Файл .env не найден!"; \
		echo "Выполните: make setup-dev"; \
		exit 1; \
	fi
	@echo "✅ Файл .env найден"
	@echo "Проверка обязательных переменных..."
	@source .env && \
	if [ -z "$$BOT_TOKEN" ]; then \
		echo "❌ BOT_TOKEN не установлен"; \
		exit 1; \
	fi && \
	if [ -z "$$WEBHOOK_URL" ]; then \
		echo "❌ WEBHOOK_URL не установлен"; \
		exit 1; \
	fi && \
	if [ -z "$$DB_DSN" ]; then \
		echo "❌ DB_DSN не установлен"; \
		exit 1; \
	fi && \
	if [ -z "$$OPENAI_API_KEY" ]; then \
		echo "❌ OPENAI_API_KEY не установлен"; \
		exit 1; \
	fi && \
	echo "✅ Все обязательные переменные установлены"

run: check-env ## Запустить бота (с проверкой окружения)
	python run_dev.py

full-setup: setup-dev check-env ## Полная настройка проекта
	@echo "🎉 Проект полностью настроен!"
	@echo "Для запуска выполните: make run"
