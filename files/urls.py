from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .models import File

urlpatterns = [
    path('', views.index, name="index"),
    path('upload_file/', views.upload_file, name="upload_file"),
    path('list_files/', views.list_files, name="list_files"),
    path('delete_file/<int:file_id>/', views.delete_file, name="delete_file"),
    path('download/<int:file_id>/', views.download, name="download"),
]

