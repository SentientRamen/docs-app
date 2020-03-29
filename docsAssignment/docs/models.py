from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Documents(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(User, through='Authorized')

    def __unicode__(self):
        return self.name


class Authorized(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey(Documents, on_delete=models.CASCADE)
    last_edited = models.DateField()
    authorized = models.BooleanField(default=False)

