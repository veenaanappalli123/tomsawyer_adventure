from django.http import HttpResponse

def home(request):
    return HttpResponse("NAHB Django app is running")
