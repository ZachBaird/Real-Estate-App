from django.urls import path

from . import views

urlpatterns = [
    path('contact', views.contact, name='contact'),
    path('getemails', views.getemails, name='getemails'),
    path('sendnda', views.sendnda, name='sendnda')
]
