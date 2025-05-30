import os
import requests
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USER = os.getenv("GITHUB_USER")
REPO_NAME = os.getenv("REPO_NAME")

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

base_url = "https://api.github.com"
repo_url = f"{base_url}/repos/{GITHUB_USER}/{REPO_NAME}"

# 1. Создание репозитория
print("Создаём репозиторий...")
response = requests.post(
    f"{base_url}/user/repos",
    headers=headers,
    json={ "name": REPO_NAME, "private": False }
)
print(f"Статус: {response.status_code}")
assert response.status_code == 201, f"Ошибка создания: {response.text}"

# 2. Проверка наличия
print("Проверяем наличие репозитория...")
repos_response = requests.get(f"{base_url}/users/{GITHUB_USER}/repos", headers=headers)
repo_names = [r['name'] for r in repos_response.json()]
assert REPO_NAME in repo_names, "Репозиторий не найден!"
print("Репозиторий найден.")

# 3. Удаление
print("Удаляем репозиторий...")
delete_response = requests.delete(repo_url, headers=headers)
assert delete_response.status_code == 204, "Ошибка удаления!"
print("Репозиторий успешно удалён.")