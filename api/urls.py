from rest_framework.urlpatterns import url, include
from rest_framework import routers 
from rest_framework.settings import api_settings
from .views import BrandViewSet, CategoryViewSet, ComputerViewSet, EquipamentViewSet, \
    FloorViewSet, GroupViewSet, ModelViewSet, UaViewSet, UserViewSet, FileUploadViewSet

router = routers.DefaultRouter()
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

print(api_settings.DEFAULT_VERSION)
urlpatterns = [ 
    url(r'^v1/', include((router.urls, 'v1'), namespace='v1')),
    ]