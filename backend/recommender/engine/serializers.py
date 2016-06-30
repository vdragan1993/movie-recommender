from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Service


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id', 'host', 'port', 'name', 'language')