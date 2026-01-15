from django.urls import path
from .views import *

urlpatterns = [
    path('reports/', TaskReportView.as_view(), name='task-reports'),
]