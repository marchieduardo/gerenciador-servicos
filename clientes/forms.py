from django import forms
from .models import Servico

class MultipleFileInput(forms.ClearableFileInput):
    """Widget que permite a seleção e captura de múltiplos arquivos no mesmo input."""
    allow_multiple_selected = True

    def value_from_datadict(self, data, files, name):
        # Captura a lista completa de arquivos enviados, em vez de apenas o último.
        if hasattr(files, 'getlist'):
            return files.getlist(name)
        return files.get(name)

class MultipleFileField(forms.FileField):
    """Campo de formulário que valida individualmente cada arquivo de uma lista de uploads."""
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={'multiple': True}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        # Itera e valida cada arquivo da lista usando a lógica padrão do FileField.
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class ServicoForm(forms.ModelForm):
    anexos = MultipleFileField(
        required=False,
        label='Anexos'
    )

    class Meta:
        model = Servico
        fields = ['descricao', 'data', 'valor', 'status']
        widgets = {
            'data': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }

    def clean_descricao(self):
        descricao = self.cleaned_data['descricao']
        if len(descricao) < 5:
            raise forms.ValidationError('Descrição muito curta.')
        return descricao