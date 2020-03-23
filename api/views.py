from django.contrib.auth.models import User, Group
from .models import Brand, Category, Computer, Computer, Equipament, Floor, Model, Ua
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import UserSerializer, GroupSerializer, BrandSerializer, CategorySerializer, \
ComputerSerializer, EquipamentSerializer, FloorSerializer, ModelSerializer, UaSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite os usuários serem editados ou visualizados.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite os grupos serem editados ou visualizados.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]


class BrandViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite as marcas serem editadas ou visualizadas.
    """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAuthenticated]


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite as categorias serem editadas ou visualizadas.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class ComputerViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite os computadores serem editados ou visualizados.
    """
    queryset = Computer.objects.all()
    serializer_class = ComputerSerializer
    permission_classes = [IsAuthenticated]


class EquipamentViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite os equipamentos serem editados ou visualizados.
    """
    queryset = Equipament.objects.all()
    serializer_class = EquipamentSerializer
    permission_classes = [IsAuthenticated]


class FloorViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite os andares serem editados ou visualizados.
    """
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer
    permission_classes = [IsAuthenticated]


class ModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite os modelos serem editados ou visualizados.
    """
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = [IsAuthenticated]


class UaViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite as unidades administrativas serem editadas ou visualizadas.
    """
    queryset = Ua.objects.all()
    serializer_class = UaSerializer
    permission_classes = [IsAuthenticated]