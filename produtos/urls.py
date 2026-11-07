from django.urls import path

from . import views

app_name = 'produtos'

urlpatterns = [
    path('', views.lista_produtos, name='lista_produtos'),
    path('novo/', views.cadastrar_produto, name='cadastrar_produto'),
]
