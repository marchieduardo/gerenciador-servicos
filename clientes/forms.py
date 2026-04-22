from django import forms
from .models import Servico

class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['descricao', 'data', 'valor', 'status']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_descricao(self):
        descricao = self.cleaned_data['descricao']
        if len(descricao) < 5:
            raise forms.ValidationError('Descrição muito curta.')
        return descricao