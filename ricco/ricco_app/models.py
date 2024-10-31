from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Modelo de Producto
class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=100, blank=False, default='')
    descripcion = models.TextField(blank=False, max_length=255, default='')
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=False, default=0.0)
    is_in_stock = models.BooleanField(default=True)
    

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
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El campo Email debe ser completado')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.rol = 'cliente' #10/10 aregado
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        user = self.create_user(email, password, **extra_fields)
        user.rol = 'admin'  # Asegúrate de asignar el rol correcto
        user.save(using=self._db)
        return user


# Modelo de Usuario Personalizado
class CustomUser(AbstractUser):
    username = None  # Esto elimina el campo username
    email = models.EmailField(max_length=150, unique=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE, blank=True, null=True, related_name="usuario")
    rol = models.CharField(max_length=10, choices=[('admin', 'Admin'), ('cliente', 'Cliente')], default='cliente') #10/10

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.email

