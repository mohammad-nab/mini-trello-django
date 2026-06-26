from django.urls import path
from . import views


app_name = 'tasks'

urlpatterns = [
    #columns urls
    path('create-column/<int:pk>/', views.CreateColumnView.as_view(), name='create-column'),
    path('update-column/<int:pk>/', views.UpdateColumnView.as_view(), name='update-column'),
    path('delete-column/<int:pk>/', views.DeleteColumnView.as_view(), name='delete-column'),

    #tasks urls
    path('create-task/<int:pk>/', views.CreateTaskView.as_view(), name='create-task'),
]

