from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser

from .serializers import UsuarioSerializers,RegistroSerializers, RolSerializer, ProductoSerializer, DireccionSerializer, CompraSerializer,DetalleSerializer, PedidoSerializer,PermisoSerializer, Rol_PermisoSerializer, PerfilUsuarioSerializer

from .models import Rol, Producto,Direccion, Compra,Detalle,Pedido,Permiso, Rol_Permiso



def bienvenida (request): 
    message = """
    <h1>Bienvenido a RICCO BURGUER</h1>
    <p>Gracias por visitar nuestra aplicación. Aquí puedes acceder a las siguientes secciones:</p>
    
    <h2>1. Acceso al Panel de Administración:</h2>
    <p>Para acceder al panel de administración de Django, ve a <a href="/admin/">/admin/</a>.</p>
    
    
    <h2>2. Acceso a las API:</h2>
    <p>Para interactuar con las API, puedes acceder a las siguientes rutas:</p>
    <ul>
        <li><a href="/api/localidad/">/api/localidad/</a></li>
        <li><a href="/api/barrio/">/api/barrio/</a></li>
        <li><a href="/api/rol/">/api/rol/</a></li>
        <li><a href="/api/producto/">/api/producto/</a></li>
        <li><a href="/api/direccion/">/api/direccion/</a></li>
    </ul>
    <p>Recuerda que estas rutas corresponden a la API de nuestra aplicación.</p>
    """
    return HttpResponse(message)

class LoginView(APIView):
    #@method_decorator(csrf_exempt)
    permission_classes=[AllowAny]
    def post(self, request):
        print(f"Datos recibidos en la solicitud: {request.data}")
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        print(f"Intentando autenticar con email: {email}, password: {password}")
        usuario = authenticate(request, username=email, password=password)
        print(f"Resultado de autenticate():{usuario}")

        if usuario:
            login(request, usuario)
            isAdmin = usuario.is_staff
            tokens = self.get_tokens_for_user(usuario)
            user_data = UsuarioSerializers(usuario).data
            return Response({
    'token': tokens['access'],
    'access': tokens['access'],
    'refresh': tokens['refresh'],
    'user': UsuarioSerializers(usuario).data
}, status=status.HTTP_200_OK)


        else:
            return Response({'error': 'Credenciales de inicio de sesión incorrectas'}, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        refresh['first_name'] = user.first_name 
        refresh['last_name'] = user.last_name
        refresh['is_staff'] = user.is_staff 
        access = refresh.access_token 
        access['first_name'] = user.first_name 
        access['last_name'] = user.last_name
        access['is_staff']= user.is_staff 
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def get(self, request):
        return Response(data={'message': 'GET request processed successfully'})
class LogoutView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
    

class RegistroView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = RegistroSerializers
    permission_classes = [AllowAny]

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @csrf_exempt
    def get(self, request, *args, **kwargs):
        print(f"GET llamado por: {request.user}")
        return Response(data={'message': 'GET request processed successfully'}, status=status.HTTP_200_OK)

class PerfilUsuarioView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PerfilUsuarioSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
             
# class LocalidadViewSet(viewsets.ModelViewSet):
#     queryset=Localidad.objects.all()
#     serializer_class= LocalidadSerializer
 
# class BarrioViewSet(viewsets.ModelViewSet):
#     queryset=Barrio.objects.all()
#     serializer_class= BarrioSerializer
 
class RolViewSet(viewsets.ModelViewSet):
    queryset=Rol.objects.all()
    serializer_class= RolSerializer
 
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()  
    serializer_class = ProductoSerializer
    permission_classes = [AllowAny]
    lookup_field = 'id_producto'  

    def get_queryset(self):
        user = self.request.user
        print(f"Usuario autenticado en productos: {user} - Is staff: {getattr(user, 'is_staff', False)}")
        if user.is_authenticated and user.is_staff:
            
            return Producto.objects.all()
        else:
            
            return Producto.objects.filter(visible=True)

    def get_serializer_context(self):
        return {'request': self.request}  
 
class DireccionViewSet(viewsets.ModelViewSet):
    queryset=Direccion.objects.all()
    serializer_class= DireccionSerializer

class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer   
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        compras = Compra.objects.select_related('user').all()
        for compra in compras:
            print(f'Compra ID: {compra.id}, Usuario: {compra.user.first_name} {compra.user.last_name}')
        return compras


class MisComprasView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        compras = Compra.objects.filter(user=request.user)
        print(f"Usuario autenticado: {request.user}")
        print(f"Compras del usuario: {compras}")

        serializer = CompraSerializer(compras, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        data['user'] = request.user.id
        serializer = CompraSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
class TodasComprasView(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        
        print("Encabezados de la solicitud:", request.headers)

        if (not request.user.is_staff) and (not request.user.rol or request.user.rol.nombre_rol != "Administrador"):
            print(f"Acceso denegado: el rol del usuario es {request.user.rol.nombre_rol if request.user.rol else 'ninguno'}")
            return Response(
                {"error": "No tienes permisos para acceder a este recurso."},
                status=403
            )

        compras = Compra.objects.all()
        print("Compras obtenidas en el backend:")
        for compra in compras:
            print(f"Compra ID: {compra.id_compra}, Usuario: {compra.user.email}, Total: {compra.precio_total}")  

        serializer = CompraSerializer(compras, many=True)
        return Response(serializer.data)

    def post(self, request):
        
        print("Encabezados de la solicitud:", request.headers)

        if not request.user.rol or request.user.rol.nombre_rol != "Administrador":
            print(f"Acceso denegado: el rol del usuario es {request.user.rol.nombre_rol if request.user.rol else 'ninguno'}")
            return Response(
                {"error": "No tienes permisos para acceder a este recurso."},
                status=403
            )

        data = request.data
        serializer = CompraSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print("Compra creada con éxito:", serializer.data)
            return Response(serializer.data, status=201)
        print("Errores en la creación de la compra:", serializer.errors)
        return Response(serializer.errors, status=400)

    
class DetalleViewSet(viewsets.ModelViewSet):
    queryset=Detalle.objects.all()
    serializer_class= DetalleSerializer  
    
 
class PermisoViewSet(viewsets.ModelViewSet):
    queryset=Permiso.objects.all()
    serializer_class= PermisoSerializer                
    
class Rol_PermisoViewSet(viewsets.ModelViewSet):
    queryset=Rol_Permiso.objects.all()
    serializer_class= Rol_PermisoSerializer        
       
class PedidoViewSet(viewsets.ModelViewSet):
    queryset=Pedido.objects.all()
    serializer_class= PedidoSerializer  
    
class AdminView(APIView):
    permission_classes = [IsAdminUser]  

    def get(self, request):
        print(f"GET llamado por: {request.user}")
        return Response({"message": "Bienvenido al panel de administración"}, status=status.HTTP_200_OK)    
          