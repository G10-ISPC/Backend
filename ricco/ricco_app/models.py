from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
# Modelo de Producto
class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=100, blank=False, default='')
    descripcion = models.TextField(blank=False, max_length=255, default='')
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=False, default=0.0)

    class Meta:
        db_table = 'producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return str(self.nombre_producto)


# Modelo de Dirección
class Direccion(models.Model):
    id_direccion = models.AutoField(primary_key=True)
    calle = models.CharField(max_length=100, blank=False, default='')
    numero = models.IntegerField(blank=False, default=0)

    class Meta:
        db_table = 'direccion'
        verbose_name = 'Direccion'
        verbose_name_plural = 'Direcciones'

    def __str__(self):
        return f"{self.calle}, {self.numero}"


# Manager de Usuario Personalizado
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None, **extra_fields):
        if not email:
            raise ValueError('El campo Email debe ser completado')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(email, password=password, **extra_fields)


# Modelo de Usuario Personalizado
class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    email = models.EmailField(max_length=150, unique=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE, blank=True, null=True, related_name="usuario")

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.email


# Crear el token automáticamente cuando se crea un usuario


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    Crea un token de autenticación para un nuevo usuario.

    Esta función se ejecuta automáticamente cuando un nuevo usuario es creado
    en el sistema (a través de la señal `post_save`). Si el usuario ha sido
    recién creado (`created=True`), entonces se genera un token de autenticación
    para dicho usuario.

    Args:
        sender: El modelo de usuario que envía la señal.
        instance: La instancia del usuario recién creado.
        created: Booleano que indica si el usuario fue creado (True si es un nuevo usuario).
    """
    if created:
        Token.objects.create(user=instance)
        
        