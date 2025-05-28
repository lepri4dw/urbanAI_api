from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

def index(request):
    return render(request, 'index.html')

@csrf_exempt
@api_view(['POST'])
def analyze_data(request):
    try:
        data = json.loads(request.body)
        modes = data.get('modes', [])
        districts = data.get('districts', [])
        
        # Анализ данных (заглушка)
        result = {
            'status': 'success',
            'modes': modes,
            'districts': districts,
            'analysis_id': f"analysis_{len(modes)}_{len(districts)}",
            'timestamp': '2024-01-01T12:00:00Z'
        }
        
        return JsonResponse(result)
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

def map_view(request):
    return render(request, 'map.html')
