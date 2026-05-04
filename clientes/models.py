from django.db import models

# Create your models here.
class Cliente(models.Model):
    id = models.AutoField(primary_key=True) 
    nome = models.CharField(max_length=100)
    documento = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    endereco = models.CharField(max_length=200, null=True, blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Servico(models.Model):
    STATUS_SERVICO = [
        ('P', 'Pendente'),
        ('C', 'Concluído'),
        ('X', 'Cancelado'),
    ]
    
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='servicos'
    )
    descricao = models.TextField()
    data = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=1, choices=STATUS_SERVICO, default='P')
    anexo = models.FileField(upload_to='anexos_servicos/', null=True, blank=True)

    @property
    def is_anexo_image(self):
        if self.anexo:
            extensao = self.anexo.name.split('.')[-1].lower()
            return extensao in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp']
        return False

    def __str__(self):
        return f'{self.cliente} - {self.data}'