from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('analyze-school/<int:scenario_id>/', views.analyze_school_scenario, name='analyze_school'),
    path('web/', views.web_interface, name='web_interface'),
    path('bishkek/', views.bishkek_interface, name='bishkek_interface'),
    path('bishkek/districts/', views.get_districts, name='get_districts'),
    path('bishkek/analyze/<str:district_name>/', views.analyze_bishkek_district, name='analyze_bishkek_district'),
    path('', views.index, name='index'),  # Главная страница (фронт)
    path('api/', views.api_index, name='api_index'),
    path('api/analyze/', views.analyze, name='analyze'),
    path('api/population/', views.population_data, name='population_data'),
    path('api/infrastructure/', views.infrastructure_data, name='infrastructure_data'),
    path('api/building-zones/', views.building_zones, name='building_zones'),
    path('api/schools/geojson/', views.school_locations_geojson, name='schools_geojson'),
]
