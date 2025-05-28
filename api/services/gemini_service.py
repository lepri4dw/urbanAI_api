"""
Сервис для работы с Google Gemini API
"""
import json
import logging
import traceback
import sys
import os
import google.generativeai as genai
from api.gemini_prompts import SCHOOL_ANALYSIS_PROMPT, BISHKEK_SCHOOL_ANALYSIS_PROMPT

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# API ключ для Google Gemini
API_KEY = "AIzaSyDvsUFB83k9nq5vOdDPEb4-8iOfAtfvWu0"

# Проверка API ключа
if not API_KEY or API_KEY == "":
    logger.error("API ключ для Gemini не установлен")
    print("API ключ для Gemini не установлен", file=sys.stderr)
    # Попытка получить ключ из переменной окружения
    API_KEY = os.environ.get("GEMINI_API_KEY", "")
    if API_KEY:
        logger.info("API ключ получен из переменной окружения")
        print("API ключ получен из переменной окружения", file=sys.stderr)
    else:
        logger.error("API ключ не найден в переменных окружения")
        print("API ключ не найден в переменных окружения", file=sys.stderr)

# Настройка Gemini API
try:
    logger.info("Настройка Gemini API с ключом")
    print("Настройка Gemini API с ключом", file=sys.stderr)
    genai.configure(api_key=API_KEY)
    logger.info("Gemini API успешно настроен")
    print("Gemini API успешно настроен", file=sys.stderr)
    
    # Проверка подключения
    try:
        logger.info("Проверка подключения к Gemini API")
        print("Проверка подключения к Gemini API", file=sys.stderr)
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content("Test connection")
        logger.info("Подключение к Gemini API успешно")
        print("Подключение к Gemini API успешно", file=sys.stderr)
        print(f"Тестовый ответ: {response.text}", file=sys.stderr)
    except Exception as e:
        logger.error(f"Ошибка при проверке подключения к Gemini API: {str(e)}")
        print(f"Ошибка при проверке подключения к Gemini API: {str(e)}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
except Exception as e:
    logger.error(f"Ошибка при настройке Gemini API: {str(e)}")
    print(f"Ошибка при настройке Gemini API: {str(e)}", file=sys.stderr)
    print(traceback.format_exc(), file=sys.stderr)

def analyze_school_need(data_json):
    """
    Анализирует необходимость строительства школы на основе предоставленных данных
    
    Args:
        data_json (dict): JSON с данными о районе
        
    Returns:
        str: Ответ от Gemini API с анализом
    """
    try:
        logger.info("Подготовка запроса к Gemini API для анализа необходимости школы")
        print("Подготовка запроса к Gemini API для анализа необходимости школы", file=sys.stderr)
        
        # Проверка API ключа перед запросом
        if not API_KEY or API_KEY == "":
            error_msg = "API ключ для Gemini не установлен. Невозможно выполнить запрос."
            logger.error(error_msg)
            print(error_msg, file=sys.stderr)
            return error_msg
        
        # Преобразуем данные в строку JSON для вставки в промпт
        logger.info("Преобразование данных в строку JSON")
        print("Преобразование данных в строку JSON", file=sys.stderr)
        data_str = json.dumps(data_json, ensure_ascii=False, indent=2)
        logger.info(f"Размер данных JSON: {len(data_str)} символов")
        print(f"Размер данных JSON: {len(data_str)} символов", file=sys.stderr)
        
        # Формируем промпт с данными
        logger.info("Формирование промпта с данными")
        print("Формирование промпта с данными", file=sys.stderr)
        prompt = SCHOOL_ANALYSIS_PROMPT.format(data=data_str)
        logger.info(f"Размер промпта: {len(prompt)} символов")
        print(f"Размер промпта: {len(prompt)} символов", file=sys.stderr)
        
        logger.info("Создание экземпляра модели Gemini")
        print("Создание экземпляра модели Gemini", file=sys.stderr)
        # Настройка модели
        model = genai.GenerativeModel('gemini-2.0-flash')
        logger.info("Модель Gemini успешно создана")
        print("Модель Gemini успешно создана", file=sys.stderr)
        
        logger.info("Отправка запроса в Gemini API...")
        print("Отправка запроса в Gemini API...", file=sys.stderr)
        # Отправка запроса
        try:
            response = model.generate_content(prompt)
            logger.info("Получен ответ от Gemini API")
            print("Получен ответ от Gemini API", file=sys.stderr)
            
            logger.info(f"Тип ответа: {type(response)}")
            print(f"Тип ответа: {type(response)}", file=sys.stderr)
            
            # Проверка наличия текста в ответе
            if not hasattr(response, 'text'):
                logger.error("Ответ от Gemini API не содержит текста")
                print("Ответ от Gemini API не содержит текста", file=sys.stderr)
                print(f"Содержимое ответа: {response}", file=sys.stderr)
                return "Ошибка: ответ от Gemini API не содержит текста"
            
            logger.info(f"Размер ответа: {len(response.text)} символов")
            print(f"Размер ответа: {len(response.text)} символов", file=sys.stderr)
            print(f"Начало ответа: {response.text[:200]}...", file=sys.stderr)
            
            return response.text
            
        except genai.types.generation_types.BlockedPromptException as e:
            error_msg = f"Промпт заблокирован системой безопасности Gemini: {str(e)}"
            logger.error(error_msg)
            print(error_msg, file=sys.stderr)
            return error_msg
            
        except genai.types.generation_types.StopCandidateException as e:
            error_msg = f"Генерация ответа остановлена системой Gemini: {str(e)}"
            logger.error(error_msg)
            print(error_msg, file=sys.stderr)
            return error_msg
            
        except Exception as e:
            error_msg = f"Ошибка при генерации ответа: {str(e)}"
            logger.error(error_msg)
            logger.error(traceback.format_exc())
            print(error_msg, file=sys.stderr)
            print(traceback.format_exc(), file=sys.stderr)
            return error_msg
    
    except Exception as e:
        logger.error(f"Ошибка при обращении к Gemini API: {str(e)}")
        print(f"Ошибка при обращении к Gemini API: {str(e)}", file=sys.stderr)
        logger.error(traceback.format_exc())
        print(traceback.format_exc(), file=sys.stderr)
        return f"Произошла ошибка при анализе данных: {str(e)}"

def analyze_bishkek_school_need(district_name):
    """
    Анализирует необходимость строительства школ в указанном районе Бишкека
    
    Args:
        district_name (str): Название района Бишкека
        
    Returns:
        str: Ответ от Gemini API с анализом
    """
    try:
        logger.info(f"Подготовка запроса к Gemini API для анализа необходимости школ в районе {district_name}")
        print(f"Подготовка запроса к Gemini API для анализа необходимости школ в районе {district_name}", file=sys.stderr)
        
        # Проверка API ключа перед запросом
        if not API_KEY or API_KEY == "":
            error_msg = "API ключ для Gemini не установлен. Невозможно выполнить запрос."
            logger.error(error_msg)
            print(error_msg, file=sys.stderr)
            return error_msg
        
        # Загружаем исторические данные
        logger.info("Загрузка исторических данных по Бишкеку")
        print("Загрузка исторических данных по Бишкеку", file=sys.stderr)
        historical_data = load_bishkek_historical_data()
        if not historical_data:
            logger.error("Не удалось загрузить исторические данные")
            print("Не удалось загрузить исторические данные", file=sys.stderr)
            return "Ошибка: не удалось загрузить исторические данные"
        logger.info("Исторические данные успешно загружены")
        print("Исторические данные успешно загружены", file=sys.stderr)
        
        # Загружаем прогнозные данные
        logger.info("Загрузка прогнозных данных по Бишкеку")
        print("Загрузка прогнозных данных по Бишкеку", file=sys.stderr)
        forecast_data = load_bishkek_forecast_data()
        if not forecast_data:
            logger.error("Не удалось загрузить прогнозные данные")
            print("Не удалось загрузить прогнозные данные", file=sys.stderr)
            return "Ошибка: не удалось загрузить прогнозные данные"
        logger.info("Прогнозные данные успешно загружены")
        print("Прогнозные данные успешно загружены", file=sys.stderr)
        
        # Объединяем данные
        logger.info("Объединение данных")
        print("Объединение данных", file=sys.stderr)
        combined_data = {
            "historical_data": historical_data,
            "forecast_data": forecast_data
        }
        
        # Преобразуем данные в строку JSON для вставки в промпт
        logger.info("Преобразование данных в строку JSON")
        print("Преобразование данных в строку JSON", file=sys.stderr)
        data_str = json.dumps(combined_data, ensure_ascii=False, indent=2)
        logger.info(f"Размер данных JSON: {len(data_str)} символов")
        print(f"Размер данных JSON: {len(data_str)} символов", file=sys.stderr)
        
        # Формируем промпт с данными
        logger.info("Формирование промпта с данными")
        print("Формирование промпта с данными", file=sys.stderr)
        prompt = BISHKEK_SCHOOL_ANALYSIS_PROMPT.format(district=district_name, data=data_str)
        logger.info(f"Размер промпта: {len(prompt)} символов")
        print(f"Размер промпта: {len(prompt)} символов", file=sys.stderr)
        
        logger.info("Создание экземпляра модели Gemini")
        print("Создание экземпляра модели Gemini", file=sys.stderr)
        # Настройка модели
        model = genai.GenerativeModel('gemini-2.0-flash')
        logger.info("Модель Gemini успешно создана")
        print("Модель Gemini успешно создана", file=sys.stderr)
        
        logger.info(f"Отправка запроса в Gemini API для анализа района {district_name}...")
        print(f"Отправка запроса в Gemini API для анализа района {district_name}...", file=sys.stderr)
        # Отправка запроса
        try:
            response = model.generate_content(prompt)
            logger.info(f"Получен ответ от Gemini API для района {district_name}")
            print(f"Получен ответ от Gemini API для района {district_name}", file=sys.stderr)
            
            logger.info(f"Тип ответа: {type(response)}")
            print(f"Тип ответа: {type(response)}", file=sys.stderr)
            
            # Проверка наличия текста в ответе
            if not hasattr(response, 'text'):
                logger.error("Ответ от Gemini API не содержит текста")
                print("Ответ от Gemini API не содержит текста", file=sys.stderr)
                print(f"Содержимое ответа: {response}", file=sys.stderr)
                return "Ошибка: ответ от Gemini API не содержит текста"
            
            logger.info(f"Размер ответа: {len(response.text)} символов")
            print(f"Размер ответа: {len(response.text)} символов", file=sys.stderr)
            print(f"Начало ответа: {response.text[:200]}...", file=sys.stderr)
            
            return response.text
            
        except genai.types.generation_types.BlockedPromptException as e:
            error_msg = f"Промпт заблокирован системой безопасности Gemini: {str(e)}"
            logger.error(error_msg)
            print(error_msg, file=sys.stderr)
            return error_msg
            
        except genai.types.generation_types.StopCandidateException as e:
            error_msg = f"Генерация ответа остановлена системой Gemini: {str(e)}"
            logger.error(error_msg)
            print(error_msg, file=sys.stderr)
            return error_msg
            
        except Exception as e:
            error_msg = f"Ошибка при генерации ответа: {str(e)}"
            logger.error(error_msg)
            logger.error(traceback.format_exc())
            print(error_msg, file=sys.stderr)
            print(traceback.format_exc(), file=sys.stderr)
            return error_msg
    
    except Exception as e:
        logger.error(f"Ошибка при обращении к Gemini API: {str(e)}")
        print(f"Ошибка при обращении к Gemini API: {str(e)}", file=sys.stderr)
        logger.error(traceback.format_exc())
        print(traceback.format_exc(), file=sys.stderr)
        return f"Произошла ошибка при анализе данных: {str(e)}"

def load_scenario_data(scenario_number):
    """
    Загружает данные сценария из JSON файла
    
    Args:
        scenario_number (int): Номер сценария (1, 2 или 3)
        
    Returns:
        dict: Данные сценария в формате JSON
    """
    scenario_files = {
        1: "api/data/scenario1_school_needed.json",
        2: "api/data/scenario2_school_not_needed.json",
        3: "api/data/scenario3_school_needed_future.json"
    }
    
    if scenario_number not in scenario_files:
        logger.error(f"Неизвестный сценарий: {scenario_number}")
        print(f"Неизвестный сценарий: {scenario_number}", file=sys.stderr)
        return None
    
    file_path = scenario_files[scenario_number]
    
    try:
        logger.info(f"Загрузка данных сценария {scenario_number} из {file_path}")
        print(f"Загрузка данных сценария {scenario_number} из {file_path}", file=sys.stderr)
        
        # Проверка существования файла
        if not os.path.exists(file_path):
            logger.error(f"Файл сценария не найден: {file_path}")
            print(f"Файл сценария не найден: {file_path}", file=sys.stderr)
            print(f"Текущая директория: {os.getcwd()}", file=sys.stderr)
            print(f"Содержимое директории api/data: {os.listdir('api/data') if os.path.exists('api/data') else 'директория не существует'}", file=sys.stderr)
            return None
        
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        logger.info(f"Данные сценария {scenario_number} успешно загружены")
        print(f"Данные сценария {scenario_number} успешно загружены", file=sys.stderr)
        print(f"Структура данных: {list(data.keys())}", file=sys.stderr)
        return data
    
    except FileNotFoundError:
        logger.error(f"Файл сценария не найден: {file_path}")
        print(f"Файл сценария не найден: {file_path}", file=sys.stderr)
        return None
    except json.JSONDecodeError:
        logger.error(f"Ошибка декодирования JSON в файле: {file_path}")
        print(f"Ошибка декодирования JSON в файле: {file_path}", file=sys.stderr)
        return None
    except Exception as e:
        logger.error(f"Ошибка при загрузке данных сценария: {str(e)}")
        print(f"Ошибка при загрузке данных сценария: {str(e)}", file=sys.stderr)
        logger.error(traceback.format_exc())
        print(traceback.format_exc(), file=sys.stderr)
        return None

def load_bishkek_historical_data():
    """
    Загружает исторические данные по Бишкеку
    
    Returns:
        dict: Исторические данные в формате JSON
    """
    file_path = "api/data/bishkek_historical_data.json"
    
    try:
        logger.info(f"Загрузка исторических данных по Бишкеку из {file_path}")
        print(f"Загрузка исторических данных по Бишкеку из {file_path}", file=sys.stderr)
        
        # Проверка существования файла
        if not os.path.exists(file_path):
            logger.error(f"Файл с историческими данными не найден: {file_path}")
            print(f"Файл с историческими данными не найден: {file_path}", file=sys.stderr)
            print(f"Текущая директория: {os.getcwd()}", file=sys.stderr)
            print(f"Содержимое директории api/data: {os.listdir('api/data') if os.path.exists('api/data') else 'директория не существует'}", file=sys.stderr)
            return None
        
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        logger.info("Исторические данные по Бишкеку успешно загружены")
        print("Исторические данные по Бишкеку успешно загружены", file=sys.stderr)
        return data
    
    except FileNotFoundError:
        logger.error(f"Файл с историческими данными не найден: {file_path}")
        print(f"Файл с историческими данными не найден: {file_path}", file=sys.stderr)
        return None
    except json.JSONDecodeError:
        logger.error(f"Ошибка декодирования JSON в файле: {file_path}")
        print(f"Ошибка декодирования JSON в файле: {file_path}", file=sys.stderr)
        return None
    except Exception as e:
        logger.error(f"Ошибка при загрузке исторических данных: {str(e)}")
        print(f"Ошибка при загрузке исторических данных: {str(e)}", file=sys.stderr)
        logger.error(traceback.format_exc())
        print(traceback.format_exc(), file=sys.stderr)
        return None

def load_bishkek_forecast_data():
    """
    Загружает прогнозные данные по Бишкеку
    
    Returns:
        dict: Прогнозные данные в формате JSON
    """
    file_path = "api/data/bishkek_forecast_data.json"
    
    try:
        logger.info(f"Загрузка прогнозных данных по Бишкеку из {file_path}")
        print(f"Загрузка прогнозных данных по Бишкеку из {file_path}", file=sys.stderr)
        
        # Проверка существования файла
        if not os.path.exists(file_path):
            logger.error(f"Файл с прогнозными данными не найден: {file_path}")
            print(f"Файл с прогнозными данными не найден: {file_path}", file=sys.stderr)
            print(f"Текущая директория: {os.getcwd()}", file=sys.stderr)
            print(f"Содержимое директории api/data: {os.listdir('api/data') if os.path.exists('api/data') else 'директория не существует'}", file=sys.stderr)
            return None
        
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        logger.info("Прогнозные данные по Бишкеку успешно загружены")
        print("Прогнозные данные по Бишкеку успешно загружены", file=sys.stderr)
        return data
    
    except FileNotFoundError:
        logger.error(f"Файл с прогнозными данными не найден: {file_path}")
        print(f"Файл с прогнозными данными не найден: {file_path}", file=sys.stderr)
        return None
    except json.JSONDecodeError:
        logger.error(f"Ошибка декодирования JSON в файле: {file_path}")
        print(f"Ошибка декодирования JSON в файле: {file_path}", file=sys.stderr)
        return None
    except Exception as e:
        logger.error(f"Ошибка при загрузке прогнозных данных: {str(e)}")
        print(f"Ошибка при загрузке прогнозных данных: {str(e)}", file=sys.stderr)
        logger.error(traceback.format_exc())
        print(traceback.format_exc(), file=sys.stderr)
        return None

def get_bishkek_districts():
    """
    Возвращает список районов Бишкека
    
    Returns:
        list: Список районов Бишкека
    """
    try:
        logger.info("Получение списка районов Бишкека")
        print("Получение списка районов Бишкека", file=sys.stderr)
        historical_data = load_bishkek_historical_data()
        if historical_data and "city_info" in historical_data:
            districts = historical_data["city_info"]["administrative_divisions"]
            logger.info(f"Получен список районов: {districts}")
            print(f"Получен список районов: {districts}", file=sys.stderr)
            return districts
        logger.warning("Не удалось получить список районов")
        print("Не удалось получить список районов", file=sys.stderr)
        return []
    
    except Exception as e:
        logger.error(f"Ошибка при получении списка районов: {str(e)}")
        print(f"Ошибка при получении списка районов: {str(e)}", file=sys.stderr)
        logger.error(traceback.format_exc())
        print(traceback.format_exc(), file=sys.stderr)
        return [] 