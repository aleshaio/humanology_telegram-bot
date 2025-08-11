#!/usr/bin/env python3
"""
Скрипт для проверки импортов и моков в локальном режиме
"""

import sys
from pathlib import Path

# Добавляем корневую папку проекта в путь
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Тестируем импорты основных модулей."""
    try:
        print("🔍 Проверка импортов...")
        
        # Импортируем основные модули
        from bot.bot import TelegramBot
        print("✅ bot.bot импортирован успешно")
        
        from bot.services.site_api_service import site_api_service
        print("✅ site_api_service импортирован успешно")
        
        from bot.services.ai_service import ai_service
        print("✅ ai_service импортирован успешно")
        
        from bot.services.consultation_service import consultation_service
        print("✅ consultation_service импортирован успешно")
        
        from bot.services.test_service import test_service
        print("✅ test_service импортирован успешно")
        
        from bot.database.database import db
        print("✅ database импортирован успешно")
        
        print("\n🎉 Все импорты работают корректно!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка импорта: {e}")
        return False

def test_mocks():
    """Тестируем мок-объекты."""
    try:
        print("\n🔍 Проверка мок-объектов...")
        
        # Импортируем моки из run_local.py
        from run_local import (
            MockSiteAPIService, 
            MockAIService, 
            MockConsultationService, 
            MockTestService, 
            MockDatabase
        )
        print("✅ Мок-классы импортированы успешно")
        
        # Создаем экземпляры моков
        mock_site_api = MockSiteAPIService()
        mock_ai = MockAIService()
        mock_consultation = MockConsultationService()
        mock_test = MockTestService()
        mock_db = MockDatabase()
        print("✅ Мок-объекты созданы успешно")
        
        print("\n🎉 Все моки работают корректно!")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка моков: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Тестирование импортов и моков для локального режима\n")
    
    imports_ok = test_imports()
    mocks_ok = test_mocks()
    
    if imports_ok and mocks_ok:
        print("\n🎯 Все тесты пройдены! Бот готов к локальному запуску.")
        print("💡 Запустите: python run_local.py")
    else:
        print("\n❌ Есть проблемы с импортами или моками.")
        print("🔧 Проверьте структуру проекта и зависимости.")
