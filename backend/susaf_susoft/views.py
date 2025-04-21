from rest_framework import viewsets
from rest_framework.response import Response
from .models import Project, Sprint, Task, Metrics, RetroNote
from .serializers import ProjectSerializer, SprintSerializer, TaskSerializer, MetricsSerializer, RetroNoteSerializer
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Project
from rest_framework.decorators import action

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class SprintViewSet(viewsets.ModelViewSet):
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer

    @action(detail=True, methods=['get'])
    def tasks(self, request, pk=None):
        sprint = self.get_object()
        tasks = Task.objects.filter(sprint=sprint)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class MetricsViewSet(viewsets.ModelViewSet):
    queryset = Metrics.objects.all()
    serializer_class = MetricsSerializer

    @action(detail=False, methods=['get'], url_path='by-task/(?P<task_id>[^/.]+)')
    def get_metrics_by_task(self, request, task_id=None):
        task = get_object_or_404(Task, id=task_id)
        metrics = Metrics.objects.filter(task=task)
        serializer = MetricsSerializer(metrics, many=True)
        return Response(serializer.data)

class RetroNoteViewSet(viewsets.ModelViewSet):
    queryset = RetroNote.objects.all()
    serializer_class = RetroNoteSerializer

    @action(detail=False, methods=['get'], url_path='by-sprint/(?P<sprint_id>[^/.]+)')
    def get_notes_by_sprint(self, request, sprint_id=None):
        sprint = Sprint.objects.filter(id=sprint_id).first()
        if not sprint:
            return Response({"error": "Sprint not found"}, status=404)
        notes = RetroNote.objects.filter(sprint=sprint)
        serializer = RetroNoteSerializer(notes, many=True)
        return Response(serializer.data)


