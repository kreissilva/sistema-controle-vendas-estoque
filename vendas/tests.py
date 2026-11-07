from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from produtos.models import Produto
from vendas.models import ItemVenda, Venda


class VendaModelTestCase(TestCase):
    def setUp(self):
        self.produto = Produto.objects.create(
            nome='Café 500 g',
            categoria='Bebidas',
            preco=Decimal('18.00'),
            quantidade_estoque=10,
            estoque_minimo=8,
        )

    def test_calculo_corretamente_do_subtotal(self):
        item = ItemVenda(produto=self.produto, quantidade=2, preco_unitario=Decimal('18.00'))
        self.assertEqual(item.subtotal, Decimal('36.00'))

    def test_calculo_corretamente_do_total_da_venda(self):
        venda = Venda.objects.create(valor_total=Decimal('36.00'))
        ItemVenda.objects.create(venda=venda, produto=self.produto, quantidade=2, preco_unitario=Decimal('18.00'))

        self.assertEqual(venda.valor_total, Decimal('36.00'))


class VendaIntegrationTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='gerente', password='senha123')
        self.produto = Produto.objects.create(
            nome='Café 500 g',
            categoria='Bebidas',
            preco=Decimal('18.00'),
            quantidade_estoque=10,
            estoque_minimo=8,
        )

    def test_registro_de_venda_e_atualizacao_automatica_do_estoque(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('vendas:nova_venda'),
            {'produto': self.produto.id, 'quantidade': 2},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.quantidade_estoque, 8)
        self.assertContains(response, 'Café 500 g')

    def test_rejeicao_de_venda_com_estoque_insuficiente(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('vendas:nova_venda'),
            {'produto': self.produto.id, 'quantidade': 11},
            follow=True,
        )

        self.assertContains(response, 'estoque')
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.quantidade_estoque, 10)

    def test_transacao_atomica_de_venda(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('vendas:nova_venda'),
            {'produto': self.produto.id, 'quantidade': 15},
            follow=True,
        )

        self.assertContains(response, 'estoque')
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.quantidade_estoque, 10)

    def test_protecao_de_rotas_que_exigem_autenticacao(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_alerta_de_estoque_baixo_aparece_na_resposta(self):
        self.client.force_login(self.user)
        self.produto.quantidade_estoque = 8
        self.produto.estoque_minimo = 8
        self.produto.save()

        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, 'Estoque baixo')
