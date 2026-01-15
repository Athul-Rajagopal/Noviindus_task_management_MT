from rest_framework import serializers
from apps.user.models import Task




# task report serializer
class TaskReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'completion_report', 'worked_hours', 'completed_at']