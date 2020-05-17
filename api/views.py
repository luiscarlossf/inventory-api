import csv
from django.contrib.auth.models import User, Group
from .models import Brand, Category, Computer, Equipament, Floor, Model, Ua
from rest_framework import viewsets, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import UserSerializer, GroupSerializer, BrandSerializer, CategorySerializer, \
ComputerSerializer, EquipamentSerializer, FloorSerializer, ModelSerializer, UaSerializer, FileUploadSerializer
from .utils import delete_all_database, save_data_from_sheet

import logging

logger = logging.getLogger("api")

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
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['name']
    ordering = ['name']
    search_fields = ['name']

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if (self.action == 'create') or (self.action == 'destroy'):
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite as categorias serem editadas ou visualizadas.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['name']
    ordering = ['name']
    search_fields = ['name']

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if (self.action == 'create') or (self.action == 'destroy'):
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class ComputerViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite os computadores serem editados ou visualizados.
    """
    queryset = Computer.objects.all()
    serializer_class = ComputerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['patrimony', 'brand', 'model']
    ordering = ['patrimony']
    filterset_fields = [ 'brand', 'category', 'model', 'warranty_start', 'warranty_end', 'ua', 'floor', 'acquisition_date', 'acquisition_value', 'status', 'policy', 'status_zenworks', 'status_trend', 'status_wsus']
    search_fields = ['patrimony']

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if (self.action == 'create') or (self.action == 'destroy'):
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

class EquipamentViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite os equipamentos serem editados ou visualizados.
    """
    queryset = Equipament.objects.all()
    serializer_class = EquipamentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['patrimony', 'brand', 'model']
    ordering = ['patrimony']
    filterset_fields = [ 'brand', 'category', 'model', 'warranty_start', 'warranty_end', 'ua', 'floor', 'acquisition_date', 'acquisition_value', 'status']
    search_fields = ['patrimony']

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if (self.action == 'create') or (self.action == 'destroy'):
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

class FloorViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite os andares serem editados ou visualizados.
    """
    queryset = Floor.objects.all()
    serializer_class = FloorSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['name']
    ordering = ['name']
    search_fields = ['name']

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if (self.action == 'create') or (self.action == 'destroy'):
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

class ModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite os modelos serem editados ou visualizados.
    """
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['name']
    ordering = ['name']
    search_fields = ['name']

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if (self.action == 'create') or (self.action == 'destroy'):
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

class UaViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite as unidades administrativas serem editadas ou visualizadas.
    """
    queryset = Ua.objects.all()
    serializer_class = UaSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['name']
    ordering = ['name']
    filterset_fields = ['floor']
    search_fields = ['code', 'name']

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if (self.action == 'create') or (self.action == 'destroy'):
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class FileUploadViewSet(viewsets.ViewSet):
    """
    API endpoint que permite o upload de arquivos.
    """
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser]
    serializer_class = FileUploadSerializer

    def create(self, request):
        """
        API endpoint que permite a criação de novos recursos a partir de um arquivo .csv
        """
        try:
            f = request.data['file']
            origem = request.data['origem']
            logger.debug("Criando novos recursos a partir da planilha enviada.")
            with open('./api/static/uploaded/'+origem+'.csv', 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

            with open('./api/static/uploaded/'+origem+'.csv', newline='') as csvfile:
                
                delete_all_database() #Deleta todos os dados do banco de dados

                reader = csv.DictReader(csvfile, delimiter=';')
                logger.info("Lendo linhas da planilha")

                for row in reader: # Itera sobre as linhas do arquivo `csvfile`
                    #Carrega as categorias
                    reg_exp = r'^(\d+) - (?P<name>\w[\w\s]+\w)' #ATENÇÃO: VERIFIQUE SE EXPRESSÃO ESTÁ CORRETA.
                    c_id = save_data_from_sheet(row['Material'], reg_exp, ['name'], CategorySerializer, Category)
                    c_uri= request.build_absolute_uri('categories/{0}'.format(c_id)) if c_id else None
                    
                    #Carrega os andares
                    #13773 - 01000621 - EDIFICIO SEDE, 2 ANDAR, ASSESSORIA DE COMUNICACAO SOCIAL
                    reg_exp = r'(?P<name>(\d ANDAR)|TERREO)'
                    id = save_data_from_sheet(row['U.L.'], reg_exp, ['name'], FloorSerializer, Floor)
                    f_uri = request.build_absolute_uri('floors/{0}'.format(id)) if id else None
                
                    
                    #Carrega as UAs
                    #01008256 - PR/PI COORDENADORIA DA PRM - PRM CORRENTE/PI
                    reg_exp = r'^(?P<code>\d+) \- (?P<name>\w[\w\s/\-.]+\w)'
                    uris = {'floor':f_uri} if f_uri else None
                    id = save_data_from_sheet(row['U.A.'], reg_exp, ['code','name'], UaSerializer, Ua, uris, request)
                    u_uri = request.build_absolute_uri('uas/{0}'.format(id)) if id else None

                    
                    #Carrega as marcas
                    reg_exp = r'(?P<name>\w[\w\s/\-.]+\w)'
                    id = save_data_from_sheet(row['Marca'], reg_exp, ['name'], BrandSerializer, Brand, request=request)
                    b_uri = request.build_absolute_uri('brands/{0}'.format(id)) if id else None

                    #Carrega os modelos
                    reg_exp = r'(?P<name>\w[\w\s/\-.]+\w)'
                    id = save_data_from_sheet(row['Modelo'], reg_exp, ['name'], ModelSerializer, Model, request=request)
                    m_uri = request.build_absolute_uri('models/{0}'.format(id)) if id else None

                    #Carrega os equipamentos.
                    #27000247;  -  ;920.85
                    string = row['Patrimônio']+';'+row['Garantia']+';'+row['Valor Aquisição(R$)'].replace('.', '').replace(',', '.')
                    reg_exp = r'^(?P<patrimony>\d+);((?P<warranty_start>\d\d\d\d-\d\d-\d\d)|\s) - ((?P<warranty_end>\d\d\d\d-\d\d-\d\d)|\s);(?P<acquisition_value>\d+\.\d+)'
                    uris = {'category': c_uri, 'floor': f_uri, 'ua': u_uri, 'brand': b_uri, 'model': m_uri}
                    category = Category.objects.get(id=c_id) if c_id else None
                    result = None
                    if not(category and ("MICROCOMPUTADOR" in category.name)): #Salva um computador
                        result = save_data_from_sheet(string, reg_exp, ['patrimony', 'warranty_start', 'warranty_end', 'acquisition_value'], EquipamentSerializer, Equipament, uris=uris, request=request)
                    elif category:
                        result = save_data_from_sheet(string, reg_exp, ['patrimony', 'warranty_start', 'warranty_end', 'acquisition_value'], ComputerSerializer, Computer, uris=uris, request=request)
                        
                    else:
                        logger.error("Categoria do equipamento não foi definida.")
                        raise ValueError("Categoria do equipamento não foi definida.")

                    if not(result):
                        logger.error("Um equipamento não foi salvo.")
                        raise RuntimeError("Um equipamento não foi salvo.")
            logger.debug("Dados carregados com sucesso.")
            return Response("O upload foi concluido com sucesso.", status=204)
        except Exception as e:
            logger.warning("O upload não foi concluido com sucesso.")
            return Response("O upload não foi concluido com sucesso. {0}".format(e), status=400)
    
