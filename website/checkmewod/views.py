from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about-us.html')

def classes(request):
    return render(request, 'classes.html')

def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')
