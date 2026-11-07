from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F


class Produto(models.Model):
    nome = models.CharField(max_length=200)
    categoria = models.CharField(max_length=100, blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade_estoque = models.IntegerField()
    estoque_minimo = models.IntegerField(default=0)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nome']

    @property
    def estoque_baixo(self):
        return self.quantidade_estoque <= self.estoque_minimo

    def clean(self):
        super().clean()
        if self.preco is None or self.preco <= Decimal('0.00'):
            raise ValidationError({'preco': 'O preço de venda deve ser maior que zero.'})
        if self.quantidade_estoque < 0:
            raise ValidationError({'quantidade_estoque': 'A quantidade em estoque não pode ser negativa.'})
        if self.estoque_minimo < 0:
            raise ValidationError({'estoque_minimo': 'O estoque mínimo não pode ser negativo.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.nome
