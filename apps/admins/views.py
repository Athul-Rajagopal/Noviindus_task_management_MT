from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone

from apps.user.models import Task, User
from .serializers import TaskReportSerializer
from apps.user.permissions import IsAdmin, IsSuperAdmin

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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
        

# admin login view
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user and (user.is_superuser or user.role == 'ADMIN'):
            login(request, user)
            return redirect('dashboard')

        return render(request, 'adminpanel/login.html', {
            'error': 'Invalid credentials or access denied'
        })

    return render(request, 'adminpanel/login.html')

# admin logout view
@login_required
def admin_logout(request):
    logout(request)
    return redirect('panel_login')


# admin dashboard view
@login_required
def dashboard(request):
    user = request.user

    if not (user.is_superuser or user.role == 'ADMIN'):
        return redirect('panel_login')

    if user.is_superuser:
        context = {
            'user_count': User.objects.count(),
            'task_count': Task.objects.count(),
        }
    else:
        context = {
            'user_count': User.objects.filter(admin=user).count(),
            'task_count': Task.objects.filter(assigned_to__admin=user).count(),
        }

    return render(request, 'adminpanel/dashboard.html', context)

# ---------- SUPERADMIN USER MANAGEMENT ----------

@login_required
def user_list(request):
    if not request.user.is_superuser:
        return redirect('dashboard')

    users = User.objects.all()
    admins = User.objects.filter(role='ADMIN')

    return render(request, 'adminpanel/user_list.html', {
        'users': users,
        'admins': admins
    })


@login_required
def user_create(request):
    if not request.user.is_superuser:
        return redirect('dashboard')

    if request.method == 'POST':
        User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password'],
            role=request.POST['role']
        )
        return redirect('user_list')

    return render(request, 'adminpanel/user_create.html')

@login_required
def user_delete(request, user_id):
    if request.user.is_superuser:
        User.objects.filter(id=user_id).delete()
    return redirect('user_list')

@login_required
def assign_user_to_admin(request, user_id):
    if not request.user.is_superuser:
        return redirect('dashboard')

    user = get_object_or_404(User, id=user_id, role='USER')

    if request.method == 'POST':
        admin = get_object_or_404(User, id=request.POST['admin_id'], role='ADMIN')
        user.admin = admin
        user.save()
        return redirect('user_list')

    admins = User.objects.filter(role='ADMIN')
    return render(request, 'adminpanel/assign_user.html', {
        'user': user,
        'admins': admins
    })

# ---------- TASKS ----------

@login_required
def task_list(request):
    if request.user.is_superuser:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(assigned_to__admin=request.user)

    return render(request, 'adminpanel/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    user = request.user

    if user.is_superuser:
        users = User.objects.filter(role='USER')
    elif user.role == 'ADMIN':
        users = User.objects.filter(admin=user)
    else:
        return redirect('panel_login')

    if request.method == 'POST':
        assigned_to = User.objects.get(id=request.POST['assigned_to'])

        if user.role == 'ADMIN' and assigned_to.admin != user:
            return redirect('panel_task_list')

        Task.objects.create(
            title=request.POST['title'],
            description=request.POST['description'],
            due_date=request.POST['due_date'],
            assigned_to=assigned_to,
            status='PENDING'
        )
        return redirect('panel_task_list')

    return render(request, 'adminpanel/task_create.html', {'users': users})


@login_required
def task_report(request, task_id):
    task = get_object_or_404(Task, id=task_id, status='COMPLETED')

    if request.user.role == 'ADMIN' and task.assigned_to.admin != request.user:
        return redirect('panel_task_list')

    return render(request, 'adminpanel/task_report.html', {'task': task})
