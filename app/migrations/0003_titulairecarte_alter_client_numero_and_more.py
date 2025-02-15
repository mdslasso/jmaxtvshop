# Generated by Django 4.2.1 on 2023-10-22 05:54

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_credit_action_paiementscredit'),
    ]

    operations = [
        migrations.CreateModel(
            name='TitulaireCarte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=250, unique=True, verbose_name='Имя')),
                ('carteNumber', models.CharField(max_length=250, unique=True, verbose_name='Номер Карты')),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='nom', unique=True)),
            ],
            options={
                'ordering': ('nom',),
            },
        ),
        migrations.AlterField(
            model_name='client',
            name='numero',
            field=models.CharField(max_length=250, unique=True, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='paiementscredit',
            name='action',
            field=models.CharField(choices=[('Оплата Долга', 'Оплата Долга')], default=1, max_length=250, verbose_name='Действия'),
        ),
        migrations.AlterField(
            model_name='paiementscredit',
            name='recu',
            field=models.IntegerField(unique=True, verbose_name='Накладная'),
        ),
        migrations.CreateModel(
            name='Carte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recu', models.CharField(max_length=250, verbose_name='Накладная')),
                ('montant', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Сумма ($)')),
                ('carte', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.titulairecarte', verbose_name='Карта')),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.client', verbose_name='Покупатель')),
                ('date', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.date', verbose_name='дата')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
    ]
