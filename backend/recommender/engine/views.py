from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.core import validators
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .serializers import UserSerializer, ServiceSerializer
from django.shortcuts import get_object_or_404
from .models import Service
import pymongo
from pymongo import MongoClient
import json
from .utils import form_critics, pearson_default_recommendation, euclid_default_recommendation, get_rest_recommendation, result_analyzer
from bson import json_util


def index(request):
    return HttpResponse("Hello from backend")


@csrf_exempt
def register(request):
    """
    View for new user registration
    :param request:
    :return:
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        username = data['username']
        email = data['email']
        password = data['password']
        message = ''

        try:
            # validate mail
            validators.validate_email(email)
            # check if exists
            found = False
            users = User.objects.all()
            for u in users:
                if u.username == username or u.email == email:
                    message = 'User with given username or email already exists!'
                    found = True
                    break

            # create new user
            if not found:
                new_user = User.objects.create_user(username=username, email=email, password=password)
                new_user.is_staff = False
                new_user.is_active = True
                new_user.is_superuser = False
                new_user.save()
                message = 'User ' + username + ' successfully registered!'

        except:
            message = 'Please enter valid email address!'

        response = {}
        response['message'] = message
        return JsonResponse(response)


@csrf_exempt
def login(request):
    """
    View for user log in
    :param request:
    :return:
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        username = data['username']
        password = data['password']
        response = {}
        message = ''

        # login mechanism
        user = authenticate(username=username, password=password)
        if user is not None:
            serializer = UserSerializer(user)
            response['user'] = serializer.data
            user.is_staff = True
            user.save()
        else:
            message = 'Wrong username or password!'

        response['message'] = message
        return JsonResponse(response)



@csrf_exempt
def logged(request):
    """
    Checks if user is logged in
    :param request:
    :return:
    """
    if request.method == 'GET':
        response = {}
        message = 'no'
        users = User.objects.all()
        for user in users:
            if user.is_staff and not user.is_superuser:
                message = 'ok'
                serializer = UserSerializer(user)
                response['user'] = serializer.data
                break

        response['message'] = message
        return JsonResponse(response)


@csrf_exempt
def logout(request, user_id):
    """
    Logs out user
    :param request:
    :param user_id:
    :return:
    """
    if request.method == 'GET':
        message = 'no'
        user = get_object_or_404(User, pk=user_id)
        if user is not None:
            user.is_staff = False
            user.save()
            message = 'ok'

        response = {}
        response['message'] = message
        return JsonResponse(response)


@csrf_exempt
def profile(request, user_id):
    """
    Displays profile data for given user
    :param request:
    :param user_id:
    :return:
    """
    if request.method == 'GET':
        response = {}
        message = 'no'
        user = get_object_or_404(User, pk=user_id)
        if user is not None:
            message = 'ok'
            list_of_services = []
            services = Service.objects.filter(user=user)
            for service in services:
                serializer = ServiceSerializer(service)
                list_of_services.append(serializer.data)

            response['services'] = list_of_services

        response['message'] = message
        return JsonResponse(response)


@csrf_exempt
def edit(request):
    """
    Update existing service
    :param request:
    :return:
    """
    if request.method == 'POST':
        # extracting data
        data = JSONParser().parse(request)
        service = data['service']
        service_id = int(service['id'])
        host = service['host']
        port = int(service['port'])
        name = service['name']
        language = service['language']
        # updating
        update_service = Service.objects.get(pk=service_id)
        update_service.host = host
        update_service.port = port
        update_service.name = name
        update_service.language = language
        update_service.save()
        # response
        response = {}
        response['message'] = 'ok'
        return JsonResponse(response)


@csrf_exempt
def insert(request):
    """
    Creating new service
    :param request:
    :return:
    """
    if request.method == 'POST':
        # extracting data
        data = JSONParser().parse(request)
        service = data['service']
        host = service['host']
        port = int(service['port'])
        name = service['name']
        language = service['language']
        user_id = int(data['user'])
        user = get_object_or_404(User, pk=user_id)
        # inserting
        new_service = Service.objects.create(user=user, host=host, port=port, name=name, language=language)
        new_service.save()
        # response
        response = {}
        response['message'] = 'ok'
        return JsonResponse(response)



@csrf_exempt
def delete(request, service_id):
    """
    Deleting service
    :param request:
    :param service_id:
    :return:
    """
    if request.method == 'GET':
        service = get_object_or_404(Service, pk=service_id)
        service.delete()
        response = {}
        response['message'] = "ok"
        return JsonResponse(response)


@csrf_exempt
def movies(request):
    """
    Collect all movie titles and ids
    :param request:
    :return:
    """
    if request.method == 'GET':
        client = MongoClient()
        db = client.recommend
        all_movies = db.movies.find().sort("title", pymongo.ASCENDING)
        movies = []
        for movie in all_movies:
            this_movie = {}
            this_movie['id'] = movie['id']
            this_movie['title'] = movie['title']
            movies.append(this_movie)

        response = {}
        response['movies'] = movies
        return JsonResponse(response)


