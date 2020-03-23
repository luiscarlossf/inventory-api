from django.contrib import admin
from .models import Brand, Category, Computer, Equipament, Floor, Model, Ua
# Register your models here.
admin.site.register([Brand, Category, Computer, Equipament, Floor, Model, Ua])
