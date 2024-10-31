from rest_framework import permissions
from rest_framework import status, generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import  logout
from .serializers import  UserProfileSerializer
from .serializers import CustomTokenObtainPairSerializer


from django.contrib.auth import get_user_model
from .serializers import (
    RegistroSerializers, ProductoSerializer, DireccionSerializer
)
from .models import Producto, Direccion



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


# # Vista para el Registro de Usuarios
# class RegistroView(generics.CreateAPIView):
#     queryset = get_user_model().objects.all()
#     serializer_class = RegistroSerializers
#     permission_classes = [AllowAny]  # Registro accesible para todos

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             tokens = obtener_tokens_para_usuario(user)
#             return Response({
#                 'tokens': tokens,
#                 'user': serializer.data
#             }, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistroView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = RegistroSerializers
    permission_classes = [AllowAny]  # Registro accesible para todos

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = obtener_tokens_para_usuario(user)
            return Response({
                'tokens': tokens,
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            errors = serializer.errors
            if 'email' in errors and isinstance(errors['email'], list):
                # Envía un mensaje simple sin corchetes ni clave "error"
                return Response("Este correo ya existe. Por favor utilice otro.", status=status.HTTP_400_BAD_REQUEST)
            
            # Otros errores en un formato más simple
            simple_errors = {field: error[0] for field, error in errors.items()}
            return Response(simple_errors, status=status.HTTP_400_BAD_REQUEST)
#Vista para el Login
class LoginView(APIView):
    permission_classes = [AllowAny]  # Login accesible para todos

    def post(self, request):
        serializer = CustomTokenObtainPairSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            # Devuelve un error en un formato más simple
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        return Response(data={'message': 'GET request processed successfully'})

# Vista para Logout
class LogoutView(APIView):
    # Logout solo para usuarios autenticados
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Realiza el logout
        logout(request)
        return Response({"message": "Logout exitoso"}, status=status.HTTP_200_OK)


# Vista para el CRUD de Productos
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAdminOrReadOnly]  # Solo admin puede editar

    def perform_update(self, serializer):
        product = serializer.save()
        print(f"Producto {product.id_producto} actualizado: is_in_stock={product.is_in_stock}")




# Vista para el CRUD de Direcciones
class DireccionViewSet(viewsets.ModelViewSet):
    queryset = Direccion.objects.all()
    serializer_class = DireccionSerializer
    # Todos los usuarios autenticados pueden acceder
    permission_classes = [IsAuthenticated]


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    """Vista para obtener, actualizar y eliminar el perfil de usuario."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        """Obtiene el usuario autenticado."""
        return self.request.user

    def get(self, request):
        """Obtiene los datos del perfil del usuario."""
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def put(self, request):
        """Actualiza los datos del perfil del usuario."""
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)  # partial=True permite actualizaciones parciales
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request):
        """Elimina la cuenta del usuario."""
        user = self.get_object()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    