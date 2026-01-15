from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import Task

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        token['username'] = user.username
        return token
    

# task list serializer
class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'status']

# task update serializer
class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['status', 'completion_report', 'worked_hours']

    def validate(self, data):
        status = data.get('status')
        if status == 'COMPLETED':
            if not data.get('completion_report'):
                raise serializers.ValidationError({'completion_report': 'This field is required when completing a task.'})
            if data.get('worked_hours') is None:
                raise serializers.ValidationError({'worked_hours': 'This field is required when completing a task.'})
        return data
    
