from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.core import validators
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout


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
        message = ''

        # login mechanism
        user = authenticate(username=username, password=password)
        if user is not None:
            message = 'Log in success'
        else:
            message = 'Wrong username or password!'

        response = {}
        response['message'] = message
        return JsonResponse(response)