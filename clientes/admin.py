from django.contrib import admin
from .models import Cliente, Servico

# Register your models here.
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'endereco')
    search_fields = ('nome', 'documento', 'email', 'telefone', 'endereco')
    ordering = ('nome',)


class ServicoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'data', 'valor', 'status')
    list_filter = ('status', 'data')
    search_fields = ('cliente__nome', 'descricao')
    ordering = ('data',)

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Servico, ServicoAdmin)
