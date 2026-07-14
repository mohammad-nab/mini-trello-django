from rest_framework_nested import routers
from .views import ColumnViewSet, TaskViewSet
from projects.api.views import ProjectViewSet

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='projects')

projects_router = routers.NestedDefaultRouter(
    router,
    r'projects',
    lookup='projects'
)

projects_router.register(
    r'columns',
    ColumnViewSet,
    basename='project-columns'
)

# new: nest tasks under columns
columns_router = routers.NestedDefaultRouter(
    projects_router,
    r'columns',
    lookup='columns'
)

columns_router.register(
    r'tasks',
    TaskViewSet,
    basename='column-tasks'
)

urlpatterns = router.urls + projects_router.urls + columns_router.urls