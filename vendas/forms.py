from django import forms

from produtos.models import Produto


class VendaForm(forms.Form):
    produto = forms.ModelChoiceField(
        queryset=Produto.objects.none(),
        label='Produto',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    quantidade = forms.IntegerField(
        min_value=1,
        label='Quantidade vendida',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'step': '1'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['produto'].queryset = Produto.objects.order_by('nome')
