from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import *
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Task
from .serializers import *
from .permissions import IsUser, IsAdmin, IsSuperAdmin


# user login view
class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny] 


# user task list view
class UserTaskListView(APIView):
    permission_classes = [IsUser]

    def get(self, request):
        try:
            tasks = Task.objects.filter(assigned_to=request.user)
            serializer = TaskListSerializer(tasks, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# user task update view
class UserTaskUpdateView(APIView):
    permission_classes = [IsUser]

    def put(self, request, pk):
        try:
            task = get_object_or_404(Task, pk=pk, assigned_to=request.user)
            serializer = TaskUpdateSerializer(task, data=request.data)

            if serializer.is_valid():
                task = serializer.save()
                if task.status == 'COMPLETED':
                    task.completed_at = timezone.now()
                    task.save()
                return Response({'message': 'Task updated successfully'})


            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
