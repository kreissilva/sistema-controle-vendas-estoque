from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import OperationalError
from django.test import TestCase
from django.urls import reverse

from produtos.models import Produto


class HealthCheckTestCase(TestCase):
    def test_retorna_ok_quando_banco_esta_disponivel(self):
        response = self.client.get(reverse('health_check'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok'})

    @patch('config.views.connection.cursor', side_effect=OperationalError)
    def test_retorna_indisponivel_quando_banco_falha(self, mock_cursor):
        response = self.client.get(reverse('health_check'))

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), {'status': 'unavailable'})


class ProdutoModelTestCase(TestCase):
    def test_cadastro_valido_de_produto(self):
        produto = Produto.objects.create(
            nome='Café 500 g',
            categoria='Bebidas',
            preco=Decimal('18.00'),
            quantidade_estoque=10,
            estoque_minimo=8,
        )

        self.assertEqual(produto.nome, 'Café 500 g')
        self.assertEqual(produto.quantidade_estoque, 10)
        self.assertTrue(produto.pk)

    def test_rejeicao_de_preco_invalido(self):
        produto = Produto(
            nome='Produto inválido',
            categoria='Geral',
            preco=Decimal('0.00'),
            quantidade_estoque=5,
            estoque_minimo=2,
        )

        with self.assertRaises(ValidationError):
            produto.full_clean()

    def test_rejeicao_de_quantidade_negativa(self):
        produto = Produto(
            nome='Produto negativo',
            categoria='Geral',
            preco=Decimal('10.00'),
            quantidade_estoque=-1,
            estoque_minimo=1,
        )

        with self.assertRaises(ValidationError):
            produto.full_clean()

    def test_identificacao_de_estoque_baixo(self):
        produto = Produto(
            nome='Leite',
            categoria='Laticínios',
            preco=Decimal('8.50'),
            quantidade_estoque=3,
            estoque_minimo=8,
        )

        self.assertTrue(produto.estoque_baixo)


class ProdutoIntegrationTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='vendedor', password='senha123')
        self.produto = Produto.objects.create(
            nome='Arroz 5kg',
            categoria='Alimentos',
            preco=Decimal('25.00'),
            quantidade_estoque=12,
            estoque_minimo=5,
        )
        self.client.force_login(self.user)

    def test_cadastro_e_consulta_de_produtos(self):
        response = self.client.get('/produtos/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Arroz 5kg')

