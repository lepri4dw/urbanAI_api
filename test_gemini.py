import os
import logging
import traceback
import json
import google.generativeai as genai

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# API ключ для Google Gemini
API_KEY = "AIzaSyDvsUFB83k9nq5vOdDPEb4-8iOfAtfvWu0"

def test_gemini_api():
    """
    Тестирует подключение к Gemini API
    """
    try:
        logger.info("Настройка Gemini API с ключом")
        genai.configure(api_key=API_KEY)
        logger.info("Gemini API успешно настроен")
        
        logger.info("Создание экземпляра модели Gemini")
        model = genai.GenerativeModel('gemini-2.0-flash')
        logger.info("Модель Gemini успешно создана")
        
        logger.info("Отправка тестового запроса в Gemini API...")
        response = model.generate_content("Привет, это тестовый запрос. Ответь одним предложением.")
        logger.info("Получен ответ от Gemini API")
        
        logger.info(f"Тип ответа: {type(response)}")
        logger.info(f"Ответ: {response.text}")
        
        return True
    
    except Exception as e:
        logger.error(f"Ошибка при обращении к Gemini API: {str(e)}")
        logger.error(traceback.format_exc())
        return False

def test_load_scenario():
    """
    Тестирует загрузку данных сценария
    """
    try:
        scenario_number = 1
        file_path = f"api/data/scenario{scenario_number}_school_needed.json"
        
        logger.info(f"Загрузка данных сценария {scenario_number} из {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        logger.info(f"Данные сценария {scenario_number} успешно загружены")
        logger.info(f"Структура данных: {list(data.keys())}")
        
        return True
    
    except FileNotFoundError:
        logger.error(f"Файл сценария не найден: {file_path}")
        return False
    except json.JSONDecodeError:
        logger.error(f"Ошибка декодирования JSON в файле: {file_path}")
        return False
    except Exception as e:
        logger.error(f"Ошибка при загрузке данных сценария: {str(e)}")
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    logger.info("=== Тестирование Gemini API ===")
    api_result = test_gemini_api()
    logger.info(f"Результат теста API: {'Успешно' if api_result else 'Ошибка'}")
    
    logger.info("\n=== Тестирование загрузки сценария ===")
    scenario_result = test_load_scenario()
    logger.info(f"Результат теста загрузки сценария: {'Успешно' if scenario_result else 'Ошибка'}") 