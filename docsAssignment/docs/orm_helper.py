from django.contrib.auth.models import User
from datetime import datetime
from .models import Document, UserDocumentInfo


# Update visit history for authorized users
def update_last_visit_user(user_name, doc_name, authorized):
    user = User.objects.get(username=user_name)
    doc = Document.objects.get(name=doc_name)

    # Return update
    try:
        update = UserDocumentInfo.objects.get(user=user, document=doc, authorized=authorized)
        update.last_visited = datetime.now()
        update.save()

    # Return none for unauthorized users
    except UserDocumentInfo.DoesNotExist:
        return False

    return True


# Give user authorization for all documents
def give_user_authorizations(user):
    user = User.objects.get(username=user)
    docs = Document.objects.all()

    for doc in docs:
        new_user_doc_info = UserDocumentInfo(user=user, document=doc)
        new_user_doc_info.save()


# Give document authorization to all users
def give_user_authorizations(document):
    doc = Document.objects.get(username=document)
    users = User.objects.all()

    for user in users:
        new_user_doc_info = UserDocumentInfo(user=user, document=doc)
        new_user_doc_info.save()
