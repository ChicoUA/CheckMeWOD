from django.urls import path
from . import views
from checkmewod import views

urlpatterns = [

]

urlpatterns = [
    path('', views.index, name='index'),
    path('about-us.html', views.about, name='about'),
    path('submit.html', views.classes, name='submit'),
    path('register.html', views.register, name='register'),
    path('login.html', views.log_in, name='login'),
    path('logout', views.log_out, name='logout')

]