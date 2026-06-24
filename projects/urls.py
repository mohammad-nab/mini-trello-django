from django.urls import path
from . import views


app_name = 'projects'
urlpatterns = [
    path('create/', views.CreateProjectView.as_view(), name='create-project'),
    path('Delete/<int:pk>/', views.DeleteProjectView.as_view(), name='delete-project'),
]