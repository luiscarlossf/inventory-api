from django.contrib import admin
from .models import Brand, Category, Computer, Equipament, Floor, Model, Ua
# Registrando os modelos no admin do Django
admin.site.register([Brand, Category, Computer, Equipament, Floor, Model, Ua])
