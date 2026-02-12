from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_files, name='upload_files'),
    path('files/', views.file_upload_interface, name='file_upload_interface'),
    ]
