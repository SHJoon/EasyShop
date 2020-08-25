from django.shortcuts import render, redirect
from django.contrib import messages

from .models import *
import bcrypt

# Create your views here.
def login_index(request):

    return render(request, 'login.html')

# Function to handle registration
def register_user(request):
    all_errors = User.objects.validator(request.POST)

    if len(all_errors) > 0:
        for _, val in all_errors.items():
            messages.error(request, val)
        return redirect('/login_index')

    password = request.POST['registered_password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    try:
        created_user = User.objects.create(
            first_name = request.POST['registered_first_name'],
            last_name = request.POST['registered_last_name'],
            email = request.POST['registered_email'],
            password = pw_hash
        )
    except:
        messages.error(request, "You can't use that email address.")
        return redirect("/login_index")
        
    request.session['user_id'] = created_user.id

    return redirect('/')

# Functions for handling login
def login_user(request):
    user_list = User.objects.filter(email=request.POST['login_email'])
    if len(user_list) == 0:
        messages.error(request, "Please check your email/password")
        return redirect("/login_index")

    if not bcrypt.checkpw(request.POST['login_password'].encode(), user_list[0].password.encode()):
        print("failed password")
        messages.error(request, "Please check your email/password")
        return redirect("/login_index")

    request.session['user_id'] = user_list[0].id
    return redirect("/")

def logout(request):
    request.session.clear()
    return redirect("/login_index")

def index(request):

    return render(request, "homepage.html")