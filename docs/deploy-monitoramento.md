# Deploy e monitoramento

## Publicação no Render

O arquivo `render.yaml` descreve um serviço web Django e um banco PostgreSQL. O processo instala as dependências, coleta os arquivos estáticos, executa as migrações na inicialização e inicia o Gunicorn. O Render gera `DJANGO_SECRET_KEY` e fornece `DATABASE_URL`; não coloque esses valores no repositório.

1. Publique o repositório no GitHub e conecte-o ao Render.
2. No Render, crie um Blueprint a partir do repositório e revise os recursos descritos em `render.yaml`.
3. Aguarde o primeiro deploy e abra a URL HTTPS informada pelo Render. O health check `/health/` deve retornar HTTP 200.
4. Crie o usuário administrador pelo Shell do serviço com `python manage.py createsuperuser`.

O plano gratuito do PostgreSQL no Render tem limitações e prazo de expiração conforme as condições atuais do provedor. Ele serve para demonstração; antes de armazenar dados reais, escolha um banco com persistência e backup adequados. O serviço gratuito também pode entrar em suspensão, o que aumenta o tempo de resposta inicial.

## Monitoramento de disponibilidade

O endpoint público `https://<dominio-do-servico>/health/` faz uma consulta `SELECT 1` ao banco e retorna JSON. HTTP 200 com `{"status":"ok"}` indica que a aplicação e o banco respondem; HTTP 503 com `{"status":"unavailable"}` indica falha na verificação. Ele não expõe detalhes internos nem exige autenticação, para permitir a sondagem externa.

Para receber alertas independentes do provedor:

1. Crie uma conta no UptimeRobot e adicione um monitor do tipo HTTP(s).
2. Informe a URL completa `https://<dominio-do-servico>/health/`, configure intervalo de 5 minutos e alertas por e-mail.
3. Considere o serviço indisponível se a sondagem não receber HTTP 200. Investigue os eventos do Render e a conectividade do banco; após a correção, confirme a recuperação pelo próximo monitoramento.

O `healthCheckPath` do Render também valida a instância durante o deploy, enquanto o monitor externo detecta indisponibilidades após a publicação. O monitor UptimeRobot precisa ser criado na conta do responsável pelo serviço; este repositório não contém credenciais nem configuração de alertas externa.

## Verificação local

```bash
python manage.py check
python manage.py test produtos.tests.HealthCheckTestCase
```

Localmente, sem `DATABASE_URL`, a aplicação continua usando SQLite. Em produção, configure `DATABASE_URL` para PostgreSQL.