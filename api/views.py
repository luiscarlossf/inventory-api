import csv
from django.contrib.auth.models import User, Group
from .models import Brand, Category, Computer, Computer, Equipament, Floor, Model, Ua
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import UserSerializer, GroupSerializer, BrandSerializer, CategorySerializer, \
ComputerSerializer, EquipamentSerializer, FloorSerializer, ModelSerializer, UaSerializer, FileUploadSerializer

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
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['name']
    ordering = ['name']
    search_fields = ['name']


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite as categorias serem editadas ou visualizadas.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['name']
    ordering = ['name']
    search_fields = ['name']


class ComputerViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite os computadores serem editados ou visualizados.
    """
    queryset = Computer.objects.all()
    serializer_class = ComputerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['patrimony', 'brand', 'model']
    ordering = ['patrimony']
    filterset_fields = [ 'brand', 'category', 'model', 'warranty_start', 'warranty_end', 'ua', 'floor', 'acquisition_date', 'acquisition_value', 'status', 'policy', 'status_zenworks', 'status_trend', 'status_wsus']
    search_fields = ['patrimony']


class EquipamentViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite os equipamentos serem editados ou visualizados.
    """
    queryset = Equipament.objects.all()
    serializer_class = EquipamentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['patrimony', 'brand', 'model']
    ordering = ['patrimony']
    filterset_fields = [ 'brand', 'category', 'model', 'warranty_start', 'warranty_end', 'ua', 'floor', 'acquisition_date', 'acquisition_value', 'status']
    search_fields = ['patrimony']


class FloorViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite os andares serem editados ou visualizados.
    """
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['name']
    ordering = ['name']
    search_fields = ['name']


class ModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite os modelos serem editados ou visualizados.
    """
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['name']
    ordering = ['name']
    search_fields = ['name']


class UaViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite as unidades administrativas serem editadas ou visualizadas.
    """
    queryset = Ua.objects.all()
    serializer_class = UaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['name']
    ordering = ['name']
    filterset_fields = ['floor']
    search_fields = ['code', 'name']

class FileUploadViewSet(viewsets.ViewSet):
    """
    API endpoint que permite o upload de arquivos.
    """
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser]
    serializer_class = FileUploadSerializer

    def create(self, request):
        """
        csvfile = request.data['file']
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row)
        #Colocar cada dada em suas determinadas tabelas do banco.
        """
        try:
            f = request.data['file']
            with open('./files/upload-file.txt', 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

            with open('./files/upload-file.txt') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=';')
                categories = set()
                floors = set()
                uas = dict()
                brands = set()
                models = set()
                equipaments = dict()
                for row in reader:
                    #Carrega as categorias
                    category = row['Material'].split('-')[1]
                    categories.add(category)
                    #Carrega os andares
                    floor = row['U.L.'].split('-')[2]
                    floors.add(floor)
                    #Carrega as UAs
                    ua = row['U.A.'].split('-')
                    uas[ua[0]] = ua[1:]
                    #Carrega as marcas
                    brand = row['Marca']
                    brands.add(brand)
                    #Carrega os modelos
                    model = row['Modelo']
                    models.add(model)
                    #Carrega os equipamentos
                    patrimony = row['Patrimônio']
                    warranty = row['Garantia'].split('-')
                    if len(warranty) == 6:
                        start = warranty[0]+'/'+warranty[1]+'/'+warranty[2]
                        end = warranty[3]+'/'+warranty[4]+'/'+warranty[5]
                    else:
                        start = end = None
                    equipaments[patrimony] = [brand, category, model, None, start, end, ua, floor, None, None, False, False, False, False]
            
            #Colocar cada dada em suas determinadas tabelas do banco.

            return Response("O upload foi concluido com sucesso.", status=204)
        except Exception:
            return Response("O upload não foi concluido com sucesso.", status=400)
    """
    def list(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
    """
    
