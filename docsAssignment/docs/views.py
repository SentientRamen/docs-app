from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreateUserForm
from .models import Document
from django.views import defaults
from .helpers import *


# Create your views here.

# User Registration
def register_page(request):
    # Check if user is already logged in
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        form = CreateUserForm()

        # Create user
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                give_all_documents_authorizations_to_user(user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'docs/register.html', context)


# User Login
def login_page(request):
    # Check if user is already logged in
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        # Login user
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'docs/login.html', context)


# User Logout
def logout_page(request):
    logout(request)
    return redirect('login')


# Docs Dashboard
@login_required(login_url='login')
def dashboard(request):
    if request.method == 'POST':
        # Hack to deal with spaces
        document_name = request.POST.get('document').replace(' ', '')
        if document_name:
            # Check if document exists
            document = Document.objects.filter(name=document_name)
            if document:
                messages.info(request, 'Document already exists')
            # Create new document and give authorizations
            else:
                give_document_authorizations_to_all_users(document_name)
                messages.success(request, 'Document created!')

    return render(request, 'docs/dashboard.html')


# Document Page
@login_required(login_url='login')
def room(request, room_name):
    # Check if document exists
    # Hack to deal with spaces
    room_name = room_name.replace(' ', '')
    doc_name = Document.objects.filter(name=room_name)
    if doc_name:
        # Update visited time if user is authorized
        if update_last_visit_user(request.user, room_name, True):
            return render(request, 'docs/room.html', {
                'room_name': room_name,
                'user_name': request.user.username
            })
        # Reroute to 403 for unauthorized users
        else:
            return defaults.permission_denied(request, '',
                                              template_name='403.html')
    # Reroute to 404 for non existent document
    else:
        return defaults.page_not_found(request, '', template_name='404.html')
