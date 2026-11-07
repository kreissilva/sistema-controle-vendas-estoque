from django import forms

from .models import Produto


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'categoria', 'preco', 'quantidade_estoque', 'estoque_minimo']
        labels = {
            'nome': 'Nome do produto',
            'categoria': 'Categoria',
            'preco': 'Preço de venda',
            'quantidade_estoque': 'Quantidade disponível em estoque',
            'estoque_minimo': 'Quantidade mínima de estoque',
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: Café 500 g'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: Bebidas'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'min': '0.01', 'step': '0.01'}),
            'quantidade_estoque': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '1'}),
            'estoque_minimo': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '1'}),
        }
