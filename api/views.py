from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import logging
import traceback
import sys

from api.services.gemini_service import (
    analyze_school_need, 
    load_scenario_data, 
    analyze_bishkek_school_need,
    get_bishkek_districts
)

# Настройка логирования
logger = logging.getLogger(__name__)

# Create your views here.

@api_view(['GET'])
@permission_classes([AllowAny])
def index(request):
    return Response({"message": "Welcome to the UrbanAI API!"})

def web_interface(request):
    """
    Отображает веб-интерфейс для анализа необходимости школ
    """
    return render(request, 'api/index.html')

def bishkek_interface(request):
    """
    Отображает веб-интерфейс для анализа необходимости школ в Бишкеке
    """
    districts = get_bishkek_districts()
    return render(request, 'api/bishkek.html', {'districts': districts})

@api_view(['GET'])
@permission_classes([AllowAny])
def analyze_school_scenario(request, scenario_id):
    """
    Анализирует необходимость строительства школы на основе выбранного сценария
    
    Args:
        request: HTTP запрос
        scenario_id (int): ID сценария (1, 2 или 3)
        
    Returns:
        Response: Ответ с результатами анализа
    """
    try:
        logger.info(f"Начало анализа сценария {scenario_id}")
        print(f"\n\n=== НАЧАЛО АНАЛИЗА СЦЕНАРИЯ {scenario_id} ===", file=sys.stderr)
        
        # Загружаем данные сценария
        logger.info(f"Загрузка данных сценария {scenario_id}")
        print(f"Загрузка данных сценария {scenario_id}", file=sys.stderr)
        scenario_data = load_scenario_data(scenario_id)
        
        if not scenario_data:
            logger.error(f"Сценарий с ID {scenario_id} не найден")
            print(f"Сценарий с ID {scenario_id} не найден", file=sys.stderr)
            return Response(
                {"error": f"Сценарий с ID {scenario_id} не найден"}, 
                status=404
            )
        
        logger.info(f"Данные сценария {scenario_id} успешно загружены")
        print(f"Данные сценария {scenario_id} успешно загружены", file=sys.stderr)
        print(f"Название района: {scenario_data['district_info']['name']}", file=sys.stderr)
        
        # Отправляем данные в Gemini API для анализа
        logger.info("Отправка данных в Gemini API для анализа")
        print("Отправка данных в Gemini API для анализа", file=sys.stderr)
        analysis_result = analyze_school_need(scenario_data)
        
        logger.info("Анализ успешно выполнен")
        print("Анализ успешно выполнен", file=sys.stderr)
        
        # Выводим полный ответ от Gemini в консоль
        print("\n=== ОТВЕТ ОТ GEMINI API ===", file=sys.stderr)
        print(analysis_result, file=sys.stderr)
        print("=== КОНЕЦ ОТВЕТА ОТ GEMINI API ===\n", file=sys.stderr)
        
        # Возвращаем результат
        return Response({
            "scenario_id": scenario_id,
            "district_name": scenario_data["district_info"]["name"],
            "analysis_result": analysis_result
        })
        
    except Exception as e:
        logger.error(f"Ошибка при анализе сценария: {str(e)}")
        logger.error(traceback.format_exc())
        print(f"Ошибка при анализе сценария: {str(e)}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        return Response(
            {"error": f"Ошибка при анализе сценария: {str(e)}"}, 
            status=500
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def analyze_bishkek_district(request, district_name):
    """
    Анализирует необходимость строительства школ в указанном районе Бишкека
    
    Args:
        request: HTTP запрос
        district_name (str): Название района Бишкека
        
    Returns:
        Response: Ответ с результатами анализа
    """
    try:
        logger.info(f"Начало анализа района {district_name}")
        print(f"\n\n=== НАЧАЛО АНАЛИЗА РАЙОНА {district_name} ===", file=sys.stderr)
        
        # Проверяем, существует ли указанный район
        logger.info("Получение списка районов")
        print("Получение списка районов", file=sys.stderr)
        districts = get_bishkek_districts()
        if district_name not in districts:
            logger.error(f"Район '{district_name}' не найден")
            print(f"Район '{district_name}' не найден", file=sys.stderr)
            return Response(
                {"error": f"Район '{district_name}' не найден"}, 
                status=404
            )
        
        logger.info(f"Район {district_name} найден")
        print(f"Район {district_name} найден", file=sys.stderr)
        
        # Отправляем запрос в Gemini API для анализа
        logger.info(f"Отправка запроса в Gemini API для анализа района {district_name}")
        print(f"Отправка запроса в Gemini API для анализа района {district_name}", file=sys.stderr)
        analysis_result = analyze_bishkek_school_need(district_name)
        
        logger.info("Анализ успешно выполнен")
        print("Анализ успешно выполнен", file=sys.stderr)
        
        # Выводим полный ответ от Gemini в консоль
        print("\n=== ОТВЕТ ОТ GEMINI API ===", file=sys.stderr)
        print(analysis_result, file=sys.stderr)
        print("=== КОНЕЦ ОТВЕТА ОТ GEMINI API ===\n", file=sys.stderr)
        
        # Возвращаем результат
        return Response({
            "district_name": district_name,
            "analysis_result": analysis_result
        })
        
    except Exception as e:
        logger.error(f"Ошибка при анализе района: {str(e)}")
        logger.error(traceback.format_exc())
        print(f"Ошибка при анализе района: {str(e)}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        return Response(
            {"error": f"Ошибка при анализе района: {str(e)}"}, 
            status=500
        )

@api_view(['GET'])
@permission_classes([AllowAny])
def get_districts(request):
    """
    Возвращает список районов Бишкека
    
    Args:
        request: HTTP запрос
        
    Returns:
        Response: Список районов Бишкека
    """
    try:
        logger.info("Получение списка районов Бишкека")
        print("Получение списка районов Бишкека", file=sys.stderr)
        districts = get_bishkek_districts()
        logger.info(f"Получен список районов: {districts}")
        print(f"Получен список районов: {districts}", file=sys.stderr)
        return Response({"districts": districts})
        
    except Exception as e:
        logger.error(f"Ошибка при получении списка районов: {str(e)}")
        logger.error(traceback.format_exc())
        print(f"Ошибка при получении списка районов: {str(e)}", file=sys.stderr)
        print(traceback.format_exc(), file=sys.stderr)
        return Response(
            {"error": f"Ошибка при получении списка районов: {str(e)}"}, 
            status=500
        )
