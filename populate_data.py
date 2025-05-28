import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urbanAI_api.settings')
django.setup()

from api.models import *

def populate_districts():
    """Районы Бишкека"""
    districts_data = [
        {
            'name': 'Октябрьский', 'code': 'oktyabrsky',
            'bounds': [[42.850, 74.540], [42.900, 74.600]],
            'area': 45.2
        },
        {
            'name': 'Первомайский', 'code': 'pervomaysky', 
            'bounds': [[42.830, 74.580], [42.890, 74.640]],
            'area': 52.8
        },
        {
            'name': 'Ленинский', 'code': 'leninsky',
            'bounds': [[42.810, 74.560], [42.870, 74.620]], 
            'area': 38.5
        },
        {
            'name': 'Свердловский', 'code': 'sverdlovsky',
            'bounds': [[42.800, 74.520], [42.860, 74.580]],
            'area': 41.3
        }
    ]
    
    for data in districts_data:
        bounds = data['bounds']
        polygon = "42.87,74.61;42.88,74.62;..."  # или GeoJSON-строка
        
        District.objects.get_or_create(
            code=data['code'],
            defaults={
                'name': data['name'],
                'geometry': polygon,
                'area_km2': data['area']
            }
        )
    print("Районы созданы")

def populate_population():
    """Данные населения по годам"""
    districts = District.objects.all()
    
    population_data = {
        'oktyabrsky': [
            {'year': 2020, 'pop': 285000, 'children': 42750},
            {'year': 2021, 'pop': 291000, 'children': 43650},
            {'year': 2022, 'pop': 297000, 'children': 44550},
            {'year': 2023, 'pop': 303000, 'children': 45450},
            {'year': 2024, 'pop': 309000, 'children': 46350},
        ],
        'pervomaysky': [
            {'year': 2020, 'pop': 312000, 'children': 46800},
            {'year': 2021, 'pop': 318000, 'children': 47700},
            {'year': 2022, 'pop': 324000, 'children': 48600},
            {'year': 2023, 'pop': 330000, 'children': 49500},
            {'year': 2024, 'pop': 336000, 'children': 50400},
        ],
        'leninsky': [
            {'year': 2020, 'pop': 265000, 'children': 39750},
            {'year': 2021, 'pop': 270000, 'children': 40500},
            {'year': 2022, 'pop': 275000, 'children': 41250},
            {'year': 2023, 'pop': 280000, 'children': 42000},
            {'year': 2024, 'pop': 285000, 'children': 42750},
        ],
        'sverdlovsky': [
            {'year': 2020, 'pop': 198000, 'children': 29700},
            {'year': 2021, 'pop': 202000, 'children': 30300},
            {'year': 2022, 'pop': 206000, 'children': 30900},
            {'year': 2023, 'pop': 210000, 'children': 31500},
            {'year': 2024, 'pop': 214000, 'children': 32100},
        ]
    }
    
    for district in districts:
        data = population_data.get(district.code, [])
        for item in data:
            PopulationData.objects.get_or_create(
                district=district,
                year=item['year'],
                defaults={
                    'population': item['pop'],
                    'density_per_km2': item['pop'] / district.area_km2,
                    'children_7_17': item['children'],
                    'children_0_6': int(item['children'] * 0.6),
                    'adults_18_64': int(item['pop'] * 0.65),
                    'seniors_65_plus': int(item['pop'] * 0.12)
                }
            )
    print("Население заполнено")

def populate_schools():
    """Существующие школы"""
    districts = {d.code: d for d in District.objects.all()}
    
    schools_data = [
        # Октябрьский
        {'name': 'Школа №1', 'type': 'secondary', 'lat': 42.875, 'lng': 74.570, 'capacity': 800, 'enrollment': 720, 'district': 'oktyabrsky'},
        {'name': 'Гимназия №12', 'type': 'gymnasium', 'lat': 42.880, 'lng': 74.575, 'capacity': 600, 'enrollment': 580, 'district': 'oktyabrsky'},
        {'name': 'Школа №25', 'type': 'secondary', 'lat': 42.865, 'lng': 74.585, 'capacity': 900, 'enrollment': 850, 'district': 'oktyabrsky'},
        
        # Первомайский 
        {'name': 'Школа №5', 'type': 'secondary', 'lat': 42.860, 'lng': 74.610, 'capacity': 750, 'enrollment': 680, 'district': 'pervomaysky'},
        {'name': 'Лицей №3', 'type': 'lyceum', 'lat': 42.870, 'lng': 74.620, 'capacity': 500, 'enrollment': 480, 'district': 'pervomaysky'},
        {'name': 'Школа №18', 'type': 'secondary', 'lat': 42.845, 'lng': 74.600, 'capacity': 850, 'enrollment': 800, 'district': 'pervomaysky'},
        
        # Ленинский
        {'name': 'Школа №7', 'type': 'secondary', 'lat': 42.840, 'lng': 74.590, 'capacity': 700, 'enrollment': 650, 'district': 'leninsky'},
        {'name': 'Школа №22', 'type': 'secondary', 'lat': 42.850, 'lng': 74.600, 'capacity': 800, 'enrollment': 750, 'district': 'leninsky'},
        
        # Свердловский
        {'name': 'Школа №14', 'type': 'secondary', 'lat': 42.830, 'lng': 74.550, 'capacity': 600, 'enrollment': 520, 'district': 'sverdlovsky'},
        {'name': 'Школа №29', 'type': 'secondary', 'lat': 42.840, 'lng': 74.560, 'capacity': 750, 'enrollment': 700, 'district': 'sverdlovsky'},
    ]
    
    for data in schools_data:
        School.objects.get_or_create(
            name=data['name'],
            defaults={
                'school_type': data['type'],
                'location': "42.87,74.61",
                'capacity': data['capacity'],
                'current_enrollment': data['enrollment'],
                'district': districts[data['district']],
                'established_year': 1995,
                'is_active': True
            }
        )
    print("Школы созданы")

