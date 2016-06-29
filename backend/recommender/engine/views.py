from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.core import validators
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404


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