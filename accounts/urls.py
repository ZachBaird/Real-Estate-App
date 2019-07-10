from django.urls import path
from . import views

# Arguments for each path is url, views method, and reference name
urlpatterns = [
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name="dashboard")
]
