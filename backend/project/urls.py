from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from susaf_susoft.views import ProjectViewSet, SprintViewSet, TaskViewSet, MetricsViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'sprints', SprintViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'metrics', MetricsViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls')),
    path('susaf/', include(router.urls)),  # API endpoints for CRUD operations
]
