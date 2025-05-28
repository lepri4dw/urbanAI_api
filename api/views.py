from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Avg, Sum, Count
import json
import numpy as np
from .models import *

@api_view(['GET'])
def api_index(request):
    return Response({"message": "UrbanAI API v1.0"})

def index(request):
    return render(request, 'index.html')

@api_view(['GET'])
def population_data(request):
    """Плотность населения по районам/годам"""
    districts = request.GET.getlist('districts', [])
    years = request.GET.getlist('years', [2020, 2021, 2022, 2023, 2024])
    
    data = PopulationData.objects.filter(
        district__code__in=districts,
        year__in=years
    ).values(
        'district__name', 'district__code', 'year',
        'population', 'density_per_km2', 
        'children_7_17'
    )
    
    return Response({'data': list(data)})

@api_view(['GET'])
def infrastructure_data(request):
    """Данные инфраструктуры"""
    districts = request.GET.getlist('districts', [])
    
    schools = School.objects.filter(
        district__code__in=districts, is_active=True
    ).values(
        'name', 'school_type', 'capacity', 'current_enrollment',
        'location', 'district__code'
    )
    
    hospitals = Hospital.objects.filter(
        district__code__in=districts, is_active=True
    ).values(
        'name', 'hospital_type', 'beds_count',
        'location', 'district__code'
    )
    
    fire_stations = FireStation.objects.filter(
        district__code__in=districts, is_active=True
    ).values(
        'name', 'response_radius_km', 'vehicles_count',
        'location', 'district__code'
    )
    
    return Response({
        'schools': list(schools),
        'hospitals': list(hospitals),
        'fire_stations': list(fire_stations)
    })

@api_view(['GET'])
def building_zones(request):
    """Зоны строительства"""
    districts = request.GET.getlist('districts', [])
    
    zones = BuildingZone.objects.filter(
        district__code__in=districts,
        can_build_school=True
    ).values(
        'zone_type', 'max_building_height',
        'district__code', 'geometry'
    )
    
    return Response({'zones': list(zones)})

@api_view(['POST'])
def analyze(request):
    """Анализ и поиск оптимального места для школы"""
    data = json.loads(request.body)
    districts = data.get('districts', [])
    modes = data.get('modes', [])
    
    # Получение базовых данных
    stats = calculate_district_stats(districts)
    
    # Поиск оптимальных мест для школ
    optimal_locations = []
    if 'education' in modes:
        optimal_locations = find_optimal_school_locations(districts)
    
    result = {
        'status': 'success',
        'districts': districts,
        'modes': modes,
        'statistics': stats,
        'optimal_locations': optimal_locations,
        'recommendations': generate_recommendations(stats, districts)
    }
    
    return JsonResponse(result)

def calculate_district_stats(districts):
    """Расчет статистики по районам"""
    stats = {}
    
    for district_code in districts:
        # Население
        pop_data = PopulationData.objects.filter(
            district__code=district_code, year=2024
        ).first()
        
        # Школы
        schools_data = School.objects.filter(
            district__code=district_code, is_active=True
        ).aggregate(
            count=Count('id'),
            total_capacity=Sum('capacity'),
            total_enrollment=Sum('current_enrollment')
        )
        
        # Больницы
        hospitals_count = Hospital.objects.filter(
            district__code=district_code, is_active=True
        ).count()
        
        # Пожарные части
        fire_count = FireStation.objects.filter(
            district__code=district_code, is_active=True
        ).count()
        
        # Потребность в школах
        demand = calculate_school_demand(district_code)
        
        stats[district_code] = {
            'population': pop_data.population if pop_data else 0,
            'density': pop_data.density_per_km2 if pop_data else 0,
            'children_school_age': pop_data.children_7_17 if pop_data else 0,
            'schools_count': schools_data['count'] or 0,
            'school_capacity': schools_data['total_capacity'] or 0,
            'school_enrollment': schools_data['total_enrollment'] or 0,
            'hospitals_count': hospitals_count,
            'fire_stations_count': fire_count,
            'school_utilization': (schools_data['total_enrollment'] / schools_data['total_capacity'] * 100) if schools_data['total_capacity'] else 0,
            'school_shortage': demand['shortage'],
            'avg_distance_to_school': demand['avg_distance']
        }
    
    return stats

