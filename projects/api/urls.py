from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet, basename='projects')

urlpatterns = router.urls


