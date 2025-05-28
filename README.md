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