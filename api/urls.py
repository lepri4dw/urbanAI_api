from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница (фронт)
    path('api/', views.api_index, name='api_index'),
    path('api/analyze/', views.analyze, name='analyze'),
    path('api/population/', views.population_data, name='population_data'),
    path('api/infrastructure/', views.infrastructure_data, name='infrastructure_data'),
    path('api/building-zones/', views.building_zones, name='building_zones'),
    path('api/schools/geojson/', views.school_locations_geojson, name='schools_geojson'),
]