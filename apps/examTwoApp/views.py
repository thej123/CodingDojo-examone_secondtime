from django.shortcuts import render, redirect
from models import *
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request, 'examTwoApp/index.html')

def main(request):
    # if someone goes to /success page with logging in, it will redirect to login page
    if 'id' not in request.session:
        return redirect('/examTwoApp')
    return render(request, 'examTwoApp/main.html', context)

def register(request):
    result = User.objects.validate_registration(request.POST)
    if type(result) == list:
        for x in result:
            messages.error(request, x)
        return redirect('/examTwoApp')
    else:
        request.session['id'] = result.id
        messages.success(request, 'You have registered successfully!')
        return redirect('/examTwoApp/main')

def login(request):
    result = User.objects.validate_login(request.POST)
    if type(result) == list:
        for x in result:
            messages.error(request, x)
        return redirect('/examTwoApp')
    else:
        request.session['id'] = result.id
        messages.success(request, 'You have logged in!')
        return redirect('/examTwoApp/main')

def logout(request):
    request.session.clear()
    return redirect('/examTwoApp')

