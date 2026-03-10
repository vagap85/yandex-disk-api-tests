import pytest
import time
from utils.helpers import generate_unique_folder_name

pytestmark = pytest.mark.delete


class TestDeleteMethods:
    """Тесты для DELETE методов"""

    def test_delete_folder(self, api_client):
        """Проверка удаления папки"""
        folder_name = generate_unique_folder_name("delete_test")
        folder_path = f"disk:/{folder_name}"

        # Создаем папку
        response = api_client.create_folder(folder_path)
        assert response.status_code == 201

        # Удаляем папку
        response = api_client.delete_resource(folder_path)
        assert response.status_code == 204

        # Проверяем, что папка удалена
        with pytest.raises(AssertionError):
            api_client.get_resource_info(folder_path)

    def test_delete_nonexistent_resource(self, api_client):
        """Проверка удаления несуществующего ресурса"""
        with pytest.raises(AssertionError) as exc_info:
            api_client.delete_resource("disk:/nonexistent_123")

        assert "404" in str(exc_info.value)

    def test_delete_without_permanent(self, api_client, test_folder):
        """Проверка удаления в корзину"""
        folder_name = test_folder.split(":/")[1]

        response = api_client.delete_resource(test_folder, permanently=False)
        assert response.status_code == 204

        time.sleep(2)

        # Получаем содержимое корзины
        trash_response = api_client._make_request("GET", "/trash/resources", params={"limit": 100})
        trash_items = trash_response.json().get("_embedded", {}).get("items", [])

        # Ищем нашу папку в корзине
        found = any(item.get("name") == folder_name for item in trash_items)
        assert found, f"Папка {folder_name} не найдена в корзине"

    def test_delete_permanently(self, api_client, test_folder):
        """Проверка полного удаления ресурса"""
        folder_name = test_folder.split(":/")[1]

        response = api_client.delete_resource(test_folder, permanently=True)
        assert response.status_code == 204

        time.sleep(2)

        # Проверяем, что ресурс не в корзине
        trash_response = api_client._make_request("GET", "/trash/resources", params={"limit": 100})
        trash_items = trash_response.json().get("_embedded", {}).get("items", [])

        found = any(item.get("name") == folder_name for item in trash_items)
        assert not found, f"Папка {folder_name} не должна быть в корзине"

    def test_clear_trash(self, api_client, test_folder):
        """Проверка очистки корзины"""
        # Удаляем в корзину с повторными попытками при блокировке
        max_retries = 3
        for attempt in range(max_retries):
            try:
                api_client.delete_resource(test_folder, permanently=False)
                break
            except AssertionError as e:
                if "423" in str(e) and attempt < max_retries - 1:
                    print(f"⚠️ Ресурс заблокирован, повтор через 2с (попытка {attempt + 1}/{max_retries})")
                    time.sleep(2)
                    continue
                else:
                    raise e

        time.sleep(2)  # Даем время на обработку

        # Очищаем корзину
        response = api_client._make_request("DELETE", "/trash/resources", expected_status=202)
        assert response.status_code == 202
        assert "href" in response.json()

        time.sleep(3)  # Ждем очистки

        # Проверяем, что корзина пуста
        trash_response = api_client._make_request("GET", "/trash/resources", params={"limit": 100})
        trash_items = trash_response.json().get("_embedded", {}).get("items", [])
        assert len(trash_items) == 0, f"Корзина должна быть пуста, но содержит {len(trash_items)} элементов"

    def test_delete_empty_folder(self, api_client):
        """Проверка удаления пустой папки"""
        folder_name = generate_unique_folder_name("empty_test")
        folder_path = f"disk:/{folder_name}"

        api_client.create_folder(folder_path)
        response = api_client.delete_resource(folder_path)

        assert response.status_code == 204