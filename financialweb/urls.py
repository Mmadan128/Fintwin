from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('newswidget/', include('newswidget.urls')), 
    path('simulations/', include('simulations.urls')), # Include the URLs from your app
    path('mainpage/', views.mainpage, name='mainpage'),
]
