# UrbanAI API

Django-based API for the UrbanAI project.

## Setup

1. Clone the repository
2. Create a virtual environment (optional):
   ```
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the server

To start the development server:

```
python manage.py migrate
python manage.py runserver
```

The API will be available at http://127.0.0.1:8000/api/

## API Endpoints

- `GET /api/` - Welcome message 

## Новый интерфейс карты и статистики

В проект добавлен современный монохромный UI для анализа городской инфраструктуры Бишкека:
- Карта на Leaflet с выбором районов и режимов анализа
- Статистическая панель с Chart.js, метриками и прогресс-барами
- Glassmorphism, адаптивность, анимации, particle-эффекты
- Bootstrap 5, Font Awesome, Chart.js, Leaflet

HTML-шаблон находится в `templates/map.html` (создать папку, если её нет). 