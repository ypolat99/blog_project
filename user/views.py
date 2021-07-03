from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

# Create your views here.

def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        new_user = User(username = username)
        new_user.set_password(password)
        new_user.save()

        login(request, new_user)
        messages.success(request, "You successfully signed up!")
        return redirect("index")

    context = {
        "form": form
    }
    return render(request, "register.html", context)       

def loginUser(request):
    if request.user.is_authenticated():
        return redirect("index")
    form = LoginForm(request.POST or None)
    
    context = {
        "form": form
    }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username= username, password = password)
        if user is None:
            messages.info(request, "Username or password is incorrect!")
            return render(request, "login.html", context )

        messages.success(request, "You successfully logged in!")
        login(request, user)
        return redirect("index")
    return render(request, "login.html", context)

def logoutUser(request):
    logout(request)
    messages.success(request, "You successfully logged out!")
    return redirect("index")