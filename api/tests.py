import datetime
from rest_framework.settings import api_settings
from django.test import TestCase, TransactionTestCase, Client
from rest_framework.test import APIClient, URLPatternsTestCase, APIRequestFactory, APITestCase
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.contrib.auth.models import UserManager, User
from .models import Brand, Category, Computer, Equipament, Floor, Model, Ua

#A versão padrão da API 
DEFAULT_VERSION = str(api_settings.DEFAULT_VERSION)

#### TESTE DE MODELOS ###########
class BrandModelTests(TransactionTestCase):
    def setUp(self):
        Brand.objects.create(name="brand1")
        Brand.objects.create(name="brand2")
        Brand.objects.create(name="brand3")
    
    def test_add_with_same_name(self):
        '''
        Assegura que não haja repetição de nomes de marca
        '''
        with self.assertRaises(IntegrityError):
            brand = Brand(name="brand3")
            brand.save()

        with self.assertRaises(IntegrityError):
            brand = Brand.objects.get(name="brand3")
            brand.name = "brand2"
            brand.save()
        
class CategoryModelTests(TransactionTestCase):
    def setUp(self):
        Category.objects.create(name="category1")
        Category.objects.create(name="category2")
        Category.objects.create(name="category3")
    
    def test_add_with_same_name(self):
        '''
        Assegura que não haja repetição de nomes de categoria
        '''
        with self.assertRaises(IntegrityError):
            category = Category(name="category3")
            category.save()
        with self.assertRaises(IntegrityError):
            category = Category.objects.get(name="category3")
            category.name = "category2"
            category.save()

class ComputerModelTests(TransactionTestCase):
    def setUp(self):
        brand = Brand.objects.create(name="brand1")
        category = Category.objects.create(name="category1")
        model = Model.objects.create(name="model1")
        floor = Floor.objects.create(name="floor1")
        floor2 = Floor.objects.create(name="floor2")
        ua = Ua(code='12345678', name="ua1")
        ua.floor = floor2
        ua.save(force_insert=True)
        computer = Computer(patrimony='12345678', warranty_start=datetime.datetime(2019, 4,29), warranty_end=datetime.datetime(2020, 4,29), acquisition_date=datetime.datetime(2019, 4,29), acquisition_value=3450.50)
        computer.brand = brand
        computer.category = category
        computer.model = model
        computer.ua = ua
        computer.floor = floor
        computer.save()
    
    def test_add_with_same_patrimony(self):
        '''
        Assegura que não seja adicionado mais de um computador com o mesmo patrimônio
        '''
        with self.assertRaises(IntegrityError):
            computer = Computer(patrimony='12345678', warranty_start=datetime.datetime(2019, 4,29), warranty_end=datetime.datetime(2020, 4,29), acquisition_date=datetime.datetime(2019, 4,29), acquisition_value=3450.50)
            computer.brand = Brand.objects.get(name='brand1')
            computer.category = Category.objects.get(name="category1")
            computer.model = Model.objects.get(name="model1")
            computer.ua = Ua.objects.get(code="12345678")
            computer.floor = Floor.objects.get(name="floor1")
            computer.save()

    def test_add_status_out_enum(self):
        '''
        Assegura que não seja adicionado status aleatórios.
        '''
        with self.assertRaises(ValidationError):
            computer = Computer.objects.get(patrimony='12345678')
            computer.status = "Amor"
            computer.clean_fields()

class EquipamentModelTests(TransactionTestCase):
    def setUp(self):
        brand = Brand.objects.create(name="brand1")
        category = Category.objects.create(name="category1")
        model = Model.objects.create(name="model1")
        floor = Floor.objects.create(name="floor1")
        floor2 = Floor.objects.create(name="floor2")
        ua = Ua(code='12345678', name="ua1")
        ua.floor = floor2
        ua.save()
        equipament = Equipament(patrimony='12345678', warranty_start=datetime.datetime(2019, 4,29), warranty_end=datetime.datetime(2020, 4,29), acquisition_date=datetime.datetime(2019, 4,29), acquisition_value=3450.50)
        equipament.brand = brand
        equipament.category = category
        equipament.model = model
        equipament.ua = ua
        equipament.floor = floor
        equipament.save()

    def test_add_with_same_patrimony(self):
        '''
        Assegura que não seja adicionado mais de um equipamento com o mesmo patrimônio
        '''
        with self.assertRaises(IntegrityError):
            equipament = Equipament(patrimony='12345678', warranty_start=datetime.datetime(2019, 4,29), warranty_end=datetime.datetime(2020, 4,29), acquisition_date=datetime.datetime(2019, 4,29), acquisition_value=3450.50)
            equipament.brand = Brand.objects.get(name="brand1")
            equipament.category = Category.objects.get(name="category1")
            equipament.model = Model.objects.get(name="model1")
            equipament.ua = Ua.objects.get(code="12345678")
            equipament.floor = Floor.objects.get(name="floor1")
            equipament.save()

    def test_add_status_out_enum(self):
        pass
    
