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
from django.http.response import HttpResponseRedirect

videocount = 0


def index(request):
    params = {
        'title': 'Home Page',
        'login': False
    }
    return render(request, 'index.html')


def about(request):
    params = {
        'title': ' About',
        'login': False
    }
    return render(request, 'about-us.html')


def contact(request):
    return render(request, 'contact.html')


def log_in(request):
    messages = []
    next = ""

    if request.GET:
        next = request.GET['next']
    if request.method == 'POST':
        form = LoginForm(request.POST)
        password = request.POST['password']
        username = request.POST['username']
        if User.objects.filter(username=username).exists():
            user = authenticate(username=username, password=password)
            if user is None:
                messages += ['Failed!']
            else:
                login(request, user)
                if next == "":
                    print("bruv")
                    return HttpResponseRedirect("/checkmewod")
                else:
                    return HttpResponseRedirect(next)
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
            print("oh yeah baby")
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password']
            password2 = form.cleaned_data['confirm_password']

            if password1 == password2:
                if User.objects.filter(email=email).exists():
                    messages += ['Email already in use!']
                else:
                    if User.objects.filter(username=username).exists():
                        messages += ['Username already in use!']

                    else:
                        user = User.objects.create_user(username, email, password1)
                        user.first_name = first_name
                        user.last_name = last_name
                        user.save()
                        user = authenticate(username=username, password=password1)
                        login(request, user)
                        return HttpResponseRedirect("/checkmewod")
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
    return HttpResponseRedirect("/checkmewod")


@login_required
def video_sub(request):
    if request.method == 'POST':
        form = DragNDropForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            f = request.FILES['video_file']
            print(request.POST['exercise_in_video'])
            print(request.POST['number_reps'])
            name = f.name
            file_extensions = (".mov", ".mp4", ".avi", ".flv", ".wmv")
            if name.endswith(file_extensions):
                with open('checkmewod/uploaded_files/' + name, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)
                return HttpResponse(json.dumps({"success": True}))
            else:
                return HttpResponse(json.dumps({"success": "extensionError"}))
        else:
            # print(form.errors)
            return HttpResponse(json.dumps({"success": False}))
    else:
        return render(request, 'submit.html')


def event(request):
    return render(request, 'event.html')

def add_event(request):
    return render(request, 'add-event.html')

@login_required
def profile(request):
    return render(request, 'profile.html')
