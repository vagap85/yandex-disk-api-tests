import pytest
from api.client import YandexDiskClient
from utils.helpers import generate_unique_folder_name


@pytest.fixture(scope="session")
def api_client():
    """Фикстура для создания клиента API"""
    return YandexDiskClient()


@pytest.fixture
def test_folder(api_client):
    """Фикстура для создания тестовой папки и её очистки после теста"""
    folder_name = generate_unique_folder_name()
    folder_path = f"disk:/{folder_name}"

    # Создаем папку
    api_client.create_folder(folder_path)

    yield folder_path

    # Очищаем после теста
    try:
        api_client.delete_resource(folder_path, permanently=True)
    except:
        pass  # Игнорируем ошибки при очистке


@pytest.fixture
def test_file_url():
    """Фикстура с URL тестового файла"""
    return "https://example.com/test.txt"