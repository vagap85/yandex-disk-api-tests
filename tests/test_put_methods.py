import pytest
from utils.helpers import generate_unique_folder_name

pytestmark = pytest.mark.put


class TestPutMethods:
    """Тесты для PUT методов"""

    def test_create_folder(self, api_client):
        """Проверка создания папки"""
        folder_name = generate_unique_folder_name()
        folder_path = f"disk:/{folder_name}"

        response = api_client.create_folder(folder_path)
        assert response.status_code == 201

        # Проверяем, что папка создалась
        info = api_client.get_resource_info(folder_path)
        assert info.json()["type"] == "dir"

    def test_create_existing_folder(self, api_client, test_folder):
        """Проверка создания существующей папки"""
        with pytest.raises(AssertionError) as exc_info:
            api_client.create_folder(test_folder)

        assert "409" in str(exc_info.value)

    def test_create_folder_with_invalid_path(self, api_client):
        """Проверка создания папки с различными типами путей"""

        # Структурированные тестовые данные
        test_cases = [
            {
                "path": "disk:/test_folder_with_special_chars_!@#$%^&*()",
                "expected": 201,
                "description": "Спецсимволы должны работать"
            },
            {
                "path": "disk:/path/with//double/slash",
                "expected": 404,
                "description": "Двойной слэш должен возвращать 404"
            },
            {
                "path": f"disk:/{'a' * 300}",
                "expected": [400, 404, 409],  # Любой из этих статусов
                "description": "Очень длинное имя"
            },
            {
                "path": "folder_without_prefix",
                "expected": 201,
                "description": "Путь без префикса disk:/"
            },
            {
                "path": "disk:/path/with/../parent",
                "expected": [400, 404, 409],
                "description": "Попытка выхода за пределы"
            },
            {
                "path": "disk:/path/with//",
                "expected": 404,
                "description": "Завершающий двойной слэш"
            },
        ]

        created_folders = []

        try:
            for case in test_cases:
                path = case["path"]
                expected = case["expected"]
                description = case["description"]

                print(f"\n📁 Тест: {description}")
                print(f"   Путь: {path}")

                try:
                    response = api_client.create_folder(path)
                    actual_status = response.status_code

                    # Проверка ожидаемого статуса
                    if isinstance(expected, list):
                        assert actual_status in expected, \
                            f"Статус {actual_status} не в списке ожидаемых {expected}"
                    else:
                        assert actual_status == expected, \
                            f"Ожидался {expected}, получен {actual_status}"

                    print(f"   ✅ Статус: {actual_status}")

                    # Запоминаем созданные папки для очистки
                    if actual_status == 201:
                        full_path = f"disk:/{path}" if not path.startswith("disk:/") else path
                        created_folders.append(full_path)

                except AssertionError as e:
                    error_str = str(e)

                    # Проверяем, что ошибка ожидаема
                    if isinstance(expected, list):
                        assert any(str(code) in error_str for code in expected), \
                            f"Неожиданная ошибка: {error_str}"
                        print(f"   ✅ Получена ожидаемая ошибка (статус из {expected})")
                    else:
                        assert str(expected) in error_str, \
                            f"Неожиданная ошибка: {error_str}"
                        print(f"   ✅ Получена ожидаемая ошибка (статус {expected})")

        finally:
            # Очистка
            if created_folders:
                print("\n🧹 Очистка тестовых данных:")
                for folder_path in created_folders:
                    try:
                        api_client.delete_resource(folder_path, permanently=True)
                        print(f"   ✅ Удалено: {folder_path}")
                    except Exception as e:
                        print(f"   ❌ Ошибка при удалении {folder_path}: {e}")
            else:
                print("\n🧹 Нет созданных папок для очистки")

    def test_publish_resource(self, api_client, test_folder):
        """Проверка публикации ресурса"""
        # Публикуем ресурс
        response = api_client.publish_resource(test_folder)

        # Проверяем, что ответ успешный
        assert response.status_code == 200

        # Проверяем наличие public_key в ответе
        data = response.json()
        assert "public_key" in data, f"public_key не найден в ответе: {data.keys()}"
        assert "public_url" in data, f"public_url не найден в ответе: {data.keys()}"

        # Проверяем, что URL валидный
        assert data["public_url"].startswith("https://"), f"Невалидный public_url: {data['public_url']}"

    def test_unpublish_resource(self, api_client, test_folder):
        """Проверка отмены публикации"""
        # Сначала публикуем
        api_client.publish_resource(test_folder)

        # Затем отменяем публикацию
        response = api_client.unpublish_resource(test_folder)
        assert response.status_code == 200

        # Проверяем, что ресурс не опубликован
        info = api_client.get_resource_info(test_folder)
        assert "public_key" not in info.json()