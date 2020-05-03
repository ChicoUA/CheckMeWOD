from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render, redirect
from checkmewod.forms import RegisterForm, LoginForm, DragNDropForm
from django.core.mail import send_mail, BadHeaderError

# Create your views here.
from checkmewod.models import MyUser
from django.http import HttpResponse
import json
from django.http.response import HttpResponseRedirect
from .forms import EventForm, ContactForm
from website import settings

from django.contrib import messages

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
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            your_email = form.cleaned_data['your_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, "[Message sent by: " + your_email + "]\n\n" + message, your_email, [settings.EMAIL_HOST_USER])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            messages.success(request, 'Thank you for your message.')
            return HttpResponseRedirect('')
            #return HttpResponse('Success! Thank you for your message.')
    else:
        form = ContactForm()
    return render(request, "contact.html", {'form': form})


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
def classes(request):
    if request.method == 'POST':
        form = DragNDropForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            f = request.FILES['video_file']
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
    form = EventForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = EventForm(request.POST or None)
    context = {
        'form' : form
    }

    return render(request, "add-event.html", context)


@login_required
def profile(request):
    return render(request, 'profile.html')
