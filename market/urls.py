from django.urls import path
from market import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cads/', views.cads, name='cads'),
    path('cadastro/cadastro_pessoa_fisica/', views.cadastrar_pessoa_fisica, name='cadastro_pessoa_fisica'),
    path('cadastro/cadastro_pessoa_juridica/', views.cadastrar_pessoa_juridica, name='cadastro_pessoa_juridica'),
]
