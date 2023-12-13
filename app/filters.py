import django_filters
from .models import *


class CreditFilter(django_filters.FilterSet):
    class Meta:
        model = Credit
        fields = ['client', 'date']


class PaiementsFilter(django_filters.FilterSet):
    class Meta:
        model = PaiementsCredit
        fields = ['client', 'date']
