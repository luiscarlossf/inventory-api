# Generated by Django 3.0.4 on 2020-03-27 23:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20200323_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipament',
            name='brand',
            field=models.ForeignKey(blank=True, help_text='Selecione a marca do equipamento.', on_delete=django.db.models.deletion.PROTECT, to='api.Brand', verbose_name='Marca'),
        ),
        migrations.AlterField(
            model_name='equipament',
            name='category',
            field=models.ForeignKey(blank=True, help_text='Selecione a categoria do equipamento.', on_delete=django.db.models.deletion.PROTECT, to='api.Category', verbose_name='Categoria'),
        ),
        migrations.AlterField(
            model_name='equipament',
            name='description',
            field=models.TextField(blank=True, help_text='Insira uma descrição do equipamento.', max_length=1000, verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='equipament',
            name='model',
            field=models.ForeignKey(blank=True, help_text='Selecione o modelo do equipamento.', on_delete=django.db.models.deletion.PROTECT, to='api.Model', verbose_name='Modelo'),
        ),
        migrations.AlterField(
            model_name='equipament',
            name='ua',
            field=models.ForeignKey(blank=True, help_text='Selecione a unidade administrativa onde o equipamento se encontra.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Ua', verbose_name='Unidade Administrativa'),
        ),
    ]