class FloorModelTests(TransactionTestCase):
    def setUp(self):
        Floor.objects.create(name="floor1")
        Floor.objects.create(name="floor2")
        Floor.objects.create(name="floor3")
    
    def test_add_with_same_name(self):
        '''
        Assegura que não seja adicionado andar repetido
        '''
        with self.assertRaises(IntegrityError):
            floor = Floor(name="floor3")
            floor.save()
        with self.assertRaises(IntegrityError):
            floor = Floor.objects.get(name="floor3")
            floor.name = "floor2"
            floor.save()

class ModelModelTests(TransactionTestCase):
    def setUp(self):
        Model.objects.create(name="model1")
        Model.objects.create(name="model2")
        Model.objects.create(name="model3")
    
    def test_add_with_same_name(self):
        '''
        Assegura que não seja adicionado um modelo repetido.
        '''
        with self.assertRaises(IntegrityError):
            model = Model(name="model3")
            model.save()

        with self.assertRaises(IntegrityError):
            model = Model.objects.get(name="model3")
            model.name = "model2"
            model.save()

class UaModelTests(TransactionTestCase):
    def setUp(self):
        Ua.objects.create(code='01234567', name="ua1")
        Ua.objects.create(code='89012345', name="ua2")
        Ua.objects.create(code='67890123', name="ua3")
    
    def test_add_with_same_name_and_code(self):
        '''
        Assegura que não seja adicionado uma Unidade Administrativa repetida.
        '''
        with self.assertRaises(IntegrityError):
            ua = Ua(code='01234567', name="ua4")
            ua.save()
        with self.assertRaises(IntegrityError):
            ua = Ua(code='11234567', name="ua3")
            ua.save()
        with self.assertRaises(IntegrityError):
            ua = Ua.objects.get(name="ua3")
            ua.name = "ua2"
            ua.save()
        with self.assertRaises(IntegrityError):
            ua = Ua.objects.get(code="67890123")
            ua.code = "01234567"
            ua.save()


#### TESTE DE VIEWSETS ############
class AccountsTests(APITestCase):
    def setUp(self):
        test_user = User.objects.create_user('test', password='test2020')
        testadmin_user = User.objects.create_superuser('testadmin', password='testadmin2020')
        Token.objects.create(user=test_user)
        Token.objects.create(user=testadmin_user)
        brand = Brand(name="Marca Test")
        brand.save()

    def test_auth_user_login(self):
        '''
        Assegura que o serviço de autenticação do usuário comum esteja funcionando apropriadamente.
        '''
        client = APIClient()
        client.login(username='test', password='test2020')
        response = client.get('/' + DEFAULT_VERSION + '/brands')
        self.assertEqual(response.status_code, 200)

    def test_auth_user_token(self):
        '''
        Assegura que o serviço de autenticação do usuário comum esteja funcionando apropriadamente.
        '''
        client = APIClient()
        token = Token.objects.get(user__username='test')
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get('/' + DEFAULT_VERSION + '/brands')
        self.assertEqual(response.status_code, 200)

    def test_auth_admin_login(self) :
        '''
        Assegura que o serviço de autenticação do administrador esteja funcionando apropriadamente.
        '''
        client = APIClient()
        client.login(username='testadmin', password='testadmin2020')
        response = client.get('/' + DEFAULT_VERSION + '/users')
        self.assertEqual(response.status_code, 200)
        client.logout()

    def test_auth_admin_token(self) :
        '''
        Assegura que o serviço de autenticação do administrador esteja funcionando apropriadamente.
        '''
        client = APIClient()
        token = Token.objects.get(user__username='testadmin')
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.get('/' + DEFAULT_VERSION + '/users')
        self.assertEqual(response.status_code, 200)

    def test_only_delete_with_admin(self):
        '''
        Assegura que só as contas de administradores excluam recursos
        '''
        client = APIClient()
        brand = Brand.objects.get(name="Marca Test")
        response = client.delete('/' + DEFAULT_VERSION + '/brands/'+str(brand.id))
        self.assertEqual(response.status_code, 401)
        client.login(username='test', password='test2020')
        response = client.delete('/' + DEFAULT_VERSION + '/brands/'+str(brand.id))
        self.assertEqual(response.status_code, 403)
        client.logout()
        client.login(username='testadmin', password='testadmin2020')
        response = client.delete('/' + DEFAULT_VERSION + '/brands/'+str(brand.id))
        self.assertEqual(response.status_code, 204)

    def test_only_create_with_admin(self):
        '''
        Assegura que só as contas de administradores criem novos recursos.
        '''
        json = {"name": "Marca Test2"}
        client = APIClient()
        response = client.post('/' + DEFAULT_VERSION + '/brands', json, format='json')
        self.assertEqual(response.status_code, 401)
        client.login(username='test', password='test2020')
        response = client.post('/' + DEFAULT_VERSION + '/brands', json, format='json')
        self.assertEqual(response.status_code, 403)
        client.logout()
        client.login(username='testadmin', password='testadmin2020')
        response = client.post('/' + DEFAULT_VERSION + '/brands', json, format='json')
        self.assertEqual(response.status_code, 201)

    def test_only_admin_read_users_data(self):
        '''
        Apenas administradores podem visualizar os usuários cadastrados
        no sistema. 
        '''
        client = APIClient()
        response = client.get('/' + DEFAULT_VERSION + '/users')
        self.assertEqual(response.status_code, 401)
        client.login(username='test', password='test2020')
        response = client.get('/' + DEFAULT_VERSION + '/users')
        self.assertEqual(response.status_code, 403)
        client.logout()
        client.login(username='testadmin', password='testadmin2020')
        response = client.get('/' + DEFAULT_VERSION + '/users')
        self.assertEqual(response.status_code, 200)

