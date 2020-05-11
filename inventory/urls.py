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
import logging

logger = logging.getLogger("django")

logger.debug("Configurando rotas...")

urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('', include('api.urls')), #Adiciona as views da API
    path('api-auth/', include('rest_framework.urls')), #Add REST framework's login an logout views
    path('api-token-auth/', views.obtain_auth_token),
]

logger.debug("Rotas 'admin/', '/', 'api-auth/', 'api-token-auth/' configuradas.")