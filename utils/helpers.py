import uuid
import time
from typing import Optional

def generate_unique_folder_name(prefix: str = "test_folder") -> str:
    """Генерация уникального имени папки для тестов"""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def generate_unique_file_name(prefix: str = "test_file", extension: str = "txt") -> str:
    """Генерация уникального имени файла для тестов"""
    return f"{prefix}_{uuid.uuid4().hex[:8]}.{extension}"

def wait_for_operation(client, operation_id: str, timeout: int = 30) -> bool:
    """Ожидание завершения операции"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        response = client._make_request("GET", f"/operations/{operation_id}")
        if response.json().get("status") == "success":
            return True
        time.sleep(1)
    return False