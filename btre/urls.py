from django.contrib import admin
from django.urls import path, include

# Here we register our app urls
urlpatterns = [
    path('', include('pages.urls')),
    path('admin/', admin.site.urls),
]
