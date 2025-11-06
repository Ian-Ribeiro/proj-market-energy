from django.urls import path
from market import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastrar/pessoa-fisica/', views.cadastrar_pessoa_fisica, name='cadastrar_pessoa_fisica'),
    path('cadastrar/pessoa-juridica/', views.cadastrar_pessoa_juridica, name='cadastrar_pessoa_juridica'),
]
