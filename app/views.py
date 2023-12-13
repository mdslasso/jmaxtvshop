from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView, )
from .filters import *
from .models import *
from django.urls import reverse
from django.db.models import Q
from itertools import chain
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User


def home(request):
    return render(request, 'app/home.html')


def credits(request):
    credits = Credit.objects.all().order_by('-id')
    clients = Client.objects.all().order_by('-id')
    credits_filters = Credit.objects.all().order_by('-id')
    myFilter = CreditFilter(request.GET, queryset=credits_filters)
    credits_filters = myFilter.qs
    total_credit = myFilter.qs.aggregate(Sum('credit'))
    context = {
        'credits': credits,
        'clients': clients,
        'credits_filters': credits_filters,
        'myFilter': myFilter,
        'total_credit': total_credit,

    }

    return render(request, 'app/credits.html', context)


class AddCredit(CreateView):
    model = Credit
    template_name = 'app/add_credits.html'
    fields = ['date', 'client', 'recu', 'action', 'credit']

    def get_context_data(self, *args, **kwargs):
        context = super(AddCredit, self).get_context_data(*args, **kwargs)
        context['credits'] = Credit.objects.all().order_by('-id')[:3]
        context['clients'] = Client.objects.all().order_by('-id')
        return context


class EditCredit(UpdateView):
    model = Credit
    template_name = 'app/edit_credit.html'
    fields = ['date', 'client', 'recu', 'action', 'credit']

    def get_success_url(self):
        return reverse('app:credits')

    def get_context_data(self, *args, **kwargs):
        context = super(EditCredit, self).get_context_data(*args, **kwargs)
        context['credits'] = Credit.objects.all().order_by('-id')[:5]
        context['clients'] = Client.objects.all().order_by('-id')
        return context


class DeleteCredit(DeleteView):
    model = Credit
    template_name = 'app/delete_credit.html'

    def get_success_url(self):
        return reverse('app:credits')

    def get_context_data(self, *args, **kwargs):
        context = super(DeleteCredit, self).get_context_data(*args, **kwargs)
        context['clients'] = Client.objects.all().order_by('-id')
        return context


def paiements_credits(request):
    paiements = PaiementsCredit.objects.all().order_by('-id')
    clients = Client.objects.all().order_by('-id')
    paiements_filters = PaiementsCredit.objects.all().order_by('-id')
    myFilter = PaiementsFilter(request.GET, queryset=paiements_filters)
    paiements_filters = myFilter.qs
    total_paiement = myFilter.qs.aggregate(Sum('credit'))

    context = {
        'paiements': paiements,
        'clients': clients,
        'paiements_filters': paiements_filters,
        'myFilter': myFilter,
        'total_paiement': total_paiement,
    }

    return render(request, 'app/paiement_credits.html', context)


class AddPaiement(CreateView):
    model = PaiementsCredit
    template_name = 'app/add_paiements.html'
    fields = ['date', 'client', 'recu', 'action', 'credit']

    def get_context_data(self, *args, **kwargs):
        context = super(AddPaiement, self).get_context_data(*args, **kwargs)
        context['paiements'] = PaiementsCredit.objects.all().order_by('-id')[:3]
        context['clients'] = Client.objects.all().order_by('-id')
        return context


class EditPaiement(UpdateView):
    model = PaiementsCredit
    template_name = 'app/edit_paiement.html'
    fields = ['date', 'client', 'recu', 'action', 'credit']

    def get_context_data(self, *args, **kwargs):
        context = super(EditPaiement, self).get_context_data(*args, **kwargs)
        context['paiements'] = PaiementsCredit.objects.all().order_by('-id')[:3]
        context['clients'] = Client.objects.all().order_by('-id')
        return context


class DeletePaiement(DeleteView):
    model = PaiementsCredit
    template_name = 'app/delete_paiement.html'

    def get_success_url(self):
        return reverse('app:paiements-credits')

    def get_context_data(self, *args, **kwargs):
        context = super(DeletePaiement, self).get_context_data(*args, **kwargs)
        context['paiements'] = PaiementsCredit.objects.all().order_by('-id')[:3]
        context['clients'] = Client.objects.all().order_by('-id')
        return context


def clients(request):
    clients = Client.objects.all().order_by('nom')
    credits = Credit.objects.all().order_by('-id')
    paiements = PaiementsCredit.objects.all().order_by('-id')
    total_credit = credits.aggregate(Sum('credit'))
    total_paiement = paiements.aggregate(Sum('credit'))
    context = {
        'clients': clients,
        'credits': credits,
        'paiements': paiements,
        'total_credit': total_credit,
        'total_paiement': total_paiement,

    }

    return render(request, 'app/clients.html', context)


