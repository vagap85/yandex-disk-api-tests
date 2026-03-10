import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем .env файл из корня проекта
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    """Настройки приложения"""

    # Базовый URL API Яндекс.Диска
    BASE_URL = os.getenv("YANDEX_DISK_API_URL", "https://cloud-api.yandex.net/v1/disk")

    # Токен для тестового пользователя (получен через полигон)
    # НЕ ИСПОЛЬЗУЙТЕ личный токен!
    OAUTH_TOKEN = os.getenv("YANDEX_DISK_TOKEN")

    if not OAUTH_TOKEN:
        raise ValueError(
            "y0__xCatrjaAxjblgMgst_A2RYw8Krn8wcN3BRZM8tipWBTkC6kPobJSjDEXg"
        )

    # Заголовки для авторизации
    @property
    def headers(self):
        return {
            "Authorization": f"OAuth {self.OAUTH_TOKEN}",
            "Content-Type": "application/json"
        }


settings = Settings()