"""Сервис для работы с API сайта."""

import httpx
from typing import Dict, Any, Optional, List
from config import settings


class SiteAPIService:
    """Сервис для работы с API сайта."""
    
    def __init__(self):
        """Инициализация сервиса."""
        self.base_url = settings.site_api_url.rstrip('/')
        self.api_key = settings.site_api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Выполнение HTTP-запроса к API."""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                url = f"{self.base_url}{endpoint}"
                
                if method.upper() == "GET":
                    response = await client.get(url, headers=self.headers)
                elif method.upper() == "POST":
                    response = await client.post(url, headers=self.headers, json=data)
                else:
                    return None
                
                if response.status_code == 200:
                    return response.json()
                else:
                    print(f"API error: {response.status_code} - {response.text}")
                    return None
                    
        except Exception as e:
            print(f"Ошибка API запроса: {e}")
            return None
    
    async def get_tests_list(self) -> Optional[List[Dict[str, Any]]]:
        """Получение списка тестов с сайта."""
        return await self._make_request("GET", "/api/tests")
    
    async def get_test_questions(self, test_id: int) -> Optional[List[Dict[str, Any]]]:
        """Получение вопросов теста по ID."""
        return await self._make_request("GET", f"/api/tests/{test_id}/questions")
    
    async def submit_test_result(
        self, 
        test_id: int, 
        user_id: int, 
        answers: List[int]
    ) -> Optional[Dict[str, Any]]:
        """Отправка результатов теста на сайт."""
        data = {
            "test_id": test_id,
            "telegram_user_id": user_id,
            "answers": answers,
            "timestamp": "2024-01-01T00:00:00Z"  # В реальном проекте текущее время
        }
        return await self._make_request("POST", f"/api/tests/{test_id}/results", data)
    
    async def check_subscription_status(self, telegram_user_id: int) -> Optional[Dict[str, Any]]:
        """Проверка статуса подписки по Telegram user_id."""
        return await self._make_request("GET", f"/api/users/{telegram_user_id}/subscription")
    
    async def check_package_balance(self, telegram_user_id: int) -> Optional[Dict[str, Any]]:
        """Проверка баланса пакетов по Telegram user_id."""
        return await self._make_request("GET", f"/api/users/{telegram_user_id}/packages")
    
    async def get_user_profile(self, telegram_user_id: int) -> Optional[Dict[str, Any]]:
        """Получение профиля пользователя с сайта."""
        return await self._make_request("GET", f"/api/users/{telegram_user_id}/profile")
    
    async def is_api_available(self) -> bool:
        """Проверка доступности API."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/health")
                return response.status_code == 200
        except Exception:
            return False
    
    def get_webview_url(self, section: str, user_id: Optional[int] = None) -> str:
        """Формирование URL для WebView."""
        base_url = self.base_url.replace("/api", "")
        
        if section == "handbook":
            url = f"{base_url}/handbook"
        elif section == "tests":
            url = f"{base_url}/tests"
        elif section == "subscription":
            url = f"{base_url}/subscription"
        elif section == "packages":
            url = f"{base_url}/packages"
        elif section == "courses":
            url = f"{base_url}/courses"
        elif section == "cards":
            url = f"{base_url}/cards"
        else:
            url = base_url
        
        # Добавляем user_id если передан
        if user_id:
            separator = "&" if "?" in url else "?"
            url += f"{separator}user_id={user_id}"
        
        return url


# Глобальный экземпляр сервиса
site_api_service = SiteAPIService()
