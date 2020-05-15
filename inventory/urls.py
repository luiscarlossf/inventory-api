"""inventory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.schemas import get_schema_view
from django.conf import settings
from django.conf.urls.static import static

import logging

logger = logging.getLogger("django")

logger.debug("Configurando rotas...")

urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('', include('api.urls')), #Adiciona as views da API
    path('api-auth/', include('rest_framework.urls')), #Add REST framework's login an logout views
    path('api-token-auth/', views.obtain_auth_token),
    path('openapi', get_schema_view(
        title="Inventory API",
        description="API para o sistema de levantamento dos equipamentos em uso no MPF/PI.",
        version="1.0.0"
    ), name='openapi-schema'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

logger.debug("Rotas 'admin/', '/', 'api-auth/', 'api-token-auth/' configuradas.")