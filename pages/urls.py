from django.urls import path
from . import views

# Arguments for each path is url, views method, and reference name
urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
]
