from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about-us.html')

def classes(request):
    return render(request, 'classes.html')