def calculate_school_demand(district_code):
    """Расчет потребности в школах"""
    try:
        district = District.objects.get(code=district_code)
        pop_data = PopulationData.objects.filter(
            district=district, year=2024
        ).first()
        
        if not pop_data:
            return {'shortage': 0, 'avg_distance': 0}
        
        # Нормы: 1 место в школе на 10 детей школьного возраста
        required_capacity = pop_data.children_7_17 * 1.1  # С запасом 10%
        
        current_capacity = School.objects.filter(
            district=district, is_active=True
        ).aggregate(Sum('capacity'))['capacity__sum'] or 0
        
        shortage = max(0, required_capacity - current_capacity)
        
        # Средняя дистанция до школы (упрощенный расчет)
        schools_count = School.objects.filter(district=district, is_active=True).count()
        area = district.area_km2
        avg_distance = np.sqrt(area / max(1, schools_count)) * 0.5  # Примерная формула
        
        return {
            'shortage': int(shortage),
            'avg_distance': round(avg_distance, 2)
        }
    except:
        return {'shortage': 0, 'avg_distance': 0}

def find_optimal_school_locations(districts):
    """Поиск оптимальных мест для строительства школ (заглушка)"""
    # Здесь можно реализовать простую логику выбора, например, возвращать центр района
    locations = []
    for district_code in districts:
        district = District.objects.filter(code=district_code).first()
        if district:
            # Пример: координаты центра района как строка 'lat,lon'
            center = district.geometry  # предполагается, что geometry хранит строку 'lat,lon'
            lat, lng = map(float, center.split(',')) if ',' in center else (0.0, 0.0)
            locations.append({
                'lat': lat,
                'lng': lng,
                'district': district_code,
                'score': 100,
                'zone_type': 'residential',
                'population_500m': 0,
                'nearest_school_distance': 0
            })
    return locations

def calculate_location_score(point, district):
    """Заглушка для оценки качества локации"""
    return 100

def estimate_population_coverage(point, radius_m):
    """Заглушка для покрытия населения"""
    return 0

def find_nearest_school_distance(point):
    """Заглушка для поиска ближайшей школы"""
    return 0

def generate_recommendations(stats, districts):
    """Генерация рекомендаций"""
    recommendations = []
    
    for district_code in districts:
        district_stats = stats.get(district_code, {})
        
        utilization = district_stats.get('school_utilization', 0)
        shortage = district_stats.get('school_shortage', 0)
        avg_distance = district_stats.get('avg_distance_to_school', 0)
        
        if shortage > 100:
            recommendations.append({
                'type': 'critical',
                'district': district_code,
                'message': f"Критическая нехватка: {int(shortage)} мест в школах",
                'priority': 'high'
            })
        elif utilization > 90:
            recommendations.append({
                'type': 'warning',
                'district': district_code,
                'message': f"Высокая загруженность школ: {utilization:.1f}%",
                'priority': 'medium'
            })
        
        if avg_distance > 2.0:
            recommendations.append({
                'type': 'info',
                'district': district_code,
                'message': f"Большое расстояние до школ: {avg_distance:.1f} км",
                'priority': 'medium'
            })
    
    # Общие рекомендации
    if len([r for r in recommendations if r['type'] == 'critical']) > 0:
        recommendations.append({
            'type': 'suggestion',
            'district': 'all',
            'message': "Рекомендуется строительство 2-3 новых школ",
            'priority': 'high'
        })
    
    return recommendations

@api_view(['GET'])
def school_locations_geojson(request):
    """GeoJSON данные для школ"""
    schools = School.objects.filter(is_active=True)
    
    features = []
    for school in schools:
        # location хранится как строка 'lat,lon'
        try:
            lat, lng = map(float, school.location.split(','))
        except:
            lat, lng = 0.0, 0.0
        features.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [lng, lat]
            },
            'properties': {
                'name': school.name,
                'type': school.school_type,
                'capacity': school.capacity,
                'enrollment': school.current_enrollment,
                'district': school.district.code
            }
        })
    
    return Response({
        'type': 'FeatureCollection',
        'features': features
    })