from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PessoaFisica, PessoaJuridica, Endereco, Produto


# ---------------------------------------------------------
#   ETAPA 1 — Criar Conta (User)
# ---------------------------------------------------------

class CriarContaForm(UserCreationForm):
    email = forms.EmailField(label="E-mail")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# ---------------------------------------------------------
#   ETAPA 2 — Escolher Tipo
# ---------------------------------------------------------

class EscolherTipoForm(forms.Form):
    TIPO_CHOICES = [
        ('pf', 'Pessoa Física'),
        ('pj', 'Pessoa Jurídica'),
    ]

    tipo = forms.ChoiceField(
        choices=TIPO_CHOICES,
        widget=forms.RadioSelect,
        label="Escolha o tipo de cadastro"
    )


# ---------------------------------------------------------
#   ETAPA 3 — Cadastro Pessoa Física (sem email, sem endereço)
# ---------------------------------------------------------

class PessoaFisicaForm(forms.ModelForm):
    class Meta:
        model = PessoaFisica
        fields = [
            'nome',
            'cpf',
            'rg',
            'data_nascimento',
            'telefone_principal',
            'telefone_secundario',
        ]


# ---------------------------------------------------------
#   ETAPA 3 — Cadastro Pessoa Jurídica (sem email, sem endereço)
# ---------------------------------------------------------

class PessoaJuridicaForm(forms.ModelForm):
    class Meta:
        model = PessoaJuridica
        fields = [
            'razao_social',
            'nome_fantasia',
            'cnpj',
            'inscricao_estadual',
            'data_abertura',
            'telefone_principal',
            'telefone_secundario',
            'site',
        ]


# ---------------------------------------------------------
#   ETAPA 4 — Cadastro Endereço (Opcional)
# ---------------------------------------------------------

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = '__all__'


# ---------------------------------------------------------
#   PRODUTO (mantém igual)
# ---------------------------------------------------------

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = '__all__'
