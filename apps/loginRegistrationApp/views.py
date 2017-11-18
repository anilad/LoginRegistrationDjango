from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from datetime import datetime

def index(request):
    if not 'id' in request.session:
        request.session['id'] = None
    if request.session['id'] != None:
        return redirect ('/success')
    else:
        return render(request, "loginRegistrationApp/index.html")

def register(request):
    if request.session['id'] != None:
        return redirect ('/success')
    else:
        context={
            "max": datetime.today().strftime('%Y-%m-%d')
        }
        return render(request, "loginRegistrationApp/registration.html", context)
    
def success(request):
    if request.session['id'] == None:
        messages.error(request,"You are not logged in")
        return redirect ('/')
    else:
        return render(request, "loginRegistrationApp/success.html")

def login(request):
    result = User.objects.valLogin(request.POST)
    if result[0]:
        request.session['id'] = result[1].id
        return redirect('/success')
    else:
        for error in result[1]:
            messages.error(request, error)
        return redirect('/')

def process(request):
    result = User.objects.valCreate(request.POST)
    if result[0]:
        request.session['id'] = result[1].id;
        return redirect('/success')
    else:
        for error in result[1]:
            messages.error(request, error)
        return redirect('/register')

def logout(request):
    request.session.clear()
    return redirect('/')