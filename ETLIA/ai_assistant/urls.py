from django.urls import path
from . import views

urlpatterns = [
    path('interpretet/', views.execute_action, name='execution_action'),
]