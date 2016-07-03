from django.http import JsonResponse
from .utils import jaccard_similarity
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def index(request):
    """
    Calculates similarity and returns result
    :param request:
    :return:
    """
    if request.method == 'POST':
        data = request.POST.dict()
        critics = json.loads(data['critics'])
        person1 = data['person1']
        person2 = data['person2']
        similarity = jaccard_similarity(critics, person1, person2)
        response = {}
        response['similarity'] = similarity
        return JsonResponse(response)