# Generated by Django 3.0.4 on 2020-05-16 22:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Insira o nome da marca.', max_length=200, unique=True, verbose_name='Marca')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Insira o nome da categoria.', max_length=200, unique=True, verbose_name='Categoria')),
            ],
        ),
        migrations.CreateModel(
            name='Floor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Insira a descrição do andar do pedrio.', max_length=100, unique=True, verbose_name='Andar')),
            ],
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Insira o nome da modelo.', max_length=200, unique=True, verbose_name='Modelo')),
            ],
        ),
        migrations.CreateModel(
            name='Ua',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='Insira o código da unidade administrativa.', max_length=8, unique=True, verbose_name='Código da UA')),
                ('name', models.CharField(help_text='Insira o nome da unidade administrativa.', max_length=200, unique=True, verbose_name='Nome da UA')),
                ('floor', models.ForeignKey(blank=True, help_text='Selecione o andar da unidade administrativa.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Floor')),
            ],
        ),
        migrations.CreateModel(
            name='Equipament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patrimony', models.CharField(blank=True, help_text='Insira o patrimônio do equipamento.', max_length=8, null=True, unique=True, verbose_name='Patrimônio')),
                ('warranty_start', models.DateField(blank=True, null=True, verbose_name='Início da Garantia')),
                ('warranty_end', models.DateField(blank=True, null=True, verbose_name='Fim da Garantia')),
                ('acquisition_date', models.DateField(blank=True, null=True, verbose_name='Data de Aquisição')),
                ('acquisition_value', models.FloatField(blank=True, null=True, verbose_name='Valor de Aquisição')),
                ('status', models.CharField(choices=[('u', 'Usado'), ('a', 'Almoxarifado'), ('e', 'Estaleiro'), ('s', 'Sucata'), ('d', 'Doação')], default='u', max_length=1, verbose_name='Status de uso')),
                ('brand', models.ForeignKey(blank=True, help_text='Selecione a marca do equipamento.', null=True, on_delete=django.db.models.deletion.PROTECT, to='api.Brand', verbose_name='Marca')),
                ('category', models.ForeignKey(blank=True, help_text='Selecione a categoria do equipamento.', on_delete=django.db.models.deletion.PROTECT, to='api.Category', verbose_name='Categoria')),
                ('floor', models.ForeignKey(blank=True, help_text='Selecione o andar em que o equipamento se encontra.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Floor', verbose_name='Andar')),
                ('model', models.ForeignKey(blank=True, help_text='Selecione o modelo do equipamento.', null=True, on_delete=django.db.models.deletion.PROTECT, to='api.Model', verbose_name='Modelo')),
                ('ua', models.ForeignKey(blank=True, help_text='Selecione a unidade administrativa onde o equipamento se encontra.', null=True, on_delete=django.db.models.deletion.PROTECT, to='api.Ua', verbose_name='Unidade Administrativa')),
            ],
            options={
                'ordering': ['patrimony'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Computer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patrimony', models.CharField(blank=True, help_text='Insira o patrimônio do equipamento.', max_length=8, null=True, unique=True, verbose_name='Patrimônio')),
                ('warranty_start', models.DateField(blank=True, null=True, verbose_name='Início da Garantia')),
                ('warranty_end', models.DateField(blank=True, null=True, verbose_name='Fim da Garantia')),
                ('acquisition_date', models.DateField(blank=True, null=True, verbose_name='Data de Aquisição')),
                ('acquisition_value', models.FloatField(blank=True, null=True, verbose_name='Valor de Aquisição')),
                ('status', models.CharField(choices=[('u', 'Usado'), ('a', 'Almoxarifado'), ('e', 'Estaleiro'), ('s', 'Sucata'), ('d', 'Doação')], default='u', max_length=1, verbose_name='Status de uso')),
                ('policy', models.BooleanField(blank=True, default=False, help_text='Marque se o computador está na política da procuradoria.', null=True, verbose_name='Política')),
                ('status_zenworks', models.BooleanField(blank=True, default=False, help_text='Marque se o computador está sendo monitorado pelo Zenworks.', null=True, verbose_name='Status do Zenworks')),
                ('status_trend', models.BooleanField(blank=True, default=False, help_text='Marque se o computador está sendo monitorado pelo TREND.', null=True, verbose_name='Status do TREND')),
                ('status_wsus', models.BooleanField(blank=True, default=False, help_text='Marque se o computador está sendo monitorado pelo WSUS.', null=True, verbose_name='Status do WSUS')),
                ('brand', models.ForeignKey(blank=True, help_text='Selecione a marca do equipamento.', null=True, on_delete=django.db.models.deletion.PROTECT, to='api.Brand', verbose_name='Marca')),
                ('category', models.ForeignKey(blank=True, help_text='Selecione a categoria do equipamento.', on_delete=django.db.models.deletion.PROTECT, to='api.Category', verbose_name='Categoria')),
                ('floor', models.ForeignKey(blank=True, help_text='Selecione o andar em que o equipamento se encontra.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Floor', verbose_name='Andar')),
                ('model', models.ForeignKey(blank=True, help_text='Selecione o modelo do equipamento.', null=True, on_delete=django.db.models.deletion.PROTECT, to='api.Model', verbose_name='Modelo')),
                ('ua', models.ForeignKey(blank=True, help_text='Selecione a unidade administrativa onde o equipamento se encontra.', null=True, on_delete=django.db.models.deletion.PROTECT, to='api.Ua', verbose_name='Unidade Administrativa')),
            ],
            options={
                'ordering': ['patrimony'],
                'abstract': False,
            },
        ),
    ]