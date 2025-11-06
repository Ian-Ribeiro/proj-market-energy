from django import forms
from .models import PessoaFisica, PessoaJuridica, Endereco


class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = '__all__'


class PessoaFisicaForm(forms.ModelForm):
    class Meta:
        model = PessoaFisica
        fields = [
            'nome', 'cpf', 'rg', 'data_nascimento',
            'email', 'telefone_principal', 'telefone_secundario', 'site',
        ]


class PessoaJuridicaForm(forms.ModelForm):
    class Meta:
        model = PessoaJuridica
        fields = [
            'razao_social', 'nome_fantasia', 'cnpj', 'inscricao_estadual', 'data_abertura',
            'email', 'telefone_principal', 'telefone_secundario', 'site',
        ]
