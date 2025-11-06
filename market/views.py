from django.shortcuts import render, redirect
from .forms import PessoaFisicaForm, PessoaJuridicaForm, EnderecoForm


def index(request):
    return render(request, 'index.html')


def cadastrar_pessoa_fisica(request):
    if request.method == 'POST':
        pessoa_form = PessoaFisicaForm(request.POST)
        endereco_form = EnderecoForm(request.POST)

        if pessoa_form.is_valid() and endereco_form.is_valid():
            endereco = endereco_form.save()
            pessoa = pessoa_form.save(commit=False)
            pessoa.endereco = endereco
            pessoa.save()
            return redirect('index')
    else:
        pessoa_form = PessoaFisicaForm()
        endereco_form = EnderecoForm()

    return render(request, 'cadastro_pessoa_fisica.html', {
        'pessoa_form': pessoa_form,
        'endereco_form': endereco_form,
    })


def cadastrar_pessoa_juridica(request):
    if request.method == 'POST':
        pessoa_form = PessoaJuridicaForm(request.POST)
        endereco_form = EnderecoForm(request.POST)

        if pessoa_form.is_valid() and endereco_form.is_valid():
            endereco = endereco_form.save()
            pessoa = pessoa_form.save(commit=False)
            pessoa.endereco = endereco
            pessoa.save()
            return redirect('index')
    else:
        pessoa_form = PessoaJuridicaForm()
        endereco_form = EnderecoForm()

    return render(request, 'cadastro_pessoa_juridica.html', {
        'pessoa_form': pessoa_form,
        'endereco_form': endereco_form,
    })
