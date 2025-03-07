from rest_framework import serializers
from .models import Project, Sprint, Task, Metrics

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class SprintSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())

    class Meta:
        model = Sprint
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    sprint = serializers.PrimaryKeyRelatedField(queryset=Sprint.objects.all())
    class Meta:
        model = Task
        fields = '__all__'

class MetricsSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())
    class Meta:
        model = Metrics
        fields = '__all__'
