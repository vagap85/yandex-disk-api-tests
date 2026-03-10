import pytest
import time

pytestmark = pytest.mark.delete


class TestDeleteMethods:
    """Тесты для DELETE методов"""

    def test_delete_folder(self, api_client):
        """Проверка удаления папки"""
        # Создаем папку
        folder_name = "test_delete_folder"
        folder_path = f"disk:/{folder_name}"
        api_client.create_folder(folder_path)

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

        # Даем время на обработку
        time.sleep(2)

        # Получаем список файлов в корзине
        trash_response = api_client._make_request("GET", "/trash/resources", params={"limit": 100})
        trash_data = trash_response.json()

        # Проверяем структуру ответа
        assert "_embedded" in trash_data, f"Нет поля _embedded в ответе: {trash_data}"
        assert "items" in trash_data["_embedded"], f"Нет поля items в _embedded: {trash_data['_embedded']}"

        # Ищем нашу папку
        trash_items = trash_data["_embedded"]["items"]
        found = False
        for item in trash_items:
            if item.get("name") == folder_name:
                found = True
                break

        assert found, f"Папка {folder_name} не найдена в корзине. Элементы в корзине: {[i.get('name') for i in trash_items]}"

    def test_delete_permanently(self, api_client, test_folder):
        """Проверка полного удаления ресурса"""
        folder_name = test_folder.split(":/")[1]

        response = api_client.delete_resource(test_folder, permanently=True)
        assert response.status_code == 204

        # Проверяем, что ресурс не в корзине
        time.sleep(1)

        trash_response = api_client._make_request("GET", "/trash/resources", params={"limit": 100})
        trash_items = trash_response.json().get("_embedded", {}).get("items", [])

        found = any(item.get("name") == folder_name for item in trash_items)
        assert not found, f"Папка {folder_name} не должна быть в корзине"

    def test_clear_trash(self, api_client, test_folder):
        """Проверка очистки корзины"""
        # Удаляем в корзину
        api_client.delete_resource(test_folder, permanently=False)

        # Даем время на обработку
        time.sleep(1)

        # Очищаем корзину (ожидаем 202, т.к. операция асинхронная)
        response = api_client._make_request("DELETE", "/trash/resources", expected_status=202)
        assert response.status_code == 202

        # Проверяем, что операция запущена
        response_data = response.json()
        assert "href" in response_data, f"Нет href в ответе: {response_data}"
        assert "method" in response_data, f"Нет method в ответе: {response_data}"
        assert response_data["method"] == "GET"

        # Можно подождать завершения операции
        operation_url = response_data["href"]
        time.sleep(2)

        # Проверяем, что корзина пуста
        trash_response = api_client._make_request("GET", "/trash/resources", params={"limit": 100})
        trash_data = trash_response.json()

        if "_embedded" in trash_data and "items" in trash_data["_embedded"]:
            assert len(trash_data["_embedded"]["items"]) == 0, "Корзина должна быть пуста"

    def test_delete_empty_folder(self, api_client):
        """Проверка удаления пустой папки"""
        folder_name = "test_empty_folder"
        folder_path = f"disk:/{folder_name}"

        api_client.create_folder(folder_path)
        response = api_client.delete_resource(folder_path)

        assert response.status_code == 204