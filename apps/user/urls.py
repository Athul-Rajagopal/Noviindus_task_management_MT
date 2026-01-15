from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', LoginView.as_view(), name='user_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('tasks/', UserTaskListView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', UserTaskUpdateView.as_view(), name='task-update'),
]