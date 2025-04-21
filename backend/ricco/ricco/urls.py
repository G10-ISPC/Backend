
from django.contrib import admin
from django.urls import path, include
from ricco_app import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.bienvenida), 
    path('admin/', admin.site.urls),    
    path('api/', include('ricco_app.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
