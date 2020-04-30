from django.urls import path
from . import views
from checkmewod import views

urlpatterns = [

]

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('submit', views.video_sub, name='submit'),
    path('register', views.register, name='register'),
    path('login', views.log_in, name='login'),
    path('event', views.event, name='event1'),
    path('addevent', views.add_event, name='event2'),
    path('logout', views.log_out, name='logout'),
    path('contact', views.contact, name='contact'),
    path('profile', views.profile, name='profile')

]