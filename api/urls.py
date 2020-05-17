from rest_framework.urlpatterns import url, include
from rest_framework import routers 
from django.urls import path
from django.views.generic import TemplateView
from .utils import get_version_default
from .views import BrandViewSet, CategoryViewSet, ComputerViewSet, EquipamentViewSet, \
    FloorViewSet, GroupViewSet, ModelViewSet, UaViewSet, UserViewSet, FileUploadViewSet

#A versão padrão da API 
DEFAULT_VERSION = get_version_default()

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'brands', BrandViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'computers', ComputerViewSet)
router.register(r'equipaments', EquipamentViewSet)
router.register(r'floors', FloorViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'models', ModelViewSet)
router.register(r'uas', UaViewSet)
router.register(r'users', UserViewSet)
router.register(r'uploads', FileUploadViewSet, basename='uploads')


urlpatterns = [ 
    url(r'^v1/', include((router.urls, 'v1'), namespace='v1')),
    path('redoc/', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema_local':'openapi/schema-'+DEFAULT_VERSION+'.yml'}
    ), name='redoc'),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_local':'openapi/schema-'+DEFAULT_VERSION+'.yml'}
    ), name='swagger-ui'),
]