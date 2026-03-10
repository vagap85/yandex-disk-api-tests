import pytest
from utils.helpers import generate_unique_folder_name

pytestmark = pytest.mark.post


class TestPostMethods:
    """Тесты для POST методов"""

    def test_copy_folder(self, api_client, test_folder):
        """Проверка копирования папки"""
        new_folder_name = generate_unique_folder_name("copy")
        new_folder_path = f"disk:/{new_folder_name}"

        response = api_client.copy_resource(test_folder, new_folder_path)
        data = response.json()

        assert "href" in data  # Ссылка на операцию
        assert "method" in data
        assert data["method"] == "GET"

        # Проверяем, что папка создалась
        api_client.get_resource_info(new_folder_path)

    def test_copy_nonexistent_resource(self, api_client):
        """Проверка копирования несуществующего ресурса"""
        with pytest.raises(AssertionError) as exc_info:
            api_client.copy_resource(
                "disk:/nonexistent",
                "disk:/new_folder"
            )

        assert "404" in str(exc_info.value)

    def test_copy_to_existing_destination(self, api_client, test_folder):
        """Проверка копирования в существующую папку"""
        with pytest.raises(AssertionError) as exc_info:
            api_client.copy_resource(test_folder, test_folder)

        assert "409" in str(exc_info.value)

    def test_move_folder(self, api_client, test_folder):
        """Проверка перемещения папки"""
        new_folder_name = generate_unique_folder_name("moved")
        new_parent = f"disk:/{new_folder_name}"

        # Создаем целевую папку
        api_client.create_folder(new_parent)

        moved_path = f"{new_parent}/subfolder"

        response = api_client.move_resource(test_folder, moved_path)
        data = response.json()

        assert "href" in data

        # Проверяем, что папка переместилась
        api_client.get_resource_info(moved_path)