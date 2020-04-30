from django.db import models
from django.core.exceptions import ValidationError

class Category(models.Model):
    """
    Modelo representando uma categoria de um equipamento.
    """
    name = models.CharField("Categoria", max_length=200, unique=True, help_text="Insira o nome da categoria.")

    def __str__(self):
        """
        String representanda a categoria.
        """
        return self.name

class Floor(models.Model):
    """
    Modelo representando um andar do prédio.
    """
    name = models.CharField("Andar", max_length=100, unique=True, help_text="Insira a descrição do andar do pedrio.")

    def __str__(self):
        """
        String representanda o andar.
        """
        return self.name

class Ua(models.Model):
    """
    Modelo representando uma unidade administrativa da Procuradoria da República.
    """
    code = models.CharField("Código da UA", unique=True, max_length=8, help_text="Insira o código da unidade administrativa.")
    name = models.CharField("Nome da UA", unique=True, max_length=200, help_text="Insira o nome da unidade administrativa.")
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, blank=True, null=True, help_text="Selecione o andar da unidade administrativa.")

    def __str__(self):
        """
        String representanda a unidade administrativa.
        """
        return self.name

class Brand(models.Model):
    """
    Modelo representando uma marca de um equipamento.
    """
    name = models.CharField("Marca", max_length=200, unique=True, help_text="Insira o nome da marca.")

    def __str__(self):
        """
        String representanda a marca.
        """
        return self.name

class Model(models.Model):
    """
    Modelo representando um modelo de equipamento.
    """
    name = models.CharField("Modelo", max_length=200, unique=True, help_text="Insira o nome da modelo.")

    def __str__(self):
        """
        String representanda o modelo.
        """
        return self.name

class Equipament(models.Model):
    """
    Modelo representando um equipamento.
    """
    patrimony = models.CharField("Patrimônio", unique=True, max_length=8, blank = True, null=True, help_text="Insira o patrimônio do equipamento.")
    brand = models.ForeignKey(Brand, verbose_name="Marca", blank=True, null=True, on_delete=models.PROTECT, help_text="Selecione a marca do equipamento.")
    category = models.ForeignKey(Category, verbose_name="Categoria", blank=True, on_delete=models.PROTECT, help_text="Selecione a categoria do equipamento." )
    model = models.ForeignKey(Model, verbose_name="Modelo", blank=True, null=True, on_delete=models.PROTECT, help_text="Selecione o modelo do equipamento.")
    warranty_start = models.DateField("Início da Garantia", null=True, blank=True)
    warranty_end = models.DateField("Fim da Garantia", null=True, blank=True)
    ua = models.ForeignKey(Ua, on_delete=models.SET_NULL, verbose_name="Unidade Administrativa",null=True, blank=True, help_text="Selecione a unidade administrativa onde o equipamento se encontra.")
    floor = models.ForeignKey(Floor, on_delete=models.SET_NULL, verbose_name="Andar", null=True, blank=True, help_text="Selecione o andar em que o equipamento se encontra.")
    acquisition_date = models.DateField("Data de Aquisição", null=True, blank=True)
    acquisition_value = models.FloatField("Valor de Aquisição", null=True, blank=True)
    
    _STATUS = (
        ('u', 'Usado'),
        ('a', 'Almoxarifado'),
        ('e', 'Estaleiro'),
        ('s', 'Sucata'),
        ('d', 'Doação'),
    )

    status = models.CharField("Status de uso", max_length=1, choices=_STATUS, default='u')

    def clean(self):
        #Não permite que sejam adicionadas datas de garantias sem lógica.
        if (self.warranty_start and self.warranty_end) and (self.warranty_start > self.warranty_end):
            raise ValidationError({"warranty_end":_("Data de fim de garantia menor que a data de início de garantia.")})

    def __str__(self):
        """
        String representando o equipamento
        """
        return "{0} - {1} - {2} - {3}".format(self.patrimony, self.category, self.brand, self.model)
    
    def getDescription(self):
        """
        String descrevendo o equipamento
        """
        return self.category + self.brand + self.model

class Computer(Equipament):
    """
    Modelo representando um computador
    """
    
    policy = models.BooleanField("Política", default=False, blank=True, null=True, help_text="Marque se o computador está na política da procuradoria.")
    status_zenworks = models.BooleanField("Status do Zenworks", default=False, blank=True, null=True, help_text="Marque se o computador está sendo monitorado pelo Zenworks.")
    status_trend = models.BooleanField("Status do TREND", default=False, blank=True, null=True, help_text="Marque se o computador está sendo monitorado pelo TREND.")
    status_wsus = models.BooleanField("Status do WSUS", default=False, blank=True, null=True, help_text="Marque se o computador está sendo monitorado pelo WSUS.")