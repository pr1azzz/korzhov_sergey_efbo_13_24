# Task Manager API

## Команды

```bash
# Создание виртуального окружения
python -m venv .venv

# Активация (Linux/Mac)
source .venv/bin/activate
# Активация (Windows)
.venv\Scripts\activate

# Установка зависимостей
pip install -r requirements.txt

# Запуск приложения
uvicorn app.main:app --reload

# Запуск тестов
pytest tests/ -v

# Запуск через Docker
docker compose up --build