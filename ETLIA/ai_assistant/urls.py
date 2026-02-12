from django.urls import path
from . import views

urlpatterns = [
    path('interpretet/', views.interpretet_intent, name='interpretet_intent'),
]