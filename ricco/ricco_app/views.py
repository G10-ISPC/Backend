from rest_framework import permissions
from rest_framework import status, generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import get_user_model
from .serializers import (
    RegistroSerializers, ProductoSerializer, DireccionSerializer, UsuarioSerializer
)
from .models import Producto, Direccion
from .serializers import CustomTokenObtainPairSerializer


# Función para crear tokens JWT
def obtener_tokens_para_usuario(usuario):
    refresh = RefreshToken.for_user(usuario)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'rol': 'admin' if usuario.is_superuser else 'cliente'  # Cambiado a 'rol' 10/10
    }


# Clases de permisos personalizadas


class IsAdmin(permissions.BasePermission):
    """Permiso que permite solo a los administradores acceder a la vista."""

    def has_permission(self, request, view):
        return request.user and request.user.rol == 'admin'


class IsCliente(permissions.BasePermission):
    """Permiso que permite solo a los clientes acceder a la vista."""

    def has_permission(self, request, view):
        return request.user and request.user.rol == 'cliente'


class IsAdminOrReadOnly(permissions.BasePermission):
    """Permiso que permite a los administradores editar, mientras que los clientes solo pueden leer."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.rol == 'admin'


# Vista para el Registro de Usuarios
class RegistroView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = RegistroSerializers
    permission_classes = [AllowAny]  # Registro accesible para todos

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            """ tokens = obtener_tokens_para_usuario(user) """
            refresh = RefreshToken.for_user(user)

            return Response({

                """ 'tokens': tokens,
                'user': serializer.data """

                'tokens': {

                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                },
                'user': UsuarioSerializer(user).data

            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Vista para el Login de Usuarios
class LoginView(APIView):
    permission_classes = [AllowAny]  # Login accesible para todos

    ##agregue hasta linea 93:
    def post(self, request):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Lanza un error si no es válido
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

        # Autenticar al usuario
        usuario = authenticate(request, username=email, password=password)

        if usuario:
            login(request, usuario)
            tokens = obtener_tokens_para_usuario(usuario)
            return Response({
                'tokens': tokens,
                'user': {
                    'id': usuario.id,
                    'email': usuario.email,
                    'first_name': usuario.first_name,
                    'last_name': usuario.last_name,
                    'is_staff': usuario.is_staff,
                    'rol': 'admin' if usuario.is_superuser else 'cliente'  # Cambiado a 'rol' 10/10
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Credenciales incorrectas'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        return Response(data={'message': 'GET request processed successfully'})


# Vista para Logout
class LogoutView(APIView):
    # Logout solo para usuarios autenticados
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ##logout(request)
        return Response({"message": "Logout exitoso"}, status=status.HTTP_200_OK) #09-10 agregado


# Vista para el CRUD de Productos
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAdminOrReadOnly]  # Solo admin puede editar


# Vista para el CRUD de Direcciones
class DireccionViewSet(viewsets.ModelViewSet):
    queryset = Direccion.objects.all()
    serializer_class = DireccionSerializer
    # Todos los usuarios autenticados pueden acceder
    permission_classes = [IsAuthenticated]
