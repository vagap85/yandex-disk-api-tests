import requests
import logging
import time
from typing import Optional, Dict, Any
from config.settings import settings
from api.endpoints import Endpoints

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class YandexDiskClient:
    """Клиент для работы с API Яндекс.Диска"""

    def __init__(self):
        self.base_url = settings.BASE_URL
        self.headers = settings.headers
        self.endpoints = Endpoints()

    def _make_request(self, method: str, endpoint: str,
                      params: Optional[Dict] = None,
                      data: Optional[Dict] = None,
                      expected_status: int = 200) -> requests.Response:
        """Базовый метод для выполнения HTTP-запросов"""
        url = self.base_url + endpoint
        logger.info(f"Making {method} request to {url}")
        logger.info(f"Params: {params}")

        response = requests.request(
            method=method,
            url=url,
            headers=self.headers,
            params=params,
            json=data
        )

        logger.info(f"Response status: {response.status_code}")
        logger.info(f"Response body: {response.text[:200]}")

        assert response.status_code == expected_status, \
            f"Expected status {expected_status}, got {response.status_code}: {response.text}"

        return response

    # GET methods
    def get_disk_info(self) -> requests.Response:
        """Получение информации о диске"""
        return self._make_request("GET", self.endpoints.INFO)

    def get_resource_info(self, path: str) -> requests.Response:
        """Получение метаинформации о ресурсе"""
        params = {"path": path}
        return self._make_request("GET", self.endpoints.RESOURCES, params=params)

    def get_files_list(self, limit: int = 20) -> requests.Response:
        """Получение плоского списка файлов"""
        params = {"limit": limit}
        return self._make_request("GET", self.endpoints.FILES, params=params)

    def get_public_resources(self) -> requests.Response:
        """Получение списка опубликованных ресурсов"""
        return self._make_request("GET", self.endpoints.PUBLIC)

    # PUT methods
    def create_folder(self, path: str) -> requests.Response:
        """Создание папки"""
        params = {"path": path}
        return self._make_request("PUT", self.endpoints.RESOURCES, params=params, expected_status=201)

    def upload_file(self, path: str, url: str) -> requests.Response:
        """Загрузка файла по URL"""
        params = {
            "path": path,
            "url": url
        }
        return self._make_request("POST", self.endpoints.UPLOAD, params=params, expected_status=202)

    # POST methods
    def copy_resource(self, from_path: str, to_path: str) -> requests.Response:
        """Копирование ресурса"""
        params = {
            "from": from_path,
            "path": to_path
        }
        return self._make_request("POST", self.endpoints.COPY, params=params, expected_status=201)

    def move_resource(self, from_path: str, to_path: str) -> requests.Response:
        """Перемещение ресурса"""
        params = {
            "from": from_path,
            "path": to_path
        }
        return self._make_request("POST", self.endpoints.MOVE, params=params, expected_status=201)

    def publish_resource(self, path: str) -> requests.Response:
        """Публикация ресурса"""
        params = {"path": path}
        # Публикуем ресурс
        publish_response = self._make_request("PUT", self.endpoints.RESOURCES + "/publish", params=params)

        # Небольшая задержка для обновления метаданных
        time.sleep(1)

        # Возвращаем информацию о ресурсе, где должен быть public_key
        return self.get_resource_info(path)

    def unpublish_resource(self, path: str) -> requests.Response:
        """Отмена публикации ресурса"""
        params = {"path": path}
        # Отменяем публикацию
        unpublish_response = self._make_request("PUT", self.endpoints.RESOURCES + "/unpublish", params=params)

        # Небольшая задержка для обновления метаданных
        time.sleep(1)

        # Возвращаем информацию о ресурсе
        return self.get_resource_info(path)

    # DELETE methods
    def delete_resource(self, path: str, permanently: bool = False) -> requests.Response:
        """Удаление ресурса"""
        params = {
            "path": path,
            "permanently": str(permanently).lower()
        }
        return self._make_request("DELETE", self.endpoints.RESOURCES, params=params, expected_status=204)

    def clear_trash(self) -> requests.Response:
        """Очистка корзины"""
        return self._make_request("DELETE", self.endpoints.TRASH, expected_status=204)