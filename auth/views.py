from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.


def loginauth(request):
    if request.user.is_authenticated:
        return redirect('/admins')
    else:
        return render(request, 'auth/login.html')


def loginclick(request):
    if (request.method == 'POST'):
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('/admins')
        else:
            return redirect('/admins/login')
    else:
        return redirect('/admins/login')


def logoutclick(request):
    # if (request.method == 'POST' and request.user.is_authenticated):
        logout(request)
        return redirect('/admins/login')
    # else:
    #     return redirect('/admins')
