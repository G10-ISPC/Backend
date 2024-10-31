from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import Producto, Direccion, CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


# Serializador de Usuario
class UsuarioSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'first_name', 'last_name', 'telefono', 'direccion', 'is_staff', 'rol')
    def create(self, validated_data):
        user = super().create(validated_data)
        user.rol = 'admin' if user.is_staff else 'cliente'  # Asigna el rol según el is_staff
        user.save()
        return user

# Serializador de Dirección
class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = ('calle', 'numero')

class LoginSerializer(serializers.Serializer):
    """Serializer for handling user login."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        # Cambiado de username a email
        user = authenticate(request=self.context.get('request'), email=email, password=password)

        #Verifica si el usuario no existe
        if user is None:
           
            if not User.objects.filter(email=email).exists():
                raise serializers.ValidationError("El usuario no existe. Registrese")
            else:
                raise serializers.ValidationError("Contraseña incorrecta.")

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data['user']
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'rol': user.rol,
            'user': UsuarioSerializer(user).data,
        }

    def update(self, instance, validated_data):
        """Este método no se necesita para el inicio de sesión."""
        return None # Solo deja este método vacío para cumplir con la interfaz
    
# Serializador de Producto
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

# Serializador de Autenticación
class CustomTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # Obtén el modelo de usuario
        User = get_user_model()
        user = User.objects.filter(email=email).first()

        # Verifica si el usuario existe
        if user is None:
            raise serializers.ValidationError("El usuario no existe.")

        # Verifica la contraseña
        if not user.check_password(password):
            raise serializers.ValidationError("Contraseña incorrecta.")

        # Si las credenciales son válidas, genera los tokens
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'rol': user.rol,
            'user': UsuarioSerializer(user).data,
        }

    def create(self, validated_data):
        raise NotImplementedError("Este método no es necesario para la creación de tokens JWT.")

    def update(self, instance, validated_data):
        raise NotImplementedError("Este método no es necesario para la actualización de tokens JWT.")

    
class UserProfileSerializer(serializers.ModelSerializer):
    direccion = DireccionSerializer()

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'telefono', 'direccion')

    def update(self, instance, validated_data):
        direccion_data = validated_data.pop('direccion', None)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.telefono = validated_data.get('telefono', instance.telefono)

        if direccion_data:
            direccion_instance = instance.direccion
            direccion_instance.calle = direccion_data.get('calle', direccion_instance.calle)
            direccion_instance.numero = direccion_data.get('numero', direccion_instance.numero)
            direccion_instance.save()

        instance.save()
        return instance   
    
# Serializador de Registro de Usuario
class RegistroSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=get_user_model().objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    direccion = DireccionSerializer(required=True)

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'password2', 'first_name', 'last_name', 'telefono', 'direccion', 'is_staff', 'rol')

    def validate(self, attrs):
        # Validar que las contraseñas coincidan
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Los campos de contraseña no coinciden."})
        return attrs

    def create(self, validated_data):
        # Extraer los datos de la dirección
        direccion_data = validated_data.pop('direccion', None)

        # Crear el usuario
        user = get_user_model().objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            telefono=validated_data['telefono'],
            is_staff=validated_data.get('is_staff', False),  # Manejo de is_staff
        )
        user.set_password(validated_data['password'])

        # Asignar rol
        user.rol = 'admin' if user.is_staff else 'cliente'

        # Guardar el usuario para poder vincular la dirección
        user.save()

        # Crear la instancia de la dirección si está presente
        if direccion_data:
            direccion_instance = Direccion.objects.create(**direccion_data)
            user.direccion = direccion_instance
            user.save()

        # Generar tokens JWT para el usuario (si es necesario)
        refresh = RefreshToken.for_user(user)

        return user
       
