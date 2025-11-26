from django.urls import path
from market import views

urlpatterns = [
    path('', views.index, name='index'),

    # ==========================
    #        PRODUTOS
    # ==========================
    path('produto/<int:produto_id>/', views.produto_detalhe, name='produto_detalhe'),

    # ==========================
    #        CARRINHO
    # ==========================
    path('carrinho/', views.carrinho, name='carrinho'),
    path('carrinho/adicionar/<int:produto_id>/', views.adicionar_carrinho, name='adicionar_carrinho'),
    path('carrinho/remover/<int:produto_id>/', views.remover_carrinho, name='remover_carrinho'),

    # ==========================
    #        LOGIN / CONTA
    # ==========================

    # PRIMEIRA TELA DO FLUXO DE CADASTRO
    path('conta/criar-login/', views.criar_login, name='criar_login'),

    # LOGIN NORMAL
    path('conta/login/', views.login_view, name='login'),

    # ETAPAS DO FLUXO
    path('conta/escolher-tipo/', views.escolher_tipo, name='escolher_tipo'),
    path('conta/cadastrar-pessoa/', views.cadastrar_pessoa, name='cadastrar_pessoa'),
    path('conta/cadastrar-endereco/', views.cadastrar_endereco, name='cadastrar_endereco'),
    path('conta/finalizar/', views.finalizar_cadastro, name='finalizar_cadastro'),
    
    path('conta/minha-conta/', views.minha_conta, name='minha_conta'),
    path('conta/sair/', views.logout_view, name='logout'),
]