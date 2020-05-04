from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render, redirect


import uuid

from checkmewod.forms import RegisterForm, LoginForm, DragNDropForm

from checkmewod.tasks import evaluate_video

from checkmewod.models import VideoSubmission, Event

from django.core.mail import send_mail, BadHeaderError

from django.http import HttpResponse
import json
from django.http.response import HttpResponseRedirect
from .forms import EventForm, ContactForm
from checkmewod_project import settings
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

def event(request):
    info = Event.objects.all()
    events = []
    for stat in info:
        image_name = str(stat.event_Logo).split("/")
        stri=""
        ctr=1
        leng = len(image_name[1:])
        for txt in image_name[1:]:
            if ctr < leng:
                stri = stri + txt + "/"
            else:
                stri = stri + txt
            ctr+=1
        print("/"+stri)
        events.append({"logo":"/"+stri,"info":stat})
    context = {
        'events': events
    }
    return render(request, 'event.html', context)


def contact(request):
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


def add_event(request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event submitted.')
            return HttpResponseRedirect("/checkmewod/event")
    else:
        context = {
            'form' : form
        }
        return render(request, "add-event.html", context)


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
            name = f.name
            file_extensions = (".mov", ".mp4", ".avi", ".flv", ".wmv")
            id = uuid.uuid4()
            if name.endswith(file_extensions):
                submitted_video = VideoSubmission.objects.create(
                    video_id = id,
                    video_file = f, 
                    exercise_in_video = request.POST['exercise_in_video'],
                    number_reps = request.POST['number_reps'],
                    video_status = "unevaluated",
                    user_email = request.user
                )
                evaluate_video.delay(id)
                
                
                return HttpResponse(json.dumps({"success": True}))
            else:
                return HttpResponse(json.dumps({"success": "extensionError"}))
        else:
            # print(form.errors)
            return HttpResponse(json.dumps({"success": False}))
    else:
        return render(request, 'submit.html')




@login_required
def profile(request):
    info = VideoSubmission.objects.filter(user_email=request.user)
    statistics=[]
    for stat in info:
        video_name = str(stat.video_file).split("/")
        stri=""
        ctr=1
        leng = len(video_name[1:])
        for txt in video_name[1:]:
            if ctr < leng:
                stri = stri + txt + "/"
            else:
                stri = stri + txt
            ctr+=1
        print("/"+stri)
        statistics.append({"name":"/"+stri, "video_name":video_name[-1], "info":stat})
    
    return render(request, 'profile.html', {"statistics":statistics})
