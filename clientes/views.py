from django.shortcuts import render
from django.views.generic import ListView
from .models import Cliente

# Create your views here.
class ListaClientesView(ListView):
    model = Cliente
    template_name = 'lista_clientes.html'
    context_object_name = 'clientes'