def populate_hospitals():
    """Медучреждения"""
    districts = {d.code: d for d in District.objects.all()}
    
    hospitals_data = [
        {'name': 'Городская больница №1', 'type': 'hospital', 'lat': 42.878, 'lng': 74.572, 'beds': 200, 'district': 'oktyabrsky'},
        {'name': 'Поликлиника №3', 'type': 'clinic', 'lat': 42.882, 'lng': 74.578, 'beds': 50, 'district': 'oktyabrsky'},
        {'name': 'Больница №2', 'type': 'hospital', 'lat': 42.865, 'lng': 74.615, 'beds': 150, 'district': 'pervomaysky'},
        {'name': 'Поликлиника №5', 'type': 'clinic', 'lat': 42.845, 'lng': 74.595, 'beds': 40, 'district': 'leninsky'},
        {'name': 'Поликлиника №7', 'type': 'clinic', 'lat': 42.835, 'lng': 74.555, 'beds': 35, 'district': 'sverdlovsky'},
    ]
    
    for data in hospitals_data:
        Hospital.objects.get_or_create(
            name=data['name'],
            defaults={
                'hospital_type': data['type'],
                'location': "42.87,74.61",
                'beds_count': data['beds'],
                'district': districts[data['district']],
                'is_active': True
            }
        )
    print("Больницы созданы")

def populate_fire_stations():
    """Пожарные части"""
    districts = {d.code: d for d in District.objects.all()}
    
    fire_data = [
        {'name': 'ПЧ №1', 'lat': 42.873, 'lng': 74.573, 'vehicles': 4, 'personnel': 15, 'district': 'oktyabrsky'},
        {'name': 'ПЧ №2', 'lat': 42.862, 'lng': 74.612, 'vehicles': 3, 'personnel': 12, 'district': 'pervomaysky'},
        {'name': 'ПЧ №3', 'lat': 42.848, 'lng': 74.592, 'vehicles': 3, 'personnel': 11, 'district': 'leninsky'},
        {'name': 'ПЧ №4', 'lat': 42.837, 'lng': 74.557, 'vehicles': 2, 'personnel': 9, 'district': 'sverdlovsky'},
    ]
    
    for data in fire_data:
        FireStation.objects.get_or_create(
            name=data['name'],
            defaults={
                'location': "42.87,74.61",
                'vehicles_count': data['vehicles'],
                'personnel_count': data['personnel'],
                'response_radius_km': 3.5,
                'district': districts[data['district']],
                'is_active': True
            }
        )
    print("Пожарные части созданы")

def populate_building_zones():
    """Зоны строительства"""
    districts = {d.code: d for d in District.objects.all()}
    
    # Жилые зоны для школ
    zones_data = [
        # Октябрьский - потенциальные места
        {'district': 'oktyabrsky', 'type': 'residential', 'bounds': [[42.870, 74.565], [42.878, 74.575]], 'can_school': True},
        {'district': 'oktyabrsky', 'type': 'educational', 'bounds': [[42.885, 74.580], [42.890, 74.590]], 'can_school': True},
        
        # Первомайский
        {'district': 'pervomaysky', 'type': 'residential', 'bounds': [[42.855, 74.605], [42.865, 74.615]], 'can_school': True},
        {'district': 'pervomaysky', 'type': 'residential', 'bounds': [[42.875, 74.625], [42.885, 74.635]], 'can_school': True},
        
        # Ленинский
        {'district': 'leninsky', 'type': 'residential', 'bounds': [[42.820, 74.570], [42.830, 74.580]], 'can_school': True},
        {'district': 'leninsky', 'type': 'educational', 'bounds': [[42.855, 74.605], [42.865, 74.615]], 'can_school': True},
        
        # Свердловский 
        {'district': 'sverdlovsky', 'type': 'residential', 'bounds': [[42.815, 74.535], [42.825, 74.545]], 'can_school': True},
        {'district': 'sverdlovsky', 'type': 'residential', 'bounds': [[42.845, 74.565], [42.855, 74.575]], 'can_school': True},
    ]
    
    for data in zones_data:
        bounds = data['bounds']
        polygon = "42.87,74.61;42.88,74.62;..."  # или GeoJSON-строка
        
        BuildingZone.objects.get_or_create(
            geometry=polygon,
            defaults={
                'zone_type': data['type'],
                'district': districts[data['district']],
                'can_build_school': data['can_school'],
                'max_building_height': 45 if data['type'] == 'residential' else 25
            }
        )
    print("Зоны строительства созданы")

if __name__ == '__main__':
    print("Заполнение базы данных...")
    populate_districts()
    populate_population() 
    populate_schools()
    populate_hospitals()
    populate_fire_stations()
    populate_building_zones()
    print("Готово!")