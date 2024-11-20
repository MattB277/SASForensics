"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

# Define a simple home view
def home(request):
    return HttpResponse("Welcome to the Django API!")

# URL patterns for the main project
urlpatterns = [
    # Home page (you can also replace this with a redirect to the file upload page)
    path('', home, name='home'),

    # Admin panel URL
    path('admin/', admin.site.urls),

    # Include URLs from the 'files' app (file upload and API)
    path('upload/', include('files.urls')),  # Add file upload routes (from files app)

    # API files endpoint (can be accessed by /api/files/)
    path('api/files/', include('files.urls')),  # API routes for file operations
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
