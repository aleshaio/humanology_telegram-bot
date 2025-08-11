"""Клавиатуры для бота."""

from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from .messages import BUTTONS


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Главное меню бота."""
    keyboard = [
        [
            InlineKeyboardButton(
                text=BUTTONS["handbook"],
                callback_data="handbook"
            ),
            InlineKeyboardButton(
                text=BUTTONS["tests_site"],
                callback_data="tests_site"
            )
        ],
        [
            InlineKeyboardButton(
                text=BUTTONS["our_test"],
                callback_data="our_test"
            ),
            InlineKeyboardButton(
                text=BUTTONS["consultation"],
                callback_data="consultation"
            )
        ],
        [
            InlineKeyboardButton(
                text=BUTTONS["ai_analysis"],
                callback_data="ai_analysis"
            ),
            InlineKeyboardButton(
                text=BUTTONS["subscription"],
                callback_data="subscription"
            )
        ],
        [
            InlineKeyboardButton(
                text=BUTTONS["packages"],
                callback_data="packages"
            ),
            InlineKeyboardButton(
                text=BUTTONS["courses"],
                callback_data="courses"
            )
        ],
        [
            InlineKeyboardButton(
                text=BUTTONS["cards"],
                callback_data="cards"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_ai_analysis_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для выбора типа медиа для ИИ-анализа."""
    keyboard = [
        [
            InlineKeyboardButton(
                text="📸 Фото",
                callback_data="ai_photo"
            ),
            InlineKeyboardButton(
                text="🎥 Видео",
                callback_data="ai_video"
            )
        ],
        [
            InlineKeyboardButton(
                text="🎤 Голос",
                callback_data="ai_voice"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔙 Назад",
                callback_data="back_to_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_test_answer_keyboard(answers: list[str], question_id: int) -> InlineKeyboardMarkup:
    """Клавиатура с вариантами ответов для теста."""
    keyboard = []
    for i, answer in enumerate(answers):
        keyboard.append([
            InlineKeyboardButton(
                text=answer,
                callback_data=f"test_answer:{question_id}:{i}"
            )
        ])
    
    keyboard.append([
        InlineKeyboardButton(
            text="🔙 Назад",
            callback_data="back_to_menu"
        )
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_back_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура с кнопкой возврата."""
    keyboard = [
        [
            InlineKeyboardButton(
                text="🔙 Назад",
                callback_data="back_to_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_webview_keyboard(url: str, button_text: str) -> InlineKeyboardMarkup:
    """Клавиатура с WebView кнопкой."""
    keyboard = [
        [
            InlineKeyboardButton(
                text=button_text,
                web_app={"url": url}
            )
        ],
        [
            InlineKeyboardButton(
                text="🔙 Назад",
                callback_data="back_to_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_consultation_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура для консультации."""
    keyboard = [
        [
            InlineKeyboardButton(
                text="💬 Начать чат",
                callback_data="start_consultation"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔙 Назад",
                callback_data="back_to_menu"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
