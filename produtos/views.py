from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ProdutoForm
from .models import Produto


@login_required
def dashboard(request):
    produtos = list(Produto.objects.order_by('nome'))
    produtos_baixo = [produto for produto in produtos if produto.estoque_baixo]
    contexto = {
        'total_produtos': len(produtos),
        'produtos_baixo': len(produtos_baixo),
        'produtos': produtos[:5],
        'produtos_alerta': produtos_baixo[:5],
    }
    return render(request, 'dashboard.html', contexto)


@login_required
def lista_produtos(request):
    query = request.GET.get('q', '').strip()
    produtos = Produto.objects.order_by('nome')
    if query:
        produtos = produtos.filter(nome__icontains=query)
    return render(request, 'produtos/lista.html', {'produtos': produtos, 'query': query})


@login_required
def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            produto = form.save()
            messages.success(request, f'Produto {produto.nome} cadastrado com sucesso.')
            return redirect('produtos:lista_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'produtos/form.html', {'form': form})
