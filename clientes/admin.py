from django.contrib import admin
from .models import Cliente, Servico, AnexoServico


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'endereco', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('nome', 'documento', 'email', 'telefone', 'endereco')
    ordering = ('nome',)


# Inline para permitir gerenciar anexos diretamente dentro da tela de Serviço
class AnexoServicoInline(admin.TabularInline):
    model = AnexoServico
    extra = 1  # Quantidade de campos vazios para novos anexos que aparecerão por padrão


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'data', 'valor', 'status')
    list_filter = ('status', 'data')
    search_fields = ('cliente__nome', 'descricao')
    ordering = ('data',)
    
    # Adiciona a interface de anexos dentro da edição do serviço
    inlines = [AnexoServicoInline]
