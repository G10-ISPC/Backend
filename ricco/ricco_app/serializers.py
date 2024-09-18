from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import Producto, Direccion

# Serializador de Usuario
class UsuarioSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('email', 'password')

# Serializador de Dirección
class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = ('calle', 'numero')

# Serializador de Registro
class RegistroSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=get_user_model().objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    direccion = DireccionSerializer(required=True)

    class Meta:
        model = get_user_model()
        fields = ('password', 'password2', 'email', 'first_name', 'last_name', 'telefono', 'direccion', 'is_staff')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Los campos de contraseña no coinciden."})
        return attrs

    def create(self, validated_data):
        direccion_data = validated_data.pop('direccion')
        direccion_instance = Direccion.objects.create(**direccion_data)
        user = get_user_model().objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            telefono=validated_data['telefono'],
            direccion=direccion_instance,
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

# Serializador de Producto
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'
        
        