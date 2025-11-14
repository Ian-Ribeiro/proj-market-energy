from django.shortcuts import render, redirect
from .forms import PessoaFisicaForm, PessoaJuridicaForm, EnderecoForm, ProdutoForm
from .models import Produto


def index(request):
    categoria = request.GET.get('categoria')
    categorias = Produto.objects.values_list('categoria', flat=True).distinct()

    if categoria:
        produtos = Produto.objects.filter(categoria=categoria)
    else:
        produtos = Produto.objects.all()

    return render(request, 'index.html', {
        'produtos': produtos,
        'categorias': categorias,
        'categoria_selecionada': categoria
    })

def cads(request):
    return render(request, 'cads.html')


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

    return render(request, 'cadastro/cadastro_pessoa_fisica.html', {
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

    return render(request, 'cadastro/cadastro_pessoa_juridica.html', {
        'pessoa_form': pessoa_form,
        'endereco_form': endereco_form,
    })
