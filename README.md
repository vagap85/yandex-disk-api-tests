# Яндекс.Диск API Автотесты

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![pytest](https://img.shields.io/badge/pytest-8.0.0-green)](https://docs.pytest.org/)
[![requests](https://img.shields.io/badge/requests-2.31.0-orange)](https://requests.readthedocs.io/)
[![uv](https://img.shields.io/badge/uv-0.1.0-purple)](https://github.com/astral-sh/uv)

Автоматические тесты для REST API Яндекс.Диска, разработанные с использованием Python, Pytest и requests.

## 🎯 О проекте

Проект содержит автоматические тесты для проверки REST API Яндекс.Диска. Тесты покрывают основные методы API: GET, POST, PUT, DELETE. Все тесты используют тестовый OAuth-токен, полученный через [полигон Яндекс.Диска](https://yandex.ru/dev/disk/poligon/), и не требуют личного аккаунта пользователя.

### ✅ Статус тестов
![Tests Status](https://img.shields.io/badge/tests-20%20passed-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-85%25-yellow)

## 🛠 Технологии

- **Python 3.9+** - язык программирования
- **pytest 8.0.0** - фреймворк для тестирования
- **requests 2.31.0** - HTTP клиент
- **python-dotenv** - управление переменными окружения
- **uv** - быстрый менеджер пакетов
- **pytest-xdist** - параллельный запуск тестов

## 📦 Установка

### Предварительные требования
- Python 3.9 или выше
- [uv](https://github.com/astral-sh/uv) (рекомендуется) или pip
- Git

### Клонирование репозитория

```
git clone https://github.com/vagap85/yandex-disk-api-tests.git
cd yandex-disk-api-tests
Установка uv (если не установлен)
macOS/Linux:


curl -LsSf https://astral.sh/uv/install.sh | sh
Windows (PowerShell):

powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
Создание виртуального окружения и установка зависимостей
# Создание виртуального окружения
uv venv

# Активация (macOS/Linux)
source .venv/bin/activate

# Активация (Windows)
.venv\Scripts\activate

# Установка зависимостей
uv pip install -e .
uv pip install -e ".[dev]"  # для разработки
🔧 Настройка
Получение тестового токена
Перейдите на полигон Яндекс.Диска

Нажмите "Получить OAuth-токен"

Подтвердите доступ (войдите в аккаунт Яндекса)

Скопируйте полученный токен

Настройка переменных окружения

# Создайте файл .env из примера
cp .env.example .env

# Отредактируйте .env, вставьте ваш токен
YANDEX_DISK_TOKEN=ваш_токен_здесь
YANDEX_DISK_API_URL=https://cloud-api.yandex.net/v1/disk
🚀 Запуск тестов
Все тесты
pytest

С подробным выводом
pytest -v

По группам методов

## GET методы
pytest -m get -v

## POST методы
pytest -m post -v

## PUT методы
pytest -m put -v

## DELETE методы
pytest -m delete -v
По конкретным файлам

pytest tests/test_get_methods.py -v
pytest tests/test_post_methods.py -v
pytest tests/test_put_methods.py -v
pytest tests/test_delete_methods.py -v
Параллельный запуск

pytest -n auto -v
С отчетом о покрытии

pytest --cov=api --cov-report=term --cov-report=html
📁 Структура проекта
text
yandex-disk-api-tests/
├── api/                           # API клиент
│   ├── __init__.py
│   ├── client.py                  # Основной клиент
│   └── endpoints.py               # Эндпоинты API
├── config/                         # Конфигурация
│   ├── __init__.py
│   └── settings.py                 # Настройки приложения
├── tests/                          # Тесты
│   ├── __init__.py
│   ├── conftest.py                  # Фикстуры pytest
│   ├── test_get_methods.py          # GET тесты
│   ├── test_post_methods.py         # POST тесты
│   ├── test_put_methods.py          # PUT тесты
│   └── test_delete_methods.py       # DELETE тесты
├── utils/                           # Утилиты
│   ├── __init__.py
│   └── helpers.py                   # Вспомогательные функции
├── .env.example                      # Пример переменных окружения
├── .gitignore                        # Игнорируемые файлы
├── pyproject.toml                    # Зависимости проекта
├── pytest.ini                        # Конфигурация pytest
└── README.md                         # Документация

🧪 Тестовые сценарии
##GET методы (5 тестов)
✅ Получение информации о диске

✅ Получение метаинформации о ресурсе

✅ Получение списка файлов

✅ Обработка некорректных лимитов

✅ Обработка несуществующих ресурсов

##POST методы (4 теста)
✅ Копирование папок

✅ Перемещение папок

✅ Обработка конфликтов при копировании

✅ Обработка несуществующих ресурсов

##PUT методы (5 тестов)
✅ Создание папок

✅ Создание существующих папок

✅ Создание папок с различными типами путей

✅ Публикация ресурсов

✅ Отмена публикации

##DELETE методы (6 тестов)
✅ Удаление папок

✅ Удаление несуществующих ресурсов

✅ Удаление в корзину

✅ Полное удаление

✅ Очистка корзины

✅ Удаление пустых папок

📊 Результаты
text
===============================================================================
✅ Все тесты пройдены! 20 passed in 77.98s
===============================================================================

📋 Детальная статистика:
┌───────────────┬─────────────┬──────────┐
│ Метод         │ Количество  │ Статус   │
├───────────────┼─────────────┼──────────┤
│ GET           │ 5           │ ✅       │
│ POST          │ 4           │ ✅       │
│ PUT           │ 5           │ ✅       │
│ DELETE        │ 6           │ ✅       │
├───────────────┼─────────────┼──────────┤
│ ИТОГО         │ 20          │ 100%     │
└───────────────┴─────────────┴──────────┘

🤝 Контакты
GitHub: vagap85

Email: vagap85@gmail.com

📄 Лицензия
Этот проект распространяется под лицензией MIT. Подробности в файле LICENSE.

⭐ Если проект оказался полезным, поставьте звезду на GitHub!
