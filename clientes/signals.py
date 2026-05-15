import os
from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import AnexoServico

@receiver(post_delete, sender=AnexoServico)
def excluir_arquivo_anexo(sender, instance, **kwargs):
    """
    Exclui o arquivo do disco físico quando o objeto AnexoServico correspondente
    é excluído do banco de dados.
    """
    if instance.arquivo:
        if os.path.isfile(instance.arquivo.path):
            os.remove(instance.arquivo.path)
