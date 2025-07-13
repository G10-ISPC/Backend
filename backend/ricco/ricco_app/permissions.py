from rest_framework.permissions import BasePermission

class EsAdministradorPorRol(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.rol and user.rol.nombre_rol.lower() == 'administrador'
