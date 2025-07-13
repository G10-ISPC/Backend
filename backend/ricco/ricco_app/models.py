from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from datetime import timedelta, datetime
from django.utils import timezone


class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=50, blank=False, default='rol')

    class Meta:
        db_table = 'rol'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return str(self.nombre_rol)

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=100, blank=False, default='')
    descripcion = models.TextField(blank=False, max_length=255, default='')
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=False, default=0.0)
    visible = models.BooleanField(default=True)
    stock = models.IntegerField(default=0)
    main_imagen = models.ImageField(upload_to='products/', null=True, blank=True)
   
    class Meta:
        db_table = 'producto'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return str(self.id_producto)

class Direccion(models.Model):
    id_direccion = models.AutoField(primary_key=True)
    calle = models.CharField(max_length=100, blank=False, default='')
    numero = models.DecimalField(max_digits=10, decimal_places=2, blank=False, default=0.0)    

    class Meta:
        db_table = 'direccion'
        verbose_name = 'Direccion'
        verbose_name_plural = 'Direcciones'

    def __str__(self):
        return f"{self.calle}, {self.numero}"

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        from .models import Rol  # ✅ Importa desde el mismo archivo

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        user = self.create_user(email, password=password, **extra_fields)

        rol_admin, _ = Rol.objects.get_or_create(nombre_rol='administrador')
        user.rol = rol_admin
        user.save()

        return user

    # def create_superuser(self, email, password=None, **extra_fields):
    #     extra_fields.setdefault('is_staff', True)
    #     extra_fields.setdefault('is_superuser', True)

    #     if extra_fields.get('is_staff') is not True:
    #         raise ValueError(_('Superuser must have is_staff=True.'))
    #     if extra_fields.get('is_superuser') is not True:
    #         raise ValueError(_('Superuser must have is_superuser=True.'))

    #     return self.create_user(email, password=password, **extra_fields)

class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    email = models.EmailField(max_length=150, unique=True)
    telefono = models.CharField(max_length=50, blank=False, null=True)
    direccion = models.ForeignKey(Direccion, to_field='id_direccion', on_delete=models.CASCADE, blank=True, null=True, related_name="usuario")
    rol = models.ForeignKey(Rol, to_field='id_rol', on_delete=models.CASCADE, blank=True, null=True, related_name="usuario")
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'usuario'
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'

    def __str__(self):
        return self.email
    
    def soft_delete(self):
      self.is_active = False
      self.deleted_at = timezone.now()
      self.save()

class Compra(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('preparacion', 'En preparación'),
        ('en_camino', 'En camino'),
        ('cancelado', 'Cancelado'),
        ('entregado', 'Entregado'),
    ]
    
    id_compra = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(max_length=1000, blank=False, default='')
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, blank=False, default=0.0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="compras")
    estado = models.CharField(max_length=50, default="pendiente")
    cancelable_hasta = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.cancelable_hasta:
            self.cancelable_hasta = timezone.now() + timedelta(minutes=3)
        super().save(*args, **kwargs) 

    class Meta:
        db_table = 'compra'
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'

    def __str__(self):
        return str(self.id_compra)

class Detalle(models.Model):
    id_detalle = models.AutoField(primary_key=True)
    cantidad = models.IntegerField(blank=False, default=1)
    precio_calculado = models.DecimalField(max_digits=10, decimal_places=2, blank=False, default=0.0)
    producto = models.ForeignKey(Producto, to_field='id_producto', on_delete=models.CASCADE, related_name="detalle")
    compra = models.ForeignKey(Compra, to_field='id_compra', on_delete=models.CASCADE, related_name="detalle")

    class Meta:
        db_table = 'detalle'
        verbose_name = 'Detalle'
        verbose_name_plural = 'Detalles'

    def __str__(self):
        return f"{self.cantidad}, {self.precio_calculado}"

class Permiso(models.Model):
    id_permiso = models.AutoField(primary_key=True)
    nombre_permiso = models.CharField(max_length=100, blank=False, default='')
    descripcion = models.CharField(max_length=1000, blank=False, default='')

    class Meta:
        db_table = 'permiso'
        verbose_name = 'Permiso'
        verbose_name_plural = 'Permisos'

    def __str__(self):
        return str(self.nombre_permiso)

class Rol_Permiso(models.Model):
    id_rol_permiso = models.AutoField(primary_key=True)
    permiso = models.ForeignKey(Permiso, to_field='id_permiso', on_delete=models.CASCADE, related_name="rol_permiso")
    rol = models.ForeignKey(Rol, to_field='id_rol', on_delete=models.CASCADE, related_name="rol_permiso")

    class Meta:
        db_table = 'rol_permiso'
        verbose_name = 'Rol_Permiso'
        verbose_name_plural = 'Rol_Permisos'

    def __str__(self):
        return str(self.id_rol_permiso)

class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=50, blank=False, default='')
    cancelable_hasta = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name="pedido")
    
    def save(self, *args, **kwargs):
        # Asegúrate de que fecha_pedido no sea None (aunque auto_now_add debería manejar esto)
        if not self.fecha_pedido:
            self.fecha_pedido = timezone.now()  # Asignamos la fecha y hora actual si no está establecida
        
        # Si cancelable_hasta no está establecido, asignamos un valor por defecto de 5 minutos a partir de fecha_pedido
        if not self.cancelable_hasta:
            self.cancelable_hasta = self.fecha_pedido + timedelta(minutes=2)  
        
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'pedido'
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return str(self.id_pedido)
                                    