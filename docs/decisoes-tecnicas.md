# Decisões técnicas

## Stack

- Python 3.12
- Django 5.2.19
- SQLite para desenvolvimento e MVP
- Bootstrap 5.3 para interface

## Estrutura modular

A solução foi organizada em apps: `produtos` e `vendas`, com templates e static separados. Isso facilita manutenção e validação por área funcional.

## Validação de estoque

A regra de negócio foi implementada diretamente no `Produto.clean()` e na operação de venda, com transação atômica. Isso evita que uma venda parcial seja persistida e garante consistência.

## Autenticação

O sistema usa o mecanismo nativo de autenticação do Django. As rotas do dashboard e vendas exigem login, e a redireção ocorre para `/accounts/login/`.

## CI

A integração contínua foi preparada em `.github/workflows/ci.yml` para validar a aplicação em pull requests e push em `main`.

## Limitações conhecidas

- O projeto ainda não foi publicado em um repositório remoto, porque o ambiente atual não possui `gh auth login` realizado.
- As validações com representantes externos ainda não ocorreram; o material foi deixado como roteiro para execução posterior.
