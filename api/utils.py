from .models import Brand, Category, Computer, Equipament, Floor, Model, Ua
from rest_framework.settings import api_settings
import re

def get_version_default():
    """Retorna a versão padrão da API

    Returns:
        str -- versão padrão da API
    """
    return str(api_settings.DEFAULT_VERSION)

def delete_all_database():
    """Exclue todos os dados do banco de dados.
    """
    Computer.objects.all().delete() #Deleta primeiro os computadores e equipamentos,
    Equipament.objects.all().delete() #pois possuem campos protegidos.
    
    Ua.objects.all().delete()
    Brand.objects.all().delete()
    Category.objects.all().delete()
    Model.objects.all().delete()
    Floor.objects.all().delete()

def isUnique(error):
    return error.code == 'unique'

def save_data_from_sheet(string, reg_exp, fields, serializer, model, uris=None, request=None):
    """Armazena os dados de uma célula da planilha no banco de dados
    da API.

    Arguments:
        string {string} -- String de uma celúla da planilha.
        reg_exp {string} -- Expressão Regular que define o padrão dos dados na 
            string para o modelo.
        fields {list} -- Os campos do modelo que deseja armazenar presentes nos 
            grupos da expressão regular.
        serializer {class} -- O serializador do modelo.
        model {class} -- O modelo dos dados.

    Returns:
        [integer] -- Retorna o identificador instância do modelo salva ou None 
            caso os dados não puderam ser salvos.
    """
    match = re.search(reg_exp, string) #Combina a string com a expressão regular
    #print(string)
    if match:
        data = dict()
        for field in fields:
            if field != 'acquisition_value':
                data[field] = match.groupdict()[field]
            else:
                data[field] = float(match.groupdict()[field])
        if uris: #prenche as chaves estrangeiras
            for field in uris:
                data[field] = uris[field]
        obj = serializer(data=data, context={'request': request})

        if obj.is_valid():
            return obj.save().id
        else:
            for field in obj.errors:
                if isUnique(obj.errors[field][0]):
                    kwargs = {field: data[field]}
                    saved_data_id = model.objects.get(**kwargs).id
                    return saved_data_id 
            raise AttributeError("Saving data from sheet: dados inválidos. \n"+ str(uris) + str(obj.errors))
    else:
        return None