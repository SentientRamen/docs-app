from django.contrib.auth.models import User
from datetime import datetime
from .models import Document, UserDocumentInfo


# Update visit history for authorized users
def update_last_visit_user(user_name, doc_name, authorized):
    user = User.objects.get(username=user_name)
    doc = Document.objects.get(name=doc_name)

    # Return true after update
    try:
        update = UserDocumentInfo.objects.get(user=user, document=doc, authorized=authorized)
        update.last_visited = datetime.now()
        update.save()
        return True

    # Return false for unauthorized users
    except UserDocumentInfo.DoesNotExist:
        return False


# Give this user access to all documents
def give_all_documents_authorizations_to_user(user):
    user = User.objects.get(username=user)
    docs = Document.objects.all()

    for doc in docs:
        UserDocumentInfo.objects.create(user=user, document=doc, last_visited=None)


# Give all users access to this document
def give_document_authorizations_to_all_users(document):
    doc = Document.objects.create(name=document)
    users = User.objects.all()

    for user in users:
        UserDocumentInfo.objects.create(user=user, document=doc, last_visited=None)
