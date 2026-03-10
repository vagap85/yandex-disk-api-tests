import pytest
import json

pytestmark = pytest.mark.get


class TestGetMethods:
    """Тесты для GET методов"""

    def test_get_disk_info(self, api_client):
        """Проверка получения информации о диске"""
        response = api_client.get_disk_info()
        data = response.json()

        assert "total_space" in data
        assert "used_space" in data
        assert "trash_size" in data
        assert "system_folders" in data

    def test_get_resource_info(self, api_client, test_folder):
        """Проверка получения информации о ресурсе"""
        response = api_client.get_resource_info(test_folder)
        data = response.json()

        assert data["type"] == "dir"
        assert data["path"] == test_folder
        assert "name" in data
        assert "created" in data
        assert "modified" in data

    def test_get_files_list(self, api_client):
        """Проверка получения списка файлов"""
        response = api_client.get_files_list(limit=5)
        data = response.json()

        assert "items" in data
        assert len(data["items"]) <= 5
        assert "limit" in data
        assert "offset" in data

    def test_get_files_list_with_invalid_limit(self, api_client):
        """Проверка обработки некорректного лимита"""
        response = api_client.get_files_list(limit=1000)
        data = response.json()

        # API должно вернуть ошибку или скорректировать лимит
        assert "items" in data

    def test_get_nonexistent_resource(self, api_client):
        """Проверка получения несуществующего ресурса"""
        with pytest.raises(AssertionError) as exc_info:
            api_client.get_resource_info("disk:/nonexistent_folder_12345")

        assert "404" in str(exc_info.value)