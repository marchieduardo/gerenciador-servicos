from django.contrib import admin
from .models import Cliente, Servico

# Register your models here.
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'endereco', 'ativo')
    list_filter = ('ativo',)
    search_fields = ('nome', 'documento', 'email', 'telefone', 'endereco')
    ordering = ('nome',)


@admin.register(Servico)
class ServicoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'data', 'valor', 'status')
    list_filter = ('status', 'data')
    search_fields = ('cliente__nome', 'descricao')
    ordering = ('data',)
