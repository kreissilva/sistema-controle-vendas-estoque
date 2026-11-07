from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import render

from produtos.models import Produto
from .forms import VendaForm
from .models import ItemVenda, Venda


@login_required
def nova_venda(request):
    form = VendaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        produto = form.cleaned_data['produto']
        quantidade = form.cleaned_data['quantidade']

        try:
            with transaction.atomic():
                produto_em_estoque = Produto.objects.select_for_update().get(pk=produto.pk)
                if quantidade > produto_em_estoque.quantidade_estoque:
                    raise ValidationError('Quantidade indisponível no estoque.')

                venda = Venda.objects.create(valor_total=Decimal('0.00'), status='concluida')
                item = ItemVenda.objects.create(
                    venda=venda,
                    produto=produto_em_estoque,
                    quantidade=quantidade,
                    preco_unitario=produto_em_estoque.preco,
                )

                produto_em_estoque.quantidade_estoque -= quantidade
                produto_em_estoque.save(update_fields=['quantidade_estoque'])

                venda.valor_total = item.subtotal
                venda.save(update_fields=['valor_total'])

                messages.success(request, 'Venda registrada com sucesso.')
                return render(
                    request,
                    'vendas/resultado.html',
                    {
                        'venda': venda,
                        'item': item,
                        'produto': produto_em_estoque,
                        'estoque_restante': produto_em_estoque.quantidade_estoque,
                    },
                )
        except ValidationError as exc:
            form.add_error(None, exc)

    return render(request, 'vendas/nova_venda.html', {'form': form})
