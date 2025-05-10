from django.urls import path, include
from rest_framework import routers
from .views import LoginView, LogoutView, RegistroView
from ricco_app import views
from .views import MisComprasView, TodasComprasView, AdminView, PerfilUsuarioView, crear_pagos_view, CancelarPedidoView
from django.conf.urls.static import static
from django.conf import settings

router= routers.DefaultRouter()
router.register(r'rol',views.RolViewSet)
router.register(r'producto',views.ProductoViewSet)
router.register(r'direccion',views.DireccionViewSet)
router.register(r'permiso',views.PermisoViewSet)
router.register(r'rol_permiso',views.Rol_PermisoViewSet)
router.register(r'pedido',views.PedidoViewSet)
router.register(r'compra',views.CompraViewSet)
router.register(r'detalle',views.DetalleViewSet)

urlpatterns = [
    path('login/',
         LoginView.as_view(), name='login'),
    path('logout/',
         LogoutView.as_view(), name='logout'),
    path('registro/',
         RegistroView.as_view(), name='registro'),
    path ('mis-compras/', 
          MisComprasView.as_view(), name='mis_compras'),
    path('todas-compras/', TodasComprasView.as_view(), name='todas_compras'), 
    path('admin/', AdminView.as_view(), name='admin'), 
    path('perfilUsuario/', PerfilUsuarioView.as_view(), name='perfilUsuario'),
    path('crear-pago/', views.crear_pagos_view, name='crear_pago'),  
     path('cancelar-compra/<int:id_compra>/', CancelarPedidoView.as_view(), name='cancelar_compra'),
    path('', include(router.urls)),
]

