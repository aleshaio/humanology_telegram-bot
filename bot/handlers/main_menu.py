"""Обработчик главного меню."""

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from .base import BaseHandler
from bot.data.messages import MAIN_MENU_TEXT, FREE_ZONE_MESSAGES, PREMIUM_MESSAGES
from bot.data.keyboards import (
    get_main_menu_keyboard,
    get_ai_analysis_keyboard,
    get_webview_keyboard,
    get_consultation_keyboard
)
from bot.services.site_api_service import site_api_service
from bot.services.consultation_service import consultation_service


class MainMenuHandler(BaseHandler):
    """Обработчик главного меню."""
    
    def _setup_handlers(self):
        """Настройка обработчиков."""
        # Команда /start
        self.router.message.register(
            self._handle_start,
            Command("start")
        )
        
        # Главное меню
        self.router.callback_query.register(
            self._handle_main_menu,
            F.data == "back_to_menu"
        )
        
        # Справочник
        self.router.callback_query.register(
            self._handle_handbook,
            F.data == "handbook"
        )
        
        # Тесты сайта
        self.router.callback_query.register(
            self._handle_tests_site,
            F.data == "tests_site"
        )
        
        # Наш тест
        self.router.callback_query.register(
            self._handle_our_test,
            F.data == "our_test"
        )
        
        # Консультация
        self.router.callback_query.register(
            self._handle_consultation,
            F.data == "consultation"
        )
        
        # ИИ-анализ
        self.router.callback_query.register(
            self._handle_ai_analysis,
            F.data == "ai_analysis"
        )
        
        # Подписка
        self.router.callback_query.register(
            self._handle_subscription,
            F.data == "subscription"
        )
        
        # Пакеты
        self.router.callback_query.register(
            self._handle_packages,
            F.data == "packages"
        )
        
        # Курсы
        self.router.callback_query.register(
            self._handle_courses,
            F.data == "courses"
        )
        
        # Карты
        self.router.callback_query.register(
            self._handle_cards,
            F.data == "cards"
        )
    
    async def _handle_start(self, message: Message):
        """Обработка команды /start."""
        user_id = await self._get_or_create_user(message)
        await self._log_user_action(user_id, "start_command")
        
        await message.answer(
            MAIN_MENU_TEXT,
            reply_markup=get_main_menu_keyboard()
        )
    
    async def _handle_main_menu(self, callback: CallbackQuery):
        """Возврат в главное меню."""
        await callback.message.edit_text(
            MAIN_MENU_TEXT,
            reply_markup=get_main_menu_keyboard()
        )
        await callback.answer()
    
    async def _handle_handbook(self, callback: CallbackQuery):
        """Обработка кнопки 'Справочник'."""
        try:
            user_id = await self._get_or_create_user(callback.message)
            await self._log_user_action(user_id, "handbook_clicked")
            
            # Получаем URL для справочника
            url = site_api_service.get_webview_url("handbook", user_id)
            
            await callback.message.edit_text(
                FREE_ZONE_MESSAGES["handbook"],
                reply_markup=get_webview_keyboard(url, "📚 Открыть справочник")
            )
            await callback.answer()
            
        except Exception as e:
            await self._handle_callback_error(callback, "general")
    
    async def _handle_tests_site(self, callback: CallbackQuery):
        """Обработка кнопки 'Тесты (сайт)'."""
        try:
            user_id = await self._get_or_create_user(callback.message)
            await self._log_user_action(user_id, "tests_site_clicked")
            
            # Получаем URL для тестов
            url = site_api_service.get_webview_url("tests", user_id)
            
            await callback.message.edit_text(
                FREE_ZONE_MESSAGES["tests_site"],
                reply_markup=get_webview_keyboard(url, "🧪 Перейти к тестам")
            )
            await callback.answer()
            
        except Exception as e:
            await self._handle_callback_error(callback, "general")
    
    async def _handle_our_test(self, callback: CallbackQuery):
        """Обработка кнопки 'Наш тест'."""
        try:
            user_id = await self._get_or_create_user(callback.message)
            await self._log_user_action(user_id, "our_test_clicked")
            
            # Переходим к тесту
            from bot.handlers.test_handler import test_handler
            await test_handler.start_test(callback)
            
        except Exception as e:
            await self._handle_callback_error(callback, "general")
    
    async def _handle_consultation(self, callback: CallbackQuery):
        """Обработка кнопки 'Консультация'."""
        try:
            user_id = await self._get_or_create_user(callback.message)
            await self._log_user_action(user_id, "consultation_clicked")
            
            # Проверяем лимит консультаций
            limit_check = await consultation_service.check_user_limit(user_id)
            
            if limit_check["can_consult"]:
                await callback.message.edit_text(
                    consultation_service.get_consultation_welcome_message(
                        limit_check["remaining_messages"]
                    ),
                    reply_markup=get_consultation_keyboard()
                )
            else:
                await callback.message.edit_text(
                    consultation_service.get_limit_reached_message(),
                    reply_markup=get_main_menu_keyboard()
                )
            
            await callback.answer()
            
        except Exception as e:
            await self._handle_callback_error(callback, "general")
    
    async def _handle_ai_analysis(self, callback: CallbackQuery):
        """Обработка кнопки 'ИИ-Определение'."""
        try:
            user_id = await self._get_or_create_user(callback.message)
            await self._log_user_action(user_id, "ai_analysis_clicked")
            
            # Проверяем доступ к премиум функциям
            has_subscription = await db.check_subscription_status(user_id)
            package_balance = await db.check_package_balance(user_id)
            
            if has_subscription or package_balance > 0:
                await callback.message.edit_text(
                    PREMIUM_MESSAGES["ai_analysis_start"],
                    reply_markup=get_ai_analysis_keyboard()
                )
            else:
                await callback.message.edit_text(
                    PREMIUM_MESSAGES["access_denied"],
                    reply_markup=get_main_menu_keyboard()
                )
            
            await callback.answer()
            
        except Exception as e:
            await self._handle_callback_error(callback, "general")
    
    async def _handle_subscription(self, callback: CallbackQuery):
        """Обработка кнопки 'Подписка'."""
        try:
            user_id = await self._get_or_create_user(callback.message)
            await self._log_user_action(user_id, "subscription_clicked")
            
            # Получаем URL для подписки
            url = site_api_service.get_webview_url("subscription", user_id)
            
            await callback.message.edit_text(
                PREMIUM_MESSAGES["subscription_check"],
                reply_markup=get_webview_keyboard(url, "⭐ Оформить подписку")
            )
            await callback.answer()
            
        except Exception as e:
            await self._handle_callback_error(callback, "general")
    
    async def _handle_packages(self, callback: CallbackQuery):
        """Обработка кнопки 'Пакеты'."""
        try:
            user_id = await self._get_or_create_user(callback.message)
            await self._log_user_action(user_id, "packages_clicked")
            
            # Получаем URL для пакетов
            url = site_api_service.get_webview_url("packages", user_id)
            
            await callback.message.edit_text(
                PREMIUM_MESSAGES["packages_check"],
                reply_markup=get_webview_keyboard(url, "📦 Купить пакет")
            )
            await callback.answer()
            
        except Exception as e:
            await self._handle_callback_error(callback, "general")
    
    async def _handle_courses(self, callback: CallbackQuery):
        """Обработка кнопки 'Курсы'."""
        try:
            user_id = await self._get_or_create_user(callback.message)
            await self._log_user_action(user_id, "courses_clicked")
            
            # Получаем URL для курсов
            url = site_api_service.get_webview_url("courses", user_id)
            
            await callback.message.edit_text(
                "🎓 Переходим к курсам...",
                reply_markup=get_webview_keyboard(url, "🎓 Открыть курсы")
            )
            await callback.answer()
            
        except Exception as e:
            await self._handle_callback_error(callback, "general")
    
    async def _handle_cards(self, callback: CallbackQuery):
        """Обработка кнопки 'Карты'."""
        try:
            user_id = await self._get_or_create_user(callback.message)
            await self._log_user_action(user_id, "cards_clicked")
            
            # Получаем URL для карт
            url = site_api_service.get_webview_url("cards", user_id)
            
            await callback.message.edit_text(
                "🃏 Переходим к картам...",
                reply_markup=get_webview_keyboard(url, "🃏 Открыть карты")
            )
            await callback.answer()
            
        except Exception as e:
            await self._handle_callback_error(callback, "general")


# Создание экземпляра обработчика
main_menu_handler = MainMenuHandler(Router())
