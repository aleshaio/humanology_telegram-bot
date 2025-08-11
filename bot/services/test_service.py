"""Сервис для работы с тестами."""

import json
import os
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

from bot.database.database import db
from bot.data.messages import TEST_MESSAGES


class TestService:
    """Сервис для работы с тестами."""
    
    def __init__(self):
        """Инициализация сервиса."""
        self.test_data_path = Path(__file__).parent.parent / "data" / "test_data.json"
        self.test_data = self._load_test_data()
    
    def _load_test_data(self) -> Dict[str, Any]:
        """Загрузка данных теста из JSON."""
        try:
            with open(self.test_data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Возвращаем базовые данные если файл не найден
            return {
                "questions": [],
                "types": {}
            }
    
    def get_question(self, question_id: int) -> Optional[Dict[str, Any]]:
        """Получение вопроса по ID."""
        questions = self.test_data.get("questions", [])
        for question in questions:
            if question["id"] == question_id:
                return question
        return None
    
    def get_total_questions(self) -> int:
        """Получение общего количества вопросов."""
        return len(self.test_data.get("questions", []))
    
    def calculate_test_result(self, answers: List[int]) -> Dict[str, Any]:
        """Расчет результата теста на основе ответов."""
        if not answers or len(answers) != self.get_total_questions():
            return {}
        
        # Подсчет баллов для каждого типа
        type_scores = {
            "Идеалист": 0,
            "Социал": 0,
            "Прагматик": 0,
            "Аналитик": 0
        }
        
        # Матрица ответов (вопрос -> ответ -> тип)
        answer_matrix = {
            0: "Идеалист",    # Первый вариант ответа
            1: "Социал",      # Второй вариант ответа
            2: "Прагматик",   # Третий вариант ответа
            3: "Аналитик"     # Четвертый вариант ответа
        }
        
        for answer in answers:
            if answer in answer_matrix:
                type_scores[answer_matrix[answer]] += 1
        
        # Определение основного типа
        main_type = max(type_scores, key=type_scores.get)
        main_type_score = type_scores[main_type]
        
        # Расчет процентов
        total_questions = self.get_total_questions()
        type_percent = round((main_type_score / total_questions) * 100)
        
        # Получение дополнительной информации о типе
        type_info = self.test_data.get("types", {}).get(main_type, {})
        
        return {
            "type_name": main_type,
            "type_percent": type_percent,
            "square": type_info.get("square", "Не определено"),
            "role": type_info.get("role", "Не определено"),
            "description": type_info.get("description", ""),
            "all_scores": type_scores
        }
    
    async def save_test_result(
        self, 
        user_id: int, 
        answers: List[int], 
        result: Dict[str, Any]
    ) -> bool:
        """Сохранение результата теста в БД."""
        try:
            await db.save_test_result(
                user_id=user_id,
                test_type="our_test",
                result_data={
                    "answers": answers,
                    "result": result
                }
            )
            return True
        except Exception as e:
            print(f"Ошибка сохранения результата теста: {e}")
            return False
    
    def get_test_progress_text(self, current: int, total: int) -> str:
        """Получение текста прогресса теста."""
        return TEST_MESSAGES["progress"].format(current=current, total=total)
    
    def get_test_welcome_text(self) -> str:
        """Получение приветственного текста для теста."""
        return f"{TEST_MESSAGES['welcome']}\n\n{TEST_MESSAGES['instructions']}"
    
    def get_test_completion_text(self) -> str:
        """Получение текста завершения теста."""
        return TEST_MESSAGES["test_completed"]


# Глобальный экземпляр сервиса
test_service = TestService()