@csrf_exempt
def favourites(request):
    """
    Favourites based recommendation
    :param request:
    :return:
    """
    if request.method == 'POST':
        # read data
        data = JSONParser().parse(request)
        this_favourites = json.loads(data['favourites'])
        heuristic = data['heuristic']
        # prepare critics
        critics = form_critics()
        # append this users' critics
        minus = 0
        critics['default'] = {}
        for favourite in this_favourites:
            favourite_movie = favourite['id']
            critics['default'][favourite_movie] = 10 - minus
            minus += 1

        # call apropriate util
        if heuristic != 'empty':
            user = heuristic['user']
            # default heuristics
            if user == 'default':
                # Euclidean or Pearson
                heuristic_name = heuristic['name']
                if "Euclidean" in heuristic_name:
                    result = euclid_default_recommendation(critics, 'default')
                else:
                    result = pearson_default_recommendation(critics, 'default')
            else:
                # call REST method
                heuristic_name = heuristic['name']
                service_url = get_service_url(user, heuristic_name)
                result = get_rest_recommendation(critics, 'default', service_url)
        # no heuristics selected, default is Pearson's
        else:
            result = pearson_default_recommendation(critics, 'default')

        # prepare response
        message = ""
        results = []
        if result:
            results = result_analyzer(result, 5)
        else:
            message = "No results!"
        response = {}
        response['message'] = message
        response['results'] = results
        return JsonResponse(response)


def get_service_url(username, heuristic_name):
    """
    Returns url of personal service
    :param username: service user name
    :param heuristic_name: heuristic name
    :return: url
    """
    user = User.objects.filter(username=username)
    service = Service.objects.filter(user=user).filter(name=heuristic_name)
    ret_val = "http://" + service[0].host + ":" + str(service[0].port) + "/" + heuristic_name + "/"
    return ret_val

@csrf_exempt
def rated(request):
    """
    Rating based recommendation
    :param request:
    :return:
    """
    if request.method == 'POST':
        # read request data
        data = JSONParser().parse(request)
        ratings = json.loads(data['rated'])
        heuristic = data['heuristic']
        # prepare critics
        critics = form_critics()
        # append user rates
        critics['default'] = {}
        for rate in ratings:
            movie_id = rate['id']
            movie_rate = int(rate['rate'])
            if movie_rate > 0:
                critics['default'][movie_id] = movie_rate

        # call appropriate util
        if heuristic != 'empty':
            user = heuristic['user']
            # default heuristics
            if user == 'default':
                # Euclidean or Pearson
                heuristic_name = heuristic['name']
                if "Euclidean" in heuristic_name:
                    result = euclid_default_recommendation(critics, 'default')
                else:
                    result = pearson_default_recommendation(critics, 'default')
            else:
                # call REST method
                heuristic_name = heuristic['name']
                service_url = get_service_url(user, heuristic_name)
                result = get_rest_recommendation(critics, 'default', service_url)
        # no heuristics selected, default is Pearson's
        else:
            result = pearson_default_recommendation(critics, 'default')

        # prepare response
        message = ""
        results = []
        if result:
            results = result_analyzer(result, 5)
        else:
            message = "No results!"
        response = {}
        response['message'] = message
        response['results'] = results
        return JsonResponse(response)


def create_heuristics(name, user):
    """
    Help function for creating list of available heuristics
    :param name: name of heuristics
    :param user: default or user
    :return:
    """
    method = {}
    method['name'] = name
    method['user'] = user
    return method


@csrf_exempt
def heuristics(request, user_id):
    """
    List all posible heuristics for given user
    :param requeste:
    :param user_id:
    :return:
    """
    if request.method == 'GET':
        methods = []
        # default methods
        methods.append(create_heuristics('Euclidean distance', 'default'))
        methods.append(create_heuristics('Pearson correlation', 'default'))

        user = get_object_or_404(User, pk=user_id)
        if user is not None:
            services = Service.objects.filter(user=user)
            for service in services:
                methods.append(create_heuristics(service.name, service.user.username))

        response = {}
        response['heuristics'] = methods
        return JsonResponse(response)


def find_movie(title):
    """
    Help method for getting movies from database
    :param title: movie title
    :return:
    """
    client = MongoClient()
    db = client.recommend
    cursor = db.movies.find({'title': title})
    for document in cursor:
        return document

@csrf_exempt
def defaults(request, number):
    """
    List default movies to rate
    :param request:
    :param number:
    :return:
    """
    part_one = ['Forrest Gump', 'The Exorcist', 'The Notebook', 'American Pie 2', 'The Godfather', 'A Beautiful Mind', 'Memento', 'The Matrix']
    part_two = ['Requiem for a Dream', 'Halloween', 'Pretty Woman', 'Scary Movie 2', 'Reservoir Dogs', "Schindler's List", 'Vertigo', 'Batman']

    ret_val = []

    collection = None
    if int(number) == 8:
        collection = part_one
    else:
        collection = part_two

    for movie in collection:
        this_movie = find_movie(movie)
        ret_movie = {}
        ret_movie['id'] = this_movie['id']
        ret_movie['title'] = this_movie['title']
        ret_movie['rate'] = 0
        ret_val.append(ret_movie)

    response = {}
    response['movies'] = ret_val
    return JsonResponse(response)