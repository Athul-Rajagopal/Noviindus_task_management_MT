from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone

from apps.user.models import Task
from .serializers import TaskReportSerializer
from apps.user.permissions import IsAdmin, IsSuperAdmin

# task report view
class TaskReportView(APIView):
    permission_classes = [IsAdmin | IsSuperAdmin]

    def get(self, request, pk):
        try:
            task = get_object_or_404(Task, pk=pk, status='COMPLETED')

            # Admin can only see tasks assigned to their users
            if request.user.role == 'ADMIN':
                if task.assigned_to.admin != request.user:
                    return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

            serializer = TaskReportSerializer(task)
            return Response(serializer.data)
    
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
