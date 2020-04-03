from django.contrib import admin
from .models import Document, UserDocumentInfo

# Register your models here.
admin.site.register(Document)
admin.site.register(UserDocumentInfo)
