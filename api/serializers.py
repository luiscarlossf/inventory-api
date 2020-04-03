"""
Serializers allow complex data such as querysets and model instances to be converted 
to native Python datatypes that can then be easily rendered into JSON, XML or other 
content types. Serializers also provide deserialization, allowing parsed data to be 
converted back into complex types, after first validating the incoming data.
"""

from django.contrib.auth.models import User, Group
from .models import Brand, Category, Computer, Equipament, Floor, Model, Ua
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class BrandSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ComputerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Computer
        fields = '__all__'


class EquipamentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Equipament
        fields = '__all__'


class FloorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Floor
        fields = '__all__'


class ModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Model
        fields = '__all__'


class UaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ua
        fields = '__all__'

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField(write_only=True, help_text="Insira o arquivos no formato CSV.")