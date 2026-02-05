import requests
from django.http import JsonResponse

def home(request):
    response = requests.get("http://127.0.0.1:5000/api/status")
    data = response.json()
    return JsonResponse({
        "message": "Django received this from Flask",
        "flask_response": data
    })
