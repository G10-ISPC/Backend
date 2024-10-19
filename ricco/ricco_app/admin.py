from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import Producto
from .models import Direccion


# Register your models here.
@admin.register(get_user_model())
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'telefono', 'direccion', 'rol')}), #10/10
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'rol'), #agregue rol
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'rol','is_staff') #10/10 agregue rol
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)



class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id_producto', 'nombre_producto', 'descripcion', 'precio')

class DireccionAdmin(admin.ModelAdmin):
    list_display = ('id_direccion', 'calle', 'numero')       
    

admin.site.register(Direccion, DireccionAdmin)
admin.site.register(Producto, ProductoAdmin)

