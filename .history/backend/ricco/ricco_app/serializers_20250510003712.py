from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

from .models import CustomUser, Rol, Producto, Direccion,Compra,Detalle,Permiso,Rol_Permiso,Pedido

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings


class UsuarioSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)  
    rol = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'username', 'first_name', 'last_name', 'rol')

    def get_rol(self, obj):
        return 'admin' if obj.is_staff else 'cliente'
class PerfilUsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = get_user_model()  
        fields = ('email', 'first_name', 'last_name', 'telefono', 'password' ) 
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance
    
# class LocalidadSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Localidad
#         fields = '__all__'

# class BarrioSerializer(serializers.ModelSerializer):
#     localidad = LocalidadSerializer(required=True)

#     class Meta:
#         model = Barrio
#         fields = ('nombre_barrio')

class DireccionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Direccion
        fields = ('calle', 'numero')
        extra_kwargs = {
            'barrio': {'required': False, 'allow_null': True},
            
        }

class RegistroSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
   

    class Meta:
        model = CustomUser
        fields = (
            'password', 'password2', 'email',
            'first_name', 'last_name', 'telefono', 'is_staff'
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Los campos de contraseña no coinciden."}
            )
        return attrs

    def create(self, validated_data):        
        user = get_user_model().objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            telefono=validated_data['telefono'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    main_imagen = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = Producto
        fields = ['id_producto', 'nombre_producto', 'descripcion', 'precio', 'visible', 'main_imagen']


class DetalleSerializer(serializers.ModelSerializer):
    nombre_producto = serializers.CharField(source='producto.nombre_producto', read_only=True)  

    class Meta:
        model = Detalle
        fields = ['id_detalle', 'cantidad', 'precio_calculado', 'producto', 'nombre_producto', 'compra']
        
class CompraSerializer(serializers.ModelSerializer):
    detalles = DetalleSerializer(many=True, read_only=True, source='detalle')
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    user_first_name = serializers.CharField(source='user.first_name', read_only=True)
    user_last_name = serializers.CharField(source='user.last_name', read_only=True)
    class Meta:
        model = Compra
        fields = '__all__'       

class MisComprasView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        compras = Compra.objects.filter(user=request.user)
        serializer = CompraSerializer(compras, many=True)
        return Response(serializer.data) 


class PermisoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permiso
        fields = '__all__'


class Rol_PermisoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol_Permiso
        fields = '__all__'


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = ['fecha_pedido', 'estado', 'cancelable_hasta', 'user']


