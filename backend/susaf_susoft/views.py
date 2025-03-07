from rest_framework import viewsets
from rest_framework.response import Response
from .models import Project, Sprint, Task, Metrics
from .serializers import ProjectSerializer, SprintSerializer, TaskSerializer, MetricsSerializer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Project

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class SprintViewSet(viewsets.ModelViewSet):
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class MetricsViewSet(viewsets.ModelViewSet):
    queryset = Metrics.objects.all()
    serializer_class = MetricsSerializer


