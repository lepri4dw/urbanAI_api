from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

@api_view(['GET'])
def index(request):
    return Response({"message": "Welcome to the UrbanAI API!"})

def map_view(request):
    return render(request, 'map.html')
