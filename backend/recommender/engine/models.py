from django.db import models
from django.contrib.auth.models import User


class Service(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    host = models.CharField(max_length=200)
    port = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    language = models.CharField(max_length=50)

    def __str__(self):
        return self.name + " at " + self.host + ":" + str(self.port)

