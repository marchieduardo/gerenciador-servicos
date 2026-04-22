from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from .models import Cliente, Servico

# Create your views here.
class ListaClientesView(ListView):
    model = Cliente
    template_name = 'lista_clientes.html'
    context_object_name = 'clientes'

    def get_queryset(self):
        return Cliente.objects.filter(ativo=True)


class CriarClienteView(CreateView):
    model = Cliente
    template_name = 'criar_cliente.html'
    fields = ['nome', 'documento', 'email', 'telefone', 'endereco']
    success_url = '/clientes/'


class DetalhesClienteView(DetailView):
    model = Cliente
    template_name = 'detalhes_cliente.html'
    context_object_name = 'cliente'


class EditarClienteView(UpdateView):
    model = Cliente
    template_name = 'editar_cliente.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('detalhes-cliente', kwargs={'pk': self.object.pk})