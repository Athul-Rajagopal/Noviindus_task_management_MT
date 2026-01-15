from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import *
from rest_framework.permissions import AllowAny


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny] 
