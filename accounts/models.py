from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    telefone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True) # Redefinindo o campo padrão email para torná-lo unique

    USERNAME_FIELD = 'email' # Dizendo ao Django que o campo de login será o email
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

    # Sobreescrevendo método padrão para retornar o username caso o campo first_name estiver vazio.
    # Obs: Por padrão o fallback usava get_username(), que retornava o email pois definimos como USERNAME_FIELD.
    def get_short_name(self):
        if self.first_name:
            return self.first_name
        return self.username # fallback
