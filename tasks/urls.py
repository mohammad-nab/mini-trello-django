from django.urls import path
from . import views


app_name = 'tasks'
urlpatterns = [
    path('create-column/<int:pk>/', views.CreateColumnView.as_view(), name='create-column'),
]