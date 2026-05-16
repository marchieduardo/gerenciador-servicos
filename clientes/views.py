from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .models import Cliente, Servico, AnexoServico
from .forms import ServicoForm

# Views de Clientes

class ListaClientesView(ListView):
    model = Cliente
    template_name = 'lista_clientes.html'
    context_object_name = 'clientes'

    # Retorna a lista de clientes que estão marcados como ativos
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


# Views de Serviços


class CriarServicoView(CreateView):
    model = Servico
    template_name = 'criar_servico.html'
    form_class = ServicoForm
    
    # Inicializa a view garantindo que o cliente exista e esteja ativo
    def dispatch(self, request, *args, **kwargs):
        self.cliente = get_object_or_404(
            Cliente,
            pk=kwargs['pk'],
            ativo=True
        )
        return super().dispatch(request, *args, **kwargs)

    # Adiciona o objeto cliente ao contexto do template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cliente'] = self.cliente
        return context

    # Associa o serviço ao cliente e processa o upload de múltiplos anexos
    def form_valid(self, form):
        form.instance.cliente = self.cliente
        response = super().form_valid(form)
        for arquivo in self.request.FILES.getlist('anexos'):
            AnexoServico.objects.create(servico=self.object, arquivo=arquivo)
        return response

    def get_success_url(self):
        return reverse('detalhes-cliente', kwargs={'pk': self.cliente.pk})


class ListaServicosView(ListView):
    model = Servico
    template_name = 'lista_servicos.html'
    context_object_name = 'servicos'


class DetalhesServicoView(DetailView):
    model = Servico
    template_name = 'detalhes_servico.html'
    context_object_name = 'servico'

    # Gerencia a URL de retorno na sessão para navegação inteligente
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        referer = self.request.META.get('HTTP_REFERER')
        
        # Se o referer for válido (não é a própria página, edição ou exclusão), salvamos na sessão
        if referer and referer != self.request.build_absolute_uri() and 'editar' not in referer and 'excluir' not in referer:
            self.request.session['servico_voltar_url'] = referer
            
        # Recuperamos da sessão o último ponto de origem válido
        context['voltar_url'] = self.request.session.get('servico_voltar_url')
        return context


class EditarServicoView(UpdateView):
    model = Servico
    template_name = 'editar_servico.html'
    form_class = ServicoForm

    # Salva as alterações do serviço e processa novos anexos enviados
    def form_valid(self, form):
        response = super().form_valid(form)
        for arquivo in self.request.FILES.getlist('anexos'):
            AnexoServico.objects.create(servico=self.object, arquivo=arquivo)
        return response

    def get_success_url(self):
        return reverse('detalhes-servico', kwargs={'pk': self.object.pk})


class ExcluirServicoView(DeleteView):
    model = Servico
    template_name = 'excluir_servico.html'
    context_object_name = 'servico'

    def get_success_url(self):
        # Recuperamos da sessão o último ponto de origem válido
        voltar_url = self.request.session.get('servico_voltar_url')
        
        if voltar_url:
            return voltar_url
            
        return reverse('lista-servicos') # fallback


class ExcluirAnexoView(DeleteView):
    model = AnexoServico

    # Realiza a exclusão lógica/física do anexo via requisição AJAX
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()  # Apaga o anexo do banco de dados, disparando o signal para apagar o arquivo físico
        return JsonResponse({'status': 'success'})

    def get_success_url(self):
        return reverse('detalhes-servico', kwargs={'pk': self.object.servico.pk})
