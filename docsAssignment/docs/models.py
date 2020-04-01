from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.
class Documents(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(User, through='Authorized')

    def __unicode__(self):
        return self.name


class Authorized(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey(Documents, on_delete=models.CASCADE)
    last_visited = models.DateTimeField(default=datetime.now, blank=True)
    authorized = models.BooleanField(default=True)
