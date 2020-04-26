from django.urls import path
from . import views
from checkmewod import views

urlpatterns = [

]

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('submit', views.classes, name='submit'),
    path('register', views.register, name='register'),
    path('login', views.log_in, name='login'),
    path('logout', views.log_out, name='logout'),
    path('contact', views.contact, name='contact')

]