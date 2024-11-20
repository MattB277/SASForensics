from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import FileListView

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('success/', views.upload_success, name='upload_success'),
    path('', views.react_app, name='react_app'),
    path('api/files/', FileListView.as_view(), name='file-list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



