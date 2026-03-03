from django.urls import path
from . import views
from ai_assistant import views as ai_views

urlpatterns = [
    path('ai_interaction/', ai_views.interpretet_intent, name='chat_interaction'),
    path('files/', views.file_upload_interface, name='file_upload_interface'),
    path('files/delete/<int:file_id>/', views.delete_file, name='delete_file'),
    ]
