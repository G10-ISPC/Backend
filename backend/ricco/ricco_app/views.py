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
from django.http import JsonResponse
import json
import mercadopago

from datetime import datetime

from .serializers import UsuarioSerializers,RegistroSerializers, RolSerializer, ProductoSerializer, DireccionSerializer, CompraSerializer,DetalleSerializer, PedidoSerializer,PermisoSerializer, Rol_PermisoSerializer, PerfilUsuarioSerializer

from .models import Rol, Producto,Direccion, Compra,Detalle,Pedido,Permiso, Rol_Permiso

from django.conf import settings

from datetime import datetime
from django.utils.timezone import now
from django.utils import timezone
import logging
from rest_framework import status


sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

User = get_user_model()


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
logger = logging.getLogger(__name__)

class CancelarPedidoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id_compra):
        print(f"Recibiendo solicitud para cancelar la compra con id: {id_compra}")
        try:
            compra = Compra.objects.get(id_compra=id_compra, user=request.user)
            print(f"Compra encontrada: {compra}")

            # Verifica si ya fue cancelada
            if compra.estado == 'cancelado':
                return Response({'error': 'Esta compra ya fue cancelada.'}, status=status.HTTP_400_BAD_REQUEST)

            # Verifica que la fecha de cancelación no sea None
            if compra.cancelable_hasta is None:
                print(f"Fecha de cancelación excedida. Ahora: {timezone.now()} - Cancelable hasta: {compra.cancelable_hasta}") 
                return Response({'error': 'La fecha de cancelación no está definida para esta compra.'}, 
                                status=status.HTTP_400_BAD_REQUEST)

            # Compara con la zona horaria correcta
            if timezone.now() > compra.cancelable_hasta:
                return Response({'error': 'Ya no puedes cancelar esta compra.'}, status=status.HTTP_400_BAD_REQUEST)

            # Cancela la compra
            compra.estado = 'cancelado'
            compra.save()
            print(f"Compra {compra.id_compra} cancelada exitosamente")


            return Response({'mensaje': 'Compra cancelada exitosamente.'}, status=status.HTTP_200_OK)

        except Compra.DoesNotExist:
            logger.error(f"Compra no encontrada o no pertenece al usuario. ID: {id_compra}")
            print(f"Compra no encontrada o no pertenece al usuario. ID: {id_compra}")
            return Response({'error': 'Compra no encontrada o no pertenece al usuario.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.exception(f"Error inesperado al cancelar compra ID: {id_compra}. Excepción: {str(e)}")
            print(f"Error inesperado al cancelar la compra {id_compra}: {str(e)}")
            return Response({'error': f'Error inesperado: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

        for compra in compras:
            # Si el estado es pendiente y ya venció el tiempo de cancelación
            if (
                compra.estado == 'pendiente'
                and compra.cancelable_hasta
                and timezone.now() > compra.cancelable_hasta
            ):
                compra.estado = 'En Preparación'
                compra.save()

        serializer = CompraSerializer(compras, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        data.pop('descripcion', None)  # Elimina si viene del frontend
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
    permission_classes = [IsAuthenticated]
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer 

    def create(self, request, *args, **kwargs):
        print("Datos recibidos:", request.data)  # Ver qué datos están llegando
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            pedido = serializer.save()
            print("Pedido registrado con éxito:", pedido)
            return Response(serializer.data, status=201)
        print("Errores al registrar pedido:", serializer.errors)  # Ver errores específicos
        return Response(serializer.errors, status=400)
    
class AdminView(APIView):
    permission_classes = [IsAdminUser]  

    def get(self, request):
        print(f"GET llamado por: {request.user}")
        return Response({"message": "Bienvenido al panel de administración"}, status=status.HTTP_200_OK)    

@csrf_exempt
def crear_pagos_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            user = User.objects.get(id=data["user"])
            
            # Inicializamos campos necesarios
            total = 0
            items = []
            descripcion_items = []
            
            compra = Compra.objects.create(
                descripcion="", #se actualizará luego
                user=user,
                fecha=datetime.now(),
                precio_total=0.0  
            )

            for detalle_data in data["detalles"]:
                producto = Producto.objects.get(id_producto=detalle_data["id_producto"])
                cantidad = int(detalle_data["cantidad"])
                precio_unitario = float(producto.precio)
                precio_calculado = cantidad * precio_unitario
                total += precio_calculado

              
                Detalle.objects.create(
                    cantidad=cantidad,
                    precio_calculado=precio_calculado,
                    producto=producto,
                    compra=compra
                )
                
                descripcion_items.append(f"{cantidad} {producto.nombre_producto}")

                items.append({
                    "title": producto.nombre_producto,
                    "quantity": cantidad,
                    "unit_price": precio_unitario,
                    "currency_id": "ARS",
                })
            # Actualizamos la compra con el total y la descripción generada
            compra.precio_total = total
            compra.descripcion = ", ".join(descripcion_items)
            compra.save()

            preference_data = {
                "items": items,
                "back_urls": {
                    "success": "https://google.com",
                    "failure": "https://google.com", "pending": "https://google.com",
                },
                "auto_return": "approved",
                "metadata": {
                    "compra_id": compra.id_compra
                }
            }

            preference_response = sdk.preference().create(preference_data)
            if preference_response["status"] != 201:
               print("Error de Mercado Pago:", preference_response["response"])
               return JsonResponse({"error": "Error al generar preferencia de pago", "detalle": preference_response["response"]}, status=500)

            init_point = preference_response["response"]["init_point"]


            return JsonResponse({"init_point": init_point}, status=201)

        except Exception as e:
            print("Error:", e)
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)

class ActualizarComprasView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ahora = timezone.now()
        compras_actualizadas = []

        compras = Compra.objects.filter(estado='pendiente', cancelable_hasta__lt=ahora)
        for compra in compras:
            compra.estado = 'preparacion'
            compra.save()
            compras_actualizadas.append(compra.id_compra)

        return Response({
            "mensaje": f"Se actualizaron {len(compras_actualizadas)} compras.",
            "compras_actualizadas": compras_actualizadas
        })

          