def clientdetail(request, client_slug=None):
    client = None
    clients = Client.objects.all()
    credits = Credit.objects.all().order_by('-pk')
    paiements = PaiementsCredit.objects.all().order_by('-pk')
    credit_client = Credit.objects.all()
    paiement_client = PaiementsCredit.objects.all()

    if client_slug:
        client = get_object_or_404(Client, slug=client_slug)
        credits = credits.filter(client=client).order_by('-id')
        paiements = paiements.filter(client=client).order_by('-id')
        credit_client = credit_client.filter(client=client).aggregate(Sum('credit'))
        paiement_client = paiement_client.filter(client=client).aggregate(Sum('credit'))

    return render(request, 'app/clients.html', {
        'clients': clients,
        'paiements': paiements,
        'credits': credits,
        'client': client,
        'credit_client': credit_client,
        'paiement_client': paiement_client

    })


class AddClient(CreateView):
    model = Client
    template_name = 'app/add_clients.html'
    fields = ['nom', 'numero', 'ville', 'adresse']

    def get_success_url(self):
        return reverse('app:clients')

    def get_context_data(self, *args, **kwargs):
        context = super(AddClient, self).get_context_data(*args, **kwargs)
        context['clients'] = Client.objects.all().order_by('nom')
        return context


class EditClient(UpdateView):
    model = Client
    template_name = 'app/edit_clients.html'
    fields = ['nom', 'numero', 'ville', 'adresse']

    def get_success_url(self):
        return reverse('app:clients')

    def get_context_data(self, *args, **kwargs):
        context = super(EditClient, self).get_context_data(*args, **kwargs)
        context['clients'] = Client.objects.all().order_by('nom')
        return context


class DeleteClient(DeleteView):
    model = Client
    template_name = 'app/delete_client.html'

    def get_success_url(self):
        return reverse('app:clients')

    def get_context_data(self, *args, **kwargs):
        context = super(DeleteClient, self).get_context_data(*args, **kwargs)
        context['clients'] = Client.objects.all().order_by('nom')
        return context


class SearchClient(ListView):
    model = Client
    paginate_by = 15
    count = 0
    template_name = 'app/clients.html'

    def get_success_url(self):
        return reverse('app:clients')

    def get_context_data(self, *args, **kwargs):
        context = super(SearchClient, self).get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        context['clients'] = Client.objects.all().order_by('nom')
        context['total_credit'] = Credit.objects.all().aggregate(Sum('credit'))
        context['total_paiement'] = PaiementsCredit.objects.all().aggregate(Sum('credit'))
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)

        if query is not None:
            nom = Client.objects.filter(Q(nom__icontains=query))
            numero = Client.objects.filter(Q(numero__icontains=query))
            queryset_chain = chain(nom, numero)

            qs = sorted(queryset_chain, key=lambda instance: instance.pk, reverse=True)
            self.count = len(qs)
            return qs

        return Client.objects.none()


def cartes(request):
    titulaireCarte = TitulaireCarte.objects.all().order_by('nom')
    paiementCarte = PaiementCarte.objects.all().order_by('-id')
    clients = Client.objects.all().order_by('-id')
    context = {
        'titulaireCarte': titulaireCarte,
        'paiementCarte': paiementCarte,
        'clients': clients,

    }

    return render(request, 'app/cartes.html', context)


class SearchTitulaireCartes(ListView):
    model = TitulaireCarte
    paginate_by = 15
    count = 0
    template_name = 'app/cartes.html'

    def get_success_url(self):
        return reverse('app:cartes')

    def get_context_data(self, *args, **kwargs):
        context = super(SearchTitulaireCartes, self).get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        context['titulaireCarte'] = TitulaireCarte.objects.all().order_by('nom')
        context['paiementCarte'] = PaiementCarte.objects.all().order_by('id')

        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)

        if query is not None:
            nom = TitulaireCarte.objects.filter(Q(nom__icontains=query))
            queryset_chain = chain(nom)

            qs = sorted(queryset_chain, key=lambda instance: instance.pk, reverse=True)
            self.count = len(qs)
            return qs

        return TitulaireCarte.objects.none()


class AddDates(CreateView):
    model = Date
    template_name = 'app/dates.html'
    fields = ['date']

    def get_success_url(self):
        return reverse('app:add-dates')

    def get_context_data(self, *args, **kwargs):
        context = super(AddDates, self).get_context_data(*args, **kwargs)
        context['clients'] = Client.objects.all().order_by('nom')
        context['dates'] = Date.objects.all().order_by('-id')[:1]
        return context


class DeleteDates(DeleteView):
    model = Date
    template_name = 'app/delete_dates.html'

    def get_success_url(self):
        return reverse('app:add-dates')

    def get_context_data(self, *args, **kwargs):
        context = super(DeleteDates, self).get_context_data(*args, **kwargs)
        context['clients'] = Client.objects.all().order_by('nom')
        context['dates'] = Date.objects.all().order_by('-id')[:1]
        return context