class ResourceTests(APITestCase):
    def setUp(self):
        test_user = User.objects.create_user('test', password='test2020')
        testadmin_user = User.objects.create_superuser('testadmin', password='testadmin2020')
        Token.objects.create(user=test_user)
        Token.objects.create(user=testadmin_user)
        brand = Brand.objects.create(name='Marca1')
        Brand.objects.create(name='Marca3')
        category = Category.objects.create(name='Categoria1')
        Category.objects.create(name='Categoria3')
        model = Model.objects.create(name='Modelo1')
        Model.objects.create(name='Modelo3')
        floor = Floor.objects.create(name='Andar1')
        Floor.objects.create(name='Andar3')
        ua = Ua.objects.create(code='1', name='Ua1')
        Ua.objects.create(code='3', name='Ua3')
        ua.floor = floor 
        ua.save()
        equipament = Equipament(patrimony='12345678', warranty_start=datetime.datetime(2019, 4,29), warranty_end=datetime.datetime(2020, 4,29), acquisition_date=datetime.datetime(2019, 4,29), acquisition_value=3450.50)
        equipament.brand = brand
        equipament.category = category
        equipament.model = model
        equipament.ua = ua
        equipament.floor = floor
        equipament.save()

    def test_add_brand_unique(self):
        '''
        Assegura que não seja adicionada uma marca já existente no sistema.
        '''
        brand_json = {"name": "Marca1"}
        client = APIClient()
        token = Token.objects.get(user__username='testadmin')
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post('/' + DEFAULT_VERSION + '/brands', brand_json)
        self.assertEqual(response.status_code, 400)
        brand_json = {"name": "Marca2"}
        response = client.post('/' + DEFAULT_VERSION + '/brands', brand_json)
        self.assertEqual(response.status_code, 201)

    def test_add_category_unique(self):
        '''
        Assegura que não seja adicionada uma categoria já existente no sistema.
        '''
        category_json = {"name": "Categoria1"}
        client = APIClient()
        token = Token.objects.get(user__username='testadmin')
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post('/' + DEFAULT_VERSION + '/categories', category_json)
        self.assertEqual(response.status_code, 400)
        category_json = {"name": "Categoria2"}
        response = client.post('/' + DEFAULT_VERSION + '/categories', category_json)
        self.assertEqual(response.status_code, 201)

    def test_add_model_unique(self):
        '''
        Assegura que não seja adicionada uma UA já existente no sistema.
        '''
        model_json = {"name": "Modelo1"}
        client = APIClient()
        token = Token.objects.get(user__username='testadmin')
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post('/' + DEFAULT_VERSION + '/models', model_json)
        self.assertEqual(response.status_code, 400)
        model_json = {"name": "Modelo2"}
        response = client.post('/' + DEFAULT_VERSION + '/models', model_json)
        self.assertEqual(response.status_code, 201)

    def test_add_floor_unique(self):
        '''
        Assegura que não seja adicionado um andar já existente no sistema.
        '''
        floor_json = {"name": "Andar1"}
        client = APIClient()
        token = Token.objects.get(user__username='testadmin')
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post('/' + DEFAULT_VERSION + '/floors', floor_json)
        self.assertEqual(response.status_code, 400)
        floor_json = {"name": "Marca2"}
        response = client.post('/' + DEFAULT_VERSION + '/floors', floor_json)
        self.assertEqual(response.status_code, 201)

    def test_remove_brand_in_use(self):
        '''
        Assegura que não seja removida uma marca que pertença a um equipamento.
        '''
        brand_id = Brand.objects.get(name="Marca1").id
        client = APIClient()
        token = Token.objects.get(user__username='testadmin')
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.delete('/' + DEFAULT_VERSION + '/brands/'+str(brand_id))
        self.assertEqual(response.status_code, 405)
        Equipament.objects.get(patrimony="12345678").delete()
        response = client.delete('/' + DEFAULT_VERSION + '/brands/'+str(brand_id))
        self.assertEqual(response.status_code, 204)
        brand_id = Brand.objects.get(name="Marca3").id
        response = client.delete('/' + DEFAULT_VERSION + '/brands/'+str(brand_id))
        self.assertEqual(response.status_code, 204)

    def test_remove_category_in_use(self):
        '''
        Assegura que não seja removida uma categoria que pertença a um equipamento.
        '''
        category_id = Category.objects.get(name="Categoria1").id
        client = APIClient()
        token = Token.objects.get(user__username='testadmin')
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.delete('/' + DEFAULT_VERSION + '/categories/'+str(category_id))
        self.assertEqual(response.status_code, 405)
        Equipament.objects.get(patrimony="12345678").delete()
        response = client.delete('/' + DEFAULT_VERSION + '/categories/'+str(category_id))
        self.assertEqual(response.status_code, 204)
        category_id = Category.objects.get(name="Categoria3").id
        response = client.delete('/' + DEFAULT_VERSION + '/categories/'+str(category_id))
        self.assertEqual(response.status_code, 204)

    def test_remove_model_in_use(self):
        '''
        Assegura que não seja removida um modelo que pertença a um equipamento.
        '''
        model_id = Model.objects.get(name="Modelo1").id
        client = APIClient()
        token = Token.objects.get(user__username='testadmin')
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.delete('/' + DEFAULT_VERSION + '/models/'+str(model_id))
        self.assertEqual(response.status_code, 405)
        Equipament.objects.get(patrimony="12345678").delete()
        response = client.delete('/' + DEFAULT_VERSION + '/models/'+str(model_id))
        self.assertEqual(response.status_code, 204)
        model_id = Model.objects.get(name="Modelo3").id
        response = client.delete('/' + DEFAULT_VERSION + '/models/'+str(model_id))
        self.assertEqual(response.status_code, 204)

    def test_remove_ua_in_use(self):
        '''
        Assegura que não seja removida uma unidade administrativa que pertença a um equipamento.
        '''
        ua_id = Ua.objects.get(code="1").id
        client = APIClient()
        token = Token.objects.get(user__username='testadmin')
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.delete('/' + DEFAULT_VERSION + '/uas/'+str(ua_id))
        self.assertEqual(response.status_code, 405)
        Equipament.objects.get(patrimony="12345678").delete()
        response = client.delete('/' + DEFAULT_VERSION + '/uas/'+str(ua_id))
        self.assertEqual(response.status_code, 204)
        ua_id = Ua.objects.get(code="3").id
        response = client.delete('/' + DEFAULT_VERSION + '/uas/'+str(ua_id))
        self.assertEqual(response.status_code, 204)

