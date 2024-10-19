from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    LoginView, LogoutView, RegistroView, ProductoViewSet, 
    DireccionViewSet, UserProfileView
)

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'direcciones', DireccionViewSet)

urlpatterns = [
    # Rutas para JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Para obtener access y refresh tokens
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Para refrescar el token

    # Rutas personalizadas de login, logout y registro
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registro/', RegistroView.as_view(), name='registro'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    # Incluyendo las rutas del router para Productos y Direcciones
    path('', include(router.urls)),
]

