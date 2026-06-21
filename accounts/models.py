from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    telefone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True) # Redefinindo o campo padrão email para torná-lo unique

    def __str__(self):
        return self.username
