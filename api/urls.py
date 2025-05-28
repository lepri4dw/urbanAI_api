from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('map/', views.map_view, name='map'),
    path('api/analyze/', views.analyze_data, name='analyze_data'),
] 