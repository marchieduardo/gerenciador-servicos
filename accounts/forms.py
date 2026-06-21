from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="E-mail ou Usuário",
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite seu e-mail ou usuário',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite sua senha',
        })
    )
