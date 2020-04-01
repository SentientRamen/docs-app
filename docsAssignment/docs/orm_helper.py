from django.contrib.auth.models import User
from datetime import datetime
from .models import Authorized, Documents


def update_visited(user_name, doc_name):
    user = User.objects.get(username=user_name)
    doc = Documents.objects.get(name=doc_name)
    try:
        update = Authorized.objects.get(user=user, document=doc)
        update.last_visited = datetime.now()
        update.save()

    except Authorized.DoesNotExist:
        update = None
    return update
