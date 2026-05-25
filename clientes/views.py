from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.db.models import Q

from .models import Cliente, Servico, AnexoServico
from .forms import ServicoForm

# Views de Clientes

class ListaClientesView(ListView):
    model = Cliente
    template_name = 'lista_clientes.html'
    context_object_name = 'clientes'

    # Retorna a lista de clientes, permitindo filtro por status (ativo/inativo) e busca textual
    def get_queryset(self):
        queryset = Cliente.objects.all()
        
        # Filtro por status (padrão é mostrar apenas os ativos)
        status_filter = self.request.GET.get('ativo', 'True')
        if status_filter == 'True':
            queryset = queryset.filter(ativo=True)
        elif status_filter == 'False':
            queryset = queryset.filter(ativo=False)
        # Se for diferente de 'True' ou 'False' (Ex: 'Todos'), não aplica filtro de status
            
        # Busca textual em múltiplos campos (nome, documento, email, telefone, endereco)
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(nome__icontains=search_query) |
                Q(documento__icontains=search_query) |
                Q(email__icontains=search_query) |
                Q(telefone__icontains=search_query) |
                Q(endereco__icontains=search_query)
            )
            
        return queryset


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

    # Adiciona o objeto cliente e extensões permitidas ao contexto do template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cliente'] = self.cliente
        context['extensoes_imagem'] = AnexoServico.EXTENSOES_IMAGEM
        context['extensoes_video'] = AnexoServico.EXTENSOES_VIDEO
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

    # Retorna a lista de serviços, permitindo filtro por status, busca textual e ordenação
    def get_queryset(self):
        queryset = Servico.objects.all()
        
        # Filtro de Texto (Nome do cliente ou descrição do serviço)
        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(cliente__nome__icontains=search_query) |
                Q(descricao__icontains=search_query)
            )
            
        # Filtro por Status do Serviço
        status_filter = self.request.GET.get('status', '').strip()
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        # Ordenação por data (padrão: mais recentes primeiro)
        ordem = self.request.GET.get('ordem', 'desc')
        if ordem == 'asc':
            queryset = queryset.order_by('data')
        else:
            queryset = queryset.order_by('-data')
            
        return queryset


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['extensoes_imagem'] = AnexoServico.EXTENSOES_IMAGEM
        context['extensoes_video'] = AnexoServico.EXTENSOES_VIDEO
        return context

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
