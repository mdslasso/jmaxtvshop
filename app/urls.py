from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'app'
urlpatterns = [
    path('home/', views.home, name='home'),

    path('credits/', views.credits, name='credits'),
    path('add-credits/', views.AddCredit.as_view(), name='add-credits'),
    path('edit-credit/<int:pk>/', views.EditCredit.as_view(), name='edit-credits'),
    path('delete-credit/<int:pk>/', views.DeleteCredit.as_view(), name='delete-credits'),

    path('paiement-credits/', views.paiements_credits, name='paiements-credits'),
    path('add-paiements/', views.AddPaiement.as_view(), name='add-paiements'),
    path('edit-paiements/<int:pk>/', views.EditPaiement.as_view(), name='edit-paiements'),
    path('delete-paiements/<int:pk>/', views.DeletePaiement.as_view(), name='delete-paiements'),

    path('clients/', views.clients, name='clients'),
    path('<slug:client_slug>', views.clientdetail, name='credit_client'),
    path('add-clients/', views.AddClient.as_view(), name='add-client'),
    path('edit-clients/<int:pk>/', views.EditClient.as_view(), name='edit-client'),
    path('delete-clients/<int:pk>/', views.DeleteClient.as_view(), name='delete-client'),
    path('search-client/', views.SearchClient.as_view(), name='search-client'),

    path('cartes/', views.cartes, name='cartes'),
    path('search-titulaire-carte/', views.SearchTitulaireCartes.as_view(), name='search-titulaire-carte'),

    path('add-dates/', views.AddDates.as_view(), name='add-dates'),
    path('delete-dates/<int:pk>/', views.DeleteDates.as_view(), name='delete-dates'),

    path('', auth_views.LoginView.as_view(template_name='admin/login_page.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]
