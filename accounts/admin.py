from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('is_staff', 'username')

    # Adiciona o campo telefone ao formulário de edição
    fieldsets = UserAdmin.fieldsets + (('Informações Extras', {'fields': ('telefone',)}),)
    
    # Adiciona o campo telefone ao formulário de criação
    add_fieldsets = UserAdmin.add_fieldsets + (('Informações Extras', {'fields': ('telefone',)}),)
