from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return HttpResponse("Hello from backend")


@csrf_exempt
def test(request):
    if request.method == 'GET':
        print("Pogodio backend")
        response = []
        response.append({'message': 'test message'})
        return JsonResponse(response, safe=False)