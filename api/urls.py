from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('analyze-school/<int:scenario_id>/', views.analyze_school_scenario, name='analyze_school'),
    path('web/', views.web_interface, name='web_interface'),
    path('bishkek/', views.bishkek_interface, name='bishkek_interface'),
    path('bishkek/districts/', views.get_districts, name='get_districts'),
    path('bishkek/analyze/<str:district_name>/', views.analyze_bishkek_district, name='analyze_bishkek_district'),
] 