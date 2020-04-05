from django.urls import path
from . import views
from checkmewod import views

urlpatterns = [

]

urlpatterns = [
    path('', views.index, name='index'),
    path('about-us.html', views.about, name='about'),
    path('classes.html', views.classes, name='submit'),
]