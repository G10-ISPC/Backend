from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LoginView, LogoutView, RegistroView, ProductoViewSet, 
    DireccionViewSet
)

router = DefaultRouter()
router.register(r'productos', ProductoViewSet)
router.register(r'direcciones', DireccionViewSet)



urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registro/', RegistroView.as_view(), name='registro'),
    path('', include(router.urls)),
]