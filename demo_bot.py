#!/usr/bin/env python3
"""
Демо-версия Telegram-бота для локального режима

Этот скрипт показывает, как будет работать бот, но не подключается к Telegram API.
Используйте его для понимания функциональности перед получением реального токена.

Для реального запуска:
1. Получите токен у @BotFather в Telegram
2. Добавьте его в .env файл
3. Запустите run_local_simple.py
"""

import random
import time

# Мок-данные для тестов
MOCK_TESTS = [
    {"id": 1, "name": "Тест на определение типа личности", "description": "16 вопросов для определения соционического типа"},
    {"id": 2, "name": "Тест на определение квадра", "description": "Определение принадлежности к одной из 4 квадр"},
    {"id": 3, "name": "Тест на определение роли", "description": "Определение роли в социуме"},
    {"id": 4, "name": "Тест на определение подтипа", "description": "Определение подтипа личности"}
]

MOCK_QUESTIONS = [
    {"id": 1, "question": "Как вы предпочитаете проводить свободное время?", "answers": ["В одиночестве", "В компании друзей", "Зависит от настроения"]},
    {"id": 2, "question": "Что для вас важнее в работе?", "answers": ["Результат", "Процесс", "Команда", "Признание"]},
    {"id": 3, "question": "Как вы принимаете решения?", "answers": ["Быстро, интуитивно", "Медленно, анализируя", "Советуюсь с другими"]},
    {"id": 4, "question": "Что вас больше мотивирует?", "answers": ["Достижение целей", "Новые впечатления", "Помощь другим", "Признание"]}
]

MOCK_CONSULT_ANSWERS = [
    "Спасибо за ваш вопрос! Я проанализирую ситуацию и дам рекомендации.",
    "Интересный вопрос. Позвольте мне подумать об этом с точки зрения психологии.",
    "Это очень важная тема. Давайте разберем её пошагово.",
    "Отличный вопрос! У меня есть несколько идей по этому поводу.",
    "Спасибо, что обратились за консультацией. Я готов помочь вам разобраться в этом вопросе.",
    "Это интересная проблема. Позвольте мне предложить несколько решений.",
    "Я понимаю вашу ситуацию. Давайте вместе найдем оптимальное решение.",
    "Спасибо за доверие. Я постараюсь дать максимально полезный совет."
]

def print_bot_message(message):
    """Выводит сообщение бота в консоль."""
    print(f"🤖 Бот: {message}")
    print()

def print_user_action(action, data=None):
    """Выводит действие пользователя в консоль."""
    if data:
        print(f"👤 Пользователь: {action} - {data}")
    else:
        print(f"👤 Пользователь: {action}")
    print()

def demo_start():
    """Демонстрация команды /start."""
    print_user_action("Отправил команду /start")
    
    welcome_text = """
🤖 Добро пожаловать в бота для определения типа личности!

👋 Привет, Демо-пользователь! Я помогу вам определить ваш соционический тип.

📋 Выберите действие из меню ниже:

[Справочник] [Тесты (сайт)] [Наш тест] [Консультация]
[ИИ-Определение] [Подписка] [Пакеты] [Курсы] [Карты]
    """
    
    print_bot_message(welcome_text.strip())

def demo_handbook():
    """Демонстрация кнопки 'Справочник'."""
    print_user_action("Нажал кнопку 'Справочник'")
    
    response = "🌐 WebView: Справочник (мок)\n\n📚 Здесь будет открываться справочник по соционике в WebView."
    print_bot_message(response)

def demo_tests_site():
    """Демонстрация кнопки 'Тесты (сайт)'."""
    print_user_action("Нажал кнопку 'Тесты (сайт)'")
    
    tests_text = "📝 Список доступных тестов:\n\n"
    for test in MOCK_TESTS:
        tests_text += f"🔸 {test['name']}\n"
        tests_text += f"   {test['description']}\n\n"
    
    tests_text += "🌐 WebView: Тесты (мок)"
    print_bot_message(tests_text)

def demo_our_test():
    """Демонстрация кнопки 'Наш тест'."""
    print_user_action("Нажал кнопку 'Наш тест'")
    
    # Начинаем тест
    test_text = "🧠 Наш тест на определение типа личности!\n\n"
    test_text += "📋 Вопросы:\n\n"
    
    for i, question in enumerate(MOCK_QUESTIONS, 1):
        test_text += f"{i}. {question['question']}\n"
        for j, answer in enumerate(question['answers']):
            test_text += f"   {chr(65+j)}) {answer}\n"
        test_text += "\n"
    
    # Мок-результат
    result_text = "🎯 Результаты теста (мок):\n\n"
    result_text += "📊 Гипотеза 1: Аналитик (INTJ) - 85%\n"
    result_text += "   • Квадра: Альфа\n"
    result_text += "   • Роль: Исследователь\n\n"
    result_text += "📊 Гипотеза 2: Дипломат (INFJ) - 15%\n"
    result_text += "   • Квадра: Бета\n"
    result_text += "   • Роль: Наставник"
    
    print_bot_message(test_text + "\n" + result_text)

