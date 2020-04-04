from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.

# Document store information specific for documents
class Document(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.name


# UserDocumentInfo table stores info about relations between users and documents
class UserDocumentInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    last_visited = models.DateTimeField(default=None,null=True, blank=True)
    authorized = models.BooleanField(default=True)

