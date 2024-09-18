from rest_framework import status, generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import get_user_model
from .serializers import (
    RegistroSerializers, ProductoSerializer, DireccionSerializer
)
from .models import Producto, Direccion

# Vista para el Registro de Usuarios
class RegistroView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = RegistroSerializers
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista para el Login de Usuarios
class LoginView(APIView):
    permission_classes = [AllowAny]

    @method_decorator(csrf_exempt)
    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        usuario = authenticate(request, username=email, password=password)
        
        if usuario:
            login(request, usuario)
            token, created = Token.objects.get_or_create(user=usuario)
            return Response({
                'token': token.key,
                'user': {
                    'id': usuario.id,
                    'email': usuario.email,
                    'is_staff': usuario.is_staff
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Credenciales incorrectas'
            }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return Response(data={'message': 'GET request processed successfully'})

# Vista para Logout
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(csrf_exempt)
    def post(self, request):
        # Eliminar el token del usuario (cerrar sesión)
        request.user.auth_token.delete()
        logout(request)
        return Response(status=status.HTTP_200_OK)

# Vista para el CRUD de Productos
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]

# Vista para el CRUD de Direcciones
class DireccionViewSet(viewsets.ModelViewSet):
    queryset = Direccion.objects.all()
    serializer_class = DireccionSerializer
    permission_classes = [IsAuthenticated]
    
    