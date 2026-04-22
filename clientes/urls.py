from django.urls import path
from . import views

urlpatterns = [
    path('clientes/', views.ListaClientesView.as_view(), name='lista-clientes'),
    path('clientes/novo/', views.CriarClienteView.as_view(), name='novo-cliente'),
    path('clientes/<int:pk>/', views.DetalhesClienteView.as_view(), name='detalhes-cliente'),
    path('clientes/<int:pk>/editar/', views.EditarClienteView.as_view(), name='editar-cliente'),
    path('clientes/<int:pk>/servicos/novo/', views.CriarServicoView.as_view(), name='novo-servico'),
]