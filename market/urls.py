from django.urls import path
from market import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cads/', views.cads, name='cads'),
    path('cadastro/cadastro_pessoa_fisica/', views.cadastrar_pessoa_fisica, name='cadastro_pessoa_fisica'),
    path('cadastro/cadastro_pessoa_juridica/', views.cadastrar_pessoa_juridica, name='cadastro_pessoa_juridica'),
    path('produto/<int:produto_id>/', views.produto_detalhe, name='produto_detalhe'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('carrinho/adicionar/<int:produto_id>/', views.adicionar_carrinho, name='adicionar_carrinho'),
    path('carrinho/remover/<int:produto_id>/', views.remover_carrinho, name='remover_carrinho'),

]
