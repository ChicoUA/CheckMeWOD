from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render, redirect
from checkmewod.forms import RegisterForm, LoginForm, DragNDropForm


# Create your views here.
from checkmewod.models import MyUser
from django.http import HttpResponse
import json

videocount=0

def index(request):
    params = {
        'title': 'Home Page',
        'login': False
    }
    return render(request, 'index.html', params)


def about(request):
    params = {
        'title': ' About',
        'login': False
    }
    return render(request, 'about-us.html')


def log_in(request):
    messages = []
    if request.method == 'POST':
        form = LoginForm(request.POST)
        password = request.POST['password']
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = authenticate(email=email, password=password)
            if user is None:
                messages += ['Failed!']
            else:
                login(request, user)
                return index(request)
        else:
            messages += ['Failed!']
    else:
        form = LoginForm()
    params = {
        'title': 'Login',
        'login': False,
        'messages': messages,
        'form': form
    }
    return render(request, 'login.html', params)




def register(request):
    messages = []
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password']
            password2 = form.cleaned_data['confirm_password']

            if password1 == password2:
                if User.objects.filter(email=email).exists():
                    messages += ['Email already in use!']

                else:

                    user = User(email=email, username=username)
                    user.set_password(password1)
                    user.save()
                    return redirect('login')
            else:
                messages += ['Password not matching!']
        else:
            messages += ['Failed!']
    else:
        form = RegisterForm()
    params = {
        'title': 'Register',
        'login': False,
        'messages': messages,
        'form': form
    }
    return render(request, 'register.html', params)


@login_required
def log_out(request):
    logout(request)
    return index(request)


def classes(request):
    if request.method == 'POST':
        form = DragNDropForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            f=request.FILES['video_file']
            name = f.name
            with open('checkmewod/uploaded_files/'+name, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
            return HttpResponse(json.dumps({"success":True}))
        else:
            #print(form.errors)
            return HttpResponse(json.dumps({"success":False}))
    else:
        return render(request, 'submit.html')

