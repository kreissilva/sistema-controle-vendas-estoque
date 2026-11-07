from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models

from produtos.models import Produto


class Venda(models.Model):
    STATUS_CHOICES = [
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    ]

    data_hora = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='concluida')

    def __str__(self):
        return f'Venda #{self.pk}'


class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.IntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def clean(self):
        super().clean()
        if self.quantidade <= 0:
            raise ValidationError({'quantidade': 'A quantidade vendida deve ser maior que zero.'})
        if self.preco_unitario <= Decimal('0.00'):
            raise ValidationError({'preco_unitario': 'O preço unitário deve ser maior que zero.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.produto.nome} - {self.quantidade}'