def demo_consultation():
    """Демонстрация кнопки 'Консультация'."""
    print_user_action("Нажал кнопку 'Консультация'")
    
    # Выбираем случайный ответ
    random_answer = random.choice(MOCK_CONSULT_ANSWERS)
    
    consultation_text = f"💬 ИИ-Консультация (мок)\n\n"
    consultation_text += f"🤖 {random_answer}\n\n"
    consultation_text += "💡 Это мок-ответ. В реальном режиме здесь был бы ответ от OpenAI."
    
    print_bot_message(consultation_text)

def demo_ai_analysis():
    """Демонстрация кнопки 'ИИ-Определение'."""
    print_user_action("Нажал кнопку 'ИИ-Определение'")
    
    ai_text = "🔍 ИИ-Определение типа личности (мок)\n\n"
    ai_text += "✅ Анализ фото выполнен успешно (мок)\n\n"
    ai_text += "📊 Результаты:\n"
    ai_text += "• Тип личности: Аналитик (INTJ)\n"
    ai_text += "• Квадра: Альфа\n"
    ai_text += "• Роль: Исследователь\n"
    ai_text += "• Уверенность: 95%\n\n"
    ai_text += "💡 В реальном режиме здесь был бы анализ через InsightFace + GPT Vision."
    
    print_bot_message(ai_text)

def demo_subscription():
    """Демонстрация кнопки 'Подписка'."""
    print_user_action("Нажал кнопку 'Подписка'")
    
    response = "💳 WebView: Подписка (мок)\n\n🔐 Здесь будет открываться страница подписки в WebView."
    print_bot_message(response)

def demo_packages():
    """Демонстрация кнопки 'Пакеты'."""
    print_user_action("Нажал кнопку 'Пакеты'")
    
    response = "📦 WebView: Пакеты (мок)\n\n🎁 Здесь будет открываться страница пакетов в WebView."
    print_bot_message(response)

def demo_courses():
    """Демонстрация кнопки 'Курсы'."""
    print_user_action("Нажал кнопку 'Курсы'")
    
    response = "📚 WebView: Курсы (мок)\n\n🎓 Здесь будет открываться страница курсов в WebView."
    print_bot_message(response)

def demo_cards():
    """Демонстрация кнопки 'Карты'."""
    print_user_action("Нажал кнопку 'Карты'")
    
    response = "🃏 WebView: Карты (мок)\n\n🎴 Здесь будет открываться страница карт в WebView."
    print_bot_message(response)

def run_demo():
    """Запускает демонстрацию всех функций бота."""
    print("🚀 ДЕМО-РЕЖИМ ТЕЛЕГРАМ-БОТА")
    print("=" * 50)
    print()
    
    print("📱 Это демонстрация того, как будет работать ваш бот в Telegram.")
    print("💡 Для реального запуска получите токен у @BotFather и используйте run_local_simple.py")
    print()
    
    # Демонстрируем все функции
    demo_start()
    time.sleep(1)
    
    demo_handbook()
    time.sleep(1)
    
    demo_tests_site()
    time.sleep(1)
    
    demo_our_test()
    time.sleep(1)
    
    demo_consultation()
    time.sleep(1)
    
    demo_ai_analysis()
    time.sleep(1)
    
    demo_subscription()
    time.sleep(1)
    
    demo_packages()
    time.sleep(1)
    
    demo_courses()
    time.sleep(1)
    
    demo_cards()
    time.sleep(1)
    
    print("🎉 Демонстрация завершена!")
    print()
    print("📋 Что было показано:")
    print("✅ Главное меню с 9 кнопками")
    print("✅ Справочник (WebView мок)")
    print("✅ Список тестов (4 фиктивных теста)")
    print("✅ Наш тест (4 вопроса + результаты)")
    print("✅ ИИ-консультация (случайные ответы)")
    print("✅ ИИ-определение (анализ фото мок)")
    print("✅ Подписка, пакеты, курсы, карты (WebView моки)")
    print()
    print("🚀 Для реального запуска:")
    print("1. Получите токен у @BotFather в Telegram")
    print("2. Добавьте BOT_TOKEN=ваш_токен в .env файл")
    print("3. Запустите: python run_local_simple.py")
    print()
    print("🔍 Все действия пользователей будут логироваться в консоль")

if __name__ == "__main__":
    run_demo()
