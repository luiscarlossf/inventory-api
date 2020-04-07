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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
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
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
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
                #Deleta todos os dados do banco de dados
                Equipament.objects.all().delete()
                Computer.objects.all().delete()
                Brand.objects.all().delete()
                Category.objects.all().delete()
                Floor.objects.all().delete()
                Model.objects.all().delete()
                Ua.objects.all().delete()

                reader = csv.DictReader(csvfile, delimiter=';')

                for row in reader:
                    #Carrega as categorias
                    c = row['Material'].split('-')[1]
                    category = CategorySerializer(data={'name': c})
                    c_url = None
                    if category.is_valid():
                        category = category.save() #Retorna uma instância de Category
                        c_url = 'http://127.0.0.1:8000/categories/{0}/'.format(category.id)
                    else:
                        category = Category.objects.get(name=c[1:])
                        c_url = 'http://127.0.0.1:8000/categories/{0}/'.format(category.id)

                    #Carrega os andares
                    f_url = None
                    try:
                        f = row['U.L.'].split('-')[2] 
                        if ("ANDAR" in f) or (("TÉRREO") in f):
                            f = f.split(',')[1] 
                            floor = FloorSerializer(data={'name':f})
                            if floor.is_valid():
                                floor = floor.save() #Retorna uma instância de Floor
                                f_url = 'http://127.0.0.1:8000/floors/{0}/'.format(floor.id)
                            else:
                                floor = Floor.objects.get(name=f[2:])
                                print(row['U.L.'].split('-')[2].split(','))
                                f_url = 'http://127.0.0.1:8000/floors/{0}/'.format(floor.id)
            
                    except Exception:
                        pass

                    #Carrega as UAs
                    u = row['U.A.'].split('-')
                    u_url = None
                    if f_url != None:
                        ua = UaSerializer(data={'code':u[0], 'name':u[1], 'floor':f_url})
                    else:
                        ua = UaSerializer(data={'code':u[0], 'name':u[1]})
                    if ua.is_valid():
                        ua = ua.save() #Retorna uma instância de Ua
                        u_url = 'http://127.0.0.1:8000/uas/{0}/'.format(ua.id)
                    else:
                        try:
                            ua = Ua.objects.get(code=u[0])
                            u_url = 'http://127.0.0.1:8000/uas/{0}/'.format(ua.id)
                        except Exception:
                            ua = None

                    #Carrega as marcas
                    b = row['Marca']
                    b_url = None
                    brand = BrandSerializer(data={'name':b})
                    if brand.is_valid():
                        brand = brand.save() #Retorna uma instância de Brand
                        b_url = 'http://127.0.0.1:8000/brands/{0}/'.format(brand.id)
                    else:
                        try:
                            brand = Brand.objects.get(name=b)
                            b_url = 'http://127.0.0.1:8000/brands/{0}/'.format(brand.id)
                        except Exception:
                            brand = None

                    #Carrega os modelos
                    m = row['Modelo']
                    m_url = None
                    model = ModelSerializer(data={'name':m})
                    if model.is_valid():
                        model = model.save() #Retorna uma instância de Model
                        m_url = 'http://127.0.0.1:8000/models/{0}/'.format(model.id)
                    else:
                        try:
                            model = Model.objects.get(name=m)
                            m_url = 'http://127.0.0.1:8000/models/{0}/'.format(model.id)
                        except:
                            model = None

                    #Carrega os equipamentos/computadores
                    patrimony = row['Patrimônio']
                    warranty = row['Garantia'].split(' ')
                    if len(warranty) == 6:
                        start = warranty[0]
                        end = warranty[2]
                    else:
                        start = end = None
                    acquisition_value = float(row['Valor Aquisição(R$)'].replace('.', '').replace(',', '.'))
                    if (c_url != None) and ("MICROCOMPUTADOR" in category.name): #Primeiro verifica se category existe
                        computer = ComputerSerializer(data={'patrimony':patrimony, 'brand':b_url, 'category':c_url,'model':m_url, 'warranty_start':start, 'warranty_end':end, 'ua':u_url, 'floor':f_url, 'acquisition_value':acquisition_value})
                        if computer.is_valid():
                            computer.save()
                    else:
                        equipament = EquipamentSerializer(data={'patrimony':patrimony, 'brand':b_url, 'category':c_url, 'model':m_url, 'warranty_start':start, 'warranty_end':end, 'ua':u_url, 'floor':f_url, 'acquisition_value':acquisition_value})
                        if equipament.is_valid():
                            equipament.save()
            
            return Response("O upload foi concluido com sucesso.", status=204)
        except Exception as e:
            return Response("O upload não foi concluido com sucesso. {0}".format(e), status=400)
    
