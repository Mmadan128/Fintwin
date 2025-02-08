from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('newswidget/', include('newswidget.urls')), 
    path('simulations/', include('simulations.urls')), # Include the URLs from your app
]
