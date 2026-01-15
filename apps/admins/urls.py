from django.urls import path
from .views import *

urlpatterns = [
    path('tasks/<int:pk>/reports/', TaskReportView.as_view(), name='task-reports'),
    path('login/', admin_login, name='panel_login'),
    path('logout/', admin_logout, name='panel_logout'),

    path('dashboard/', dashboard, name='dashboard'),

    # SuperAdmin
    path('users/', user_list, name='user_list'),
    path('users/create/', user_create, name='user_create'),
    path('users/<int:user_id>/delete/', user_delete, name='user_delete'),
    path('users/<int:user_id>/assign-admin/', assign_user_to_admin, name='assign_user_to_admin'),

    # Tasks
    path('tasks/', task_list, name='panel_task_list'),
    path('tasks/create/', task_create, name='panel_task_create'),
    path('tasks/<int:task_id>/report/', task_report, name='panel_task_report'),
]