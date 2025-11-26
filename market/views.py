from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import (
    EscolherTipoForm,
    PessoaFisicaForm,
    PessoaJuridicaForm,
    EnderecoForm
)

from .models import Produto, PessoaFisica, PessoaJuridica, Endereco


# ======================================================================
#                           ÁREA PÚBLICA
# ======================================================================

def index(request):
    categoria = request.GET.get('categoria')
    categorias = Produto.objects.values_list('categoria', flat=True).distinct()
    produtos = Produto.objects.filter(categoria=categoria) if categoria else Produto.objects.all()

    return render(request, 'index.html', {
        'produtos': produtos,
        'categorias': categorias,
        'categoria_selecionada': categoria
    })


def cads(request):
    # se você usa essa view em algum lugar, deixei de volta
    return render(request, 'cads.html')


def produto_detalhe(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    return render(request, 'produto_detalhe.html', {'produto': produto})


# ======================================================================
#                    FLUXO DE CADASTRO — SEQUÊNCIA CORRETA
# ======================================================================

# ETAPA 1 — Criar login (primeira página do fluxo)
def criar_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar = request.POST.get('confirmar')

        # Validações básicas
        if not email or not senha or not confirmar:
            messages.error(request, "Preencha todos os campos.")
            return render(request, 'conta/criar_login.html')

        if senha != confirmar:
            messages.error(request, "As senhas não coincidem.")
            return render(request, 'conta/criar_login.html')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Já existe uma conta com este email.")
            return render(request, 'conta/criar_login.html')

        # Criar usuário e guardar id na sessão
        user = User.objects.create_user(username=email, email=email, password=senha)
        request.session['user_id_temp'] = user.id

        return redirect('escolher_tipo')

    return render(request, 'conta/criar_login.html')


# ETAPA 2 — Escolher tipo de pessoa
def escolher_tipo(request):
    if 'user_id_temp' not in request.session:
        return redirect('criar_login')

    if request.method == 'POST':
        form = EscolherTipoForm(request.POST)
        if form.is_valid():
            request.session['tipo_cliente'] = form.cleaned_data['tipo']
            return redirect('cadastrar_pessoa')
    else:
        form = EscolherTipoForm()

    return render(request, 'conta/escolher_tipo.html', {'form': form})


# ETAPA 3 — Cadastrar PF ou PJ
import logging
from django.db import IntegrityError

logger = logging.getLogger(__name__)

def cadastrar_pessoa(request):
    # 1) checar sessão
    user_id = request.session.get('user_id_temp')
    tipo = request.session.get('tipo_cliente')

    if not user_id or not tipo:
        messages.error(request, "Sessão perdida: inicie o cadastro novamente.")
        return redirect('criar_login')

    # 2) pegar user
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "Usuário não encontrado. Refaça o cadastro.")
        return redirect('criar_login')

    FormClass = PessoaFisicaForm if tipo == 'pf' else PessoaJuridicaForm

    if request.method == 'POST':
        form = FormClass(request.POST)
        # DEBUG: logar dados e validação
        logger.debug("POST em cadastrar_pessoa: user_id=%s tipo=%s", user_id, tipo)
        logger.debug("POST data: %s", request.POST)

        if form.is_valid():
            try:
                pessoa = form.save(commit=False)
                pessoa.user = user
                pessoa.email = user.email
                # endereço opcional
                pessoa.endereco = None
                pessoa.save()

                # garantir sessão marcada
                request.session['pessoa_id_temp'] = int(pessoa.id)
                request.session.modified = True

                messages.success(request, "Dados salvos com sucesso.")
                return redirect('cadastrar_endereco')   # nome da rota
            except IntegrityError as e:
                logger.exception("IntegrityError ao salvar pessoa: %s", e)
                messages.error(request, "Erro ao salvar os dados (integridade). Verifique os campos.")
            except Exception as e:
                logger.exception("Erro inesperado ao salvar pessoa: %s", e)
                messages.error(request, "Erro inesperado ao salvar os dados.")
        else:
            # mostrar erros do form para o usuário
            logger.debug("Form inválido: %s", form.errors.as_json())
            # adiciona mensagens de erro detalhadas
            for field, errs in form.errors.items():
                for err in errs:
                    messages.error(request, f"{field}: {err}")
    else:
        form = FormClass()

    return render(request, 'conta/cadastrar_pessoa.html', {'form': form})



# ETAPA 4 — Cadastrar endereço (opcional) — botão "pular" cria opção
def cadastrar_endereco(request):
    pessoa_id = request.session.get('pessoa_id_temp')
    if not pessoa_id:
        return redirect('criar_conta')

    pessoa = PessoaFisica.objects.filter(id=pessoa_id).first() \
             or PessoaJuridica.objects.get(id=pessoa_id)

    # ======= BOTÃO PULAR =======
    if request.method == "POST" and "pular" in request.POST:
        return redirect('finalizar_cadastro')

    # ======= SALVAR ENDEREÇO =======
    if request.method == 'POST':
        form = EnderecoForm(request.POST)
        if form.is_valid():
            endereco = form.save()
            pessoa.endereco = endereco
            pessoa.save()
            return redirect('finalizar_cadastro')
    else:
        form = EnderecoForm()

    return render(request, 'conta/cadastrar_endereco.html', {'form': form})


# ETAPA FINAL — limpa sessão e mostra página final (ou redireciona para login)
def finalizar_cadastro(request):
    # limpa variáveis temporárias
    for key in ['user_id_temp', 'tipo_cliente', 'pessoa_id_temp']:
        request.session.pop(key, None)

    # renderiza uma página informando que cadastro terminou
    return render(request, 'conta/finalizar_cadastro.html')


# ======================================================================
#                               LOGIN
# ======================================================================

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        user = authenticate(request, username=email, password=senha)

        if user:
            login(request, user)
            return redirect('index')

        messages.error(request, "E-mail ou senha incorretos.")

    return render(request, 'conta/login.html')


# ======================================================================
#                               CARRINHO
# ======================================================================

def adicionar_carrinho(request, produto_id):
    carrinho = request.session.get('carrinho', {})
    pid = str(produto_id)
    carrinho[pid] = carrinho.get(pid, 0) + 1
    request.session['carrinho'] = carrinho
    return redirect('carrinho')


def remover_carrinho(request, produto_id):
    carrinho = request.session.get('carrinho', {})
    pid = str(produto_id)
    if pid in carrinho:
        del carrinho[pid]
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
    
@login_required
def minha_conta(request):
    user = request.user

    # tenta achar Pessoa Física
    pessoa = PessoaFisica.objects.filter(user=user).first()

    # se não achar, tenta PJ
    if not pessoa:
        pessoa = PessoaJuridica.objects.filter(user=user).first()

    return render(request, 'conta/minha_conta.html', {
        'user': user,
        'pessoa': pessoa
    })
    
def logout_view(request):
    logout(request)
    return redirect('login')