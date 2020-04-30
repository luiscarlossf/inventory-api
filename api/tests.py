import datetime
from django.test import TestCase, TransactionTestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from .models import Brand, Category, Computer, Equipament, Floor, Model, Ua

#### TESTE DE MODELOS ###########
class BrandModelTests(TransactionTestCase):
    def setUp(self):
        Brand.objects.create(name="brand1")
        Brand.objects.create(name="brand2")
        Brand.objects.create(name="brand3")
    
    def test_add_with_same_name(self):
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
        with self.assertRaises(IntegrityError):
            computer = Computer(patrimony='12345678', warranty_start=datetime.datetime(2019, 4,29), warranty_end=datetime.datetime(2020, 4,29), acquisition_date=datetime.datetime(2019, 4,29), acquisition_value=3450.50)
            computer.brand = Brand.objects.get(name='brand1')
            computer.category = Category.objects.get(name="category1")
            computer.model = Model.objects.get(name="model1")
            computer.ua = Ua.objects.get(code="12345678")
            computer.floor = Floor.objects.get(name="floor1")
            computer.save()

    def test_add_status_out_enum(self):
        with self.assertRaises(ValidationError):
            computer = Computer.objects.get(patrimony='12345678')
            computer.status = "A"
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



#### TESTE DE SERIALIZERS ###########

#### TESTE DE VIEWSETS ############
