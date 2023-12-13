from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from django.conf import settings
from django.db.models import Count
from django.db.models import Sum
from decimal import Decimal
from django.core.exceptions import MultipleObjectsReturned

ActionCredits = (("Долг", "Долг"),)
ActionPaiements = (("Оплата Долга", "Оплата Долга"),)
ActionCarte = (("Да", "Да"), ("Нет", "Нет"))


class Date(models.Model):
    date = models.CharField(max_length=250, verbose_name="Сегодняшняя дата", unique=True, default="01-01-2024")
    slug = AutoSlugField(populate_from='date', unique=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.date


class Client(models.Model):
    nom = models.CharField(max_length=250, verbose_name="Имя", unique=True)
    slug = AutoSlugField(populate_from='nom', unique=True)
    numero = models.CharField(max_length=250, verbose_name="Телефон", unique=True)
    ville = models.CharField(max_length=250, verbose_name="Город", blank=True)
    adresse = models.CharField(max_length=250, verbose_name="Адрес", blank=True)

    class Meta:
        ordering = ('nom',)

    def get_absolute_url(self):
        return reverse('app:credit_client', args=[self.slug])

    def __str__(self):
        return self.nom


class Credit(models.Model):
    date = models.ForeignKey(Date, on_delete=models.SET_NULL, null=True, verbose_name="дата", default='')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, verbose_name="Покупатель", default='')
    recu = models.CharField(max_length=250, verbose_name="Накладная", unique=True)
    action = models.CharField(max_length=250, choices=ActionCredits, default=1, verbose_name="Действия")
    credit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма ($)")

    class Meta:
        ordering = ('-id',)

    def get_absolute_url(self):
        return reverse('app:credits')

    def __str__(self):
        return str(self.client)


class PaiementsCredit(models.Model):
    date = models.ForeignKey(Date, on_delete=models.SET_NULL, null=True, verbose_name="дата", default='')
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, verbose_name="Покупатель", default='')
    recu = models.IntegerField(verbose_name="Накладная", unique=True)
    action = models.CharField(max_length=250, choices=ActionPaiements, default=1, verbose_name="Действия")
    credit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сумма ($)")

    class Meta:
        ordering = ('-id',)

    def get_absolute_url(self):
        return reverse('app:paiements-credits')

    def __str__(self):
        return str(self.client)


class TitulaireCarte(models.Model):
    nom = models.CharField(max_length=250, verbose_name="Имя", unique=True)
    carteNumber = models.CharField(max_length=250, verbose_name="Номер Карты", unique=True)
    slug = AutoSlugField(populate_from='nom', unique=True)

    class Meta:
        ordering = ('nom',)

    def __str__(self):
        return self.nom


class PaiementCarte(models.Model):
    date = models.ForeignKey(Date, on_delete=models.SET_NULL, null=True, verbose_name="дата")
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, verbose_name="Покупатель")
    recu = models.CharField(max_length=250, verbose_name="Накладная")
    carte = models.ForeignKey(TitulaireCarte, on_delete=models.SET_NULL, null=True, verbose_name="Карта")
    montant = models.DecimalField(max_digits=10, decimal_places=2, null=True, verbose_name="Сумма ($)")
    action = models.CharField(max_length=250, choices=ActionCarte, default=1, verbose_name="Оплата", blank=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return str(self.client)
