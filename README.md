# Sistema de Controle de Vendas e Estoque

## Descrição

Sistema web para pequenos comércios controlar produtos, registrar vendas, atualizar estoque automaticamente e identificar itens com estoque baixo.

## Problema e objetivo do MVP

Pequenos comerciantes costumam depender de registros manuais e dispersos, o que gera inconsistência no estoque e dificuldades na reposição. Este MVP busca centralizar o controle com uma interface simples, responsiva e segura, usando Django 5.2, Bootstrap 5 e SQLite.

## Público-alvo

Proprietários, gerentes e responsáveis por pequenos estabelecimentos comerciais de Camaçari–BA.

## Funcionalidades implementadas

- Cadastro de produtos com nome, categoria, preço, quantidade em estoque e estoque mínimo
- Validação de preço positivo e quantidade positiva
- Consulta de produtos com filtro por nome
- Identificação automática de estoque baixo
- Registro de venda com cálculo do subtotal e total
- Atualização atômica do estoque após confirmação da venda
- Proteção por autenticação do Django
- Dashboard inicial com resumo e alertas

## Tecnologias

- Python 3.12
- Django 5.2 LTS
- SQLite
- HTML5
- CSS3
- Bootstrap 5.3

## Arquitetura

A aplicação segue o padrão MVT do Django em camadas:

- Apresentação: templates HTML com Bootstrap
- Regras de negócio: views, formulários e validações em apps
- Persistência: models e SQLite

## Estrutura do projeto

```text
sistema-controle-vendas-estoque/
├── .github/
│   └── workflows/
│       └── ci.yml
├── config/
├── docs/
├── produtos/
├── static/
│   └── css/
├── templates/
│   ├── produtos/
│   ├── registration/
│   └── vendas/
├── vendas/
├── .env.example
├── .gitignore
├── manage.py
├── README.md
├── requirements.txt
├── db.sqlite3
└── .venv/
```

## Instalação

1. Clone o projeto.
2. Crie um ambiente virtual com Python 3.12.
3. Ative o ambiente e instale as dependências:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

4. Copie o arquivo de exemplo do ambiente:

```bash
cp .env.example .env
```

5. Prepare o banco de dados:

```bash
python manage.py migrate
```

## Execução

```bash
python manage.py runserver
```

Acesse:

- http://127.0.0.1:8000/
- Login padrão do Django em /accounts/login/

## Testes

```bash
python manage.py test
```

## Versionamento

- Branch principal: `main`
- O desenvolvimento foi realizado em branch(es) de funcionalidade e, no ambiente local, a estrutura foi preparada para revisão e merge posterior.
- O repositório remoto não foi publicado porque o GitHub CLI não está autenticado nesta sessão (`gh auth status` retornou não autenticado).

## Pull Request e revisão

1. Crie uma branch de desenvolvimento.
2. Faça commits semânticos.
3. Execute os testes.
4. Abra um pull request para `main`.
5. Revise mudanças e integre após validação das verificações.

## Integração contínua

O workflow em `.github/workflows/ci.yml` executa:

- instalação do Python 3.12
- instalação das dependências
- `manage.py check`
- `manage.py migrate`
- `manage.py test`

## Limitações e melhorias futuras

- MVP focado em pequenos negócios e estoque simples
- Sem módulo de usuários com permissões finas além do login nativo do Django
- Sem relatórios avançados de faturamento e histórico de vendas por período
- Possível expansão para integrações e exportação de dados em CSV

## Validação com a comunidade

A documentação de validação do projeto está em `docs/validacao-comunidade.md` e foi preparada com roteiro, critérios e checklist, sem inventar participantes ou resultados reais de teste.

## Publicação final

O código está pronto para publicação em um repositório público no GitHub, mas a etapa final depende de autenticação e autorização do usuário para criar o repositório e configurar o remote.
