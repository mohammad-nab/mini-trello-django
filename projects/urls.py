from django.urls import path
from . import views


app_name = 'projects'
urlpatterns = [
    path('create/', views.CreateProjectView.as_view(), name='create-project'),
    path('delete/<int:pk>/', views.DeleteProjectView.as_view(), name='delete-project'),
    path('detail/<int:pk>/', views.DetailProjectView.as_view(), name='detail-project'),
    path('dashboard/', views.DashboardProjectView.as_view(), name='project-dashboard'),
    path('update/<int:pk>/', views.UpdateProjectView.as_view(), name='update-project'),
]