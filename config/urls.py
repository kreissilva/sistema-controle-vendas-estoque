from django.contrib import admin
from django.urls import include, path

from produtos.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('produtos/', include('produtos.urls')),
    path('vendas/', include('vendas.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
