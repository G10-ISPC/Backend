from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import Producto, Direccion
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


# Serializador de Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'first_name',
                  'last_name', 'telefono', 'is_staff', 'rol')
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
        fields = ('email', 'password', 'password2', 'first_name',
                  'last_name', 'telefono', 'direccion', 'is_staff', 'rol') #agregue campo rol 10/10

    def validate(self, attrs):
        # Validar que las contraseñas coincidan
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Los campos de contraseña no coinciden."})
        return attrs

    def create(self, validated_data):
        # Extraer y crear la dirección
        direccion_data = validated_data.pop('direccion')
        direccion_instance = Direccion.objects.create(**direccion_data)

        # Crear el usuario
        user = get_user_model().objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            telefono=validated_data['telefono'],
            direccion=direccion_instance,
            is_staff=validated_data.get(
                'is_staff', False),  # Manejo de is_staff
        )
        user.set_password(validated_data['password'])
        user.rol = 'admin' if user.is_staff else 'cliente'  # Asigna rol 10/10
        user.save()

        # Generar tokens JWT para el usuario
        refresh = RefreshToken.for_user(user)

        return user
        """ return {
            'user': UsuarioSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        } """

# Serializador de Producto


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

# Serializador de Autenticación


class CustomTokenObtainPairSerializer(serializers.Serializer):
    """
    Serializador para obtener tokens JWT cuando el usuario se autentica.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # Autenticar al usuario
        user = get_user_model().objects.filter(email=email).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            print(f"Rol obtenido: {user.rol}")  # Agrega este log
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'rol': user.rol, #10/10
                'user': UsuarioSerializer(user).data,
            }

        raise serializers.ValidationError("Credenciales inválidas")

    def create(self, validated_data):
        raise NotImplementedError(
            "Este método no es necesario para la creación de tokens JWT.")

    def update(self, instance, validated_data):
        raise NotImplementedError(
            "Este método no es necesario para la actualización de tokens JWT.")


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Credenciales inválidas")

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