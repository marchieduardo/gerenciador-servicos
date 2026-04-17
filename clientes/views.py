from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .models import Cliente

# Create your views here.
class ListaClientesView(ListView):
    model = Cliente
    template_name = 'lista_clientes.html'
    context_object_name = 'clientes'


class CriarClienteView(CreateView):
    model = Cliente
    template_name = 'criar_cliente.html'
    fields = '__all__'
    success_url = '/clientes/'