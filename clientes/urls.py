from django.urls import path
from . import views

urlpatterns = [
    path('clientes/', views.ListaClientesView.as_view(), name='lista-clientes'),
]