# your_project_name/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reversi/', include('reversi.urls')),  # Include the Reversi app's URLs
]
