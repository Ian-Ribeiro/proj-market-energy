from django.shortcuts import render, redirect, get_object_or_404
from .forms import PessoaFisicaForm, PessoaJuridicaForm, EnderecoForm
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


def produto_detalhe(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    return render(request, 'produto_detalhe.html', {'produto': produto})


# ----------------------------
#        CARRINHO
# ----------------------------

def adicionar_carrinho(request, produto_id):
    carrinho = request.session.get('carrinho', {})

    produto_id = str(produto_id)  # 🔥 manter tudo como string

    carrinho[produto_id] = carrinho.get(produto_id, 0) + 1

    request.session['carrinho'] = carrinho
    return redirect('carrinho')


def remover_carrinho(request, produto_id):
    carrinho = request.session.get('carrinho', {})

    produto_id = str(produto_id)

    if produto_id in carrinho:
        del carrinho[produto_id]

    request.session['carrinho'] = carrinho
    return redirect('carrinho')


def carrinho(request):
    carrinho_session = request.session.get('carrinho', {})
    produtos = []
    total = 0

    for product_id, quantidade in carrinho_session.items():
        produto = get_object_or_404(Produto, id=int(product_id))
        subtotal = quantidade * produto.preco
        total += subtotal

        produtos.append({
            "produto": produto,
            "quantidade": quantidade,
            "subtotal": subtotal
        })

    return render(request, 'carrinho.html', {
        'produtos': produtos,
        'total': total
    })
