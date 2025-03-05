from rest_framework import serializers
from . models import Goal

class GoalSerializer(serializers.ModelSerializer):
    model = Goal
    fields = ['User', 'title', 'description', 'start_date', 'start_time', 'deadline_date', 'deadline_time', 'created_date']