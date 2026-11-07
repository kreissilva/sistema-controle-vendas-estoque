from django.urls import path

from . import views

app_name = 'vendas'

urlpatterns = [
    path('', views.nova_venda, name='nova_venda'),
]
