from django.contrib.auth import authenticate, login, logout
from rest_framework import status, generics
from rest_framework.response import Response
from .serializers import CustomTokenObtainPairSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import GenericAPIView
from .models import CustomUser


class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        user = authenticate(email = email, password = password)

        if user:
            login_serializer = self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                user_serializer = UserSerializer(user)
                return Response({
                    'token': login_serializer.validated_data['access'],
                    'refresh-token': login_serializer.validated_data['refresh'],
                    'user' : user_serializer.data,
                    'message' : 'Inicio de session exitoso',
                }, status=status.HTTP_200_OK)
        
            return Response({
                'error' : 'Email o Contraseña Incorrectos'
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
                'error' : 'Email o Contraseña Incorrectos'
            }, status=status.HTTP_400_BAD_REQUEST)
    
class Logout(GenericAPIView):
    def post(self, request, *args, **kwargs):
        user = CustomUser.objects.filter(id=request.data.get('user', ''))
        if user.exists():
            RefreshToken.for_user(user.first())
            return Response({'message' : 'Sesión cerrada correctamente'}, status=status.HTTP_200_OK)
        return Response({
                'error' : 'No existe este usuario'
            }, status=status.HTTP_400_BAD_REQUEST)