class EquipamentsTests(APITestCase):
    def setUp(self):
        test_user = User.objects.create_user('test', password='test2020')
        testadmin_user = User.objects.create_superuser('testadmin', password='testadmin2020')
        Token.objects.create(user=test_user)
        Token.objects.create(user=testadmin_user)
        brand = Brand.objects.create(name='Marca1')
        Brand.objects.create(name='Marca3')
        category = Category.objects.create(name='Categoria1')
        Category.objects.create(name='Categoria3')
        model = Model.objects.create(name='Modelo1')
        Model.objects.create(name='Modelo3')
        floor = Floor.objects.create(name='Andar1')
        Floor.objects.create(name='Andar3')
        ua = Ua.objects.create(code='1', name='Ua1')
        Ua.objects.create(code='3', name='Ua3')
        ua.floor = floor 
        ua.save()
        equipament = Equipament(patrimony='12345678', warranty_start=datetime.datetime(2019, 4,29), warranty_end=datetime.datetime(2020, 4,29), acquisition_date=datetime.datetime(2019, 4,29), acquisition_value=3450.50)
        equipament.brand = brand
        equipament.category = category
        equipament.model = model
        equipament.ua = ua
        equipament.floor = floor
        equipament.save()

    def test_add_status_random(self):
        '''
        Assegura que não sejam adicionados equipamentos com status
        aleatório.
        '''
        category = Category.objects.get(name="Categoria1")
        equipament_json = {"patrimony":"12345670","warranty_start":"2020-05-03","warranty_end":"2020-05-05","acquisition_date":"2020-05-05","acquisition_value":444.0,"status":"Geraldo", "category": "/" + DEFAULT_VERSION + "/categories/"+str(category.id)}
        client = APIClient()
        client.login(username='testadmin', password='testadmin2020')
        response = client.post('/' + DEFAULT_VERSION + '/equipaments', equipament_json, format='json')
        self.assertEqual(response.status_code, 400)
        equipament_json = {"patrimony":"12345670","warranty_start":"2020-05-03","warranty_end":"2020-05-05","acquisition_date":"2020-05-05","acquisition_value":444.0,"status":"Usado", "category": "/" + DEFAULT_VERSION + "/categories/"+str(category.id)}
        client = APIClient()
        client.login(username='testadmin', password='testadmin2020')
        response = client.post('/' + DEFAULT_VERSION + '/equipaments', equipament_json, format='json')
        self.assertEqual(response.status_code, 201)

    def test_add_equipament_with_same_patrimony(self):
        '''
        Assegura que não sejam adicionados equipamentos com o mesmo patrimônios.
        '''
        category = Category.objects.get(name="Categoria1")
        equipament_json = {"patrimony":"12345678","warranty_start":"2020-05-03","warranty_end":"2020-05-05","acquisition_date":"2020-05-05","acquisition_value":444.0,"status":"Geraldo", "category": "/" + DEFAULT_VERSION + "/categories/"+str(category.id)}
        client = APIClient()
        client.login(username='testadmin', password='testadmin2020')
        response = client.post('/' + DEFAULT_VERSION + '/equipaments', equipament_json, format='json')
        self.assertEqual(response.status_code, 400)
        equipament_json = {"patrimony":"12345670","warranty_start":"2020-05-03","warranty_end":"2020-05-05","acquisition_date":"2020-05-05","acquisition_value":444.0,"status":"Usado", "category": "/" + DEFAULT_VERSION + "/categories/"+str(category.id)}
        client = APIClient()
        client.login(username='testadmin', password='testadmin2020')
        response = client.post('/' + DEFAULT_VERSION + '/equipaments', equipament_json, format='json')
        self.assertEqual(response.status_code, 201) 

    def test_add_equipament_with_warranty_conflict(self):
        '''
        Assegura que não sejam adicionados equipamentos com datas de garantias conflitantes. 
        '''
        category = Category.objects.get(name="Categoria1")
        equipament_json = {"patrimony":"12345670","warranty_start":"2020-05-05","warranty_end":"2020-05-03","acquisition_date":"2020-05-05","acquisition_value":444.0,"status":"Geraldo", "category": "/" + DEFAULT_VERSION + "/categories/"+str(category.id)}
        client = APIClient()
        client.login(username='testadmin', password='testadmin2020')
        response = client.post('/' + DEFAULT_VERSION + '/equipaments', equipament_json, format='json')
        self.assertEqual(response.status_code, 400)
        equipament_json = {"patrimony":"12345670","warranty_start":"2020-05-03","warranty_end":"2020-05-05","acquisition_date":"2020-05-05","acquisition_value":444.0,"status":"Usado", "category": "/" + DEFAULT_VERSION + "/categories/"+str(category.id)}
        client = APIClient()
        client.login(username='testadmin', password='testadmin2020')
        response = client.post('/' + DEFAULT_VERSION + '/equipaments', equipament_json, format='json')
        self.assertEqual(response.status_code, 201)
