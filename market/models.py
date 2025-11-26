from django.db import models
from django.contrib.auth.models import User


class Endereco(models.Model):
    cep = models.CharField(max_length=9)
    logradouro = models.CharField(max_length=150)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=50, blank=True, null=True)
    bairro = models.CharField(max_length=80)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    pais = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.logradouro}, {self.numero} - {self.cidade}/{self.estado}"


class Cliente(models.Model):
    email = models.EmailField()
    telefone_principal = models.CharField(max_length=15)
    telefone_secundario = models.CharField(max_length=15, blank=True, null=True)

    # ENDEREÇO OPCIONAL
    endereco = models.OneToOneField(
        "Endereco",
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True


class PessoaFisica(Cliente):
    # 🔥 Vincula ao usuário do Django
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="pessoa_fisica",
        null=True
    )

    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=11, unique=True)
    rg = models.CharField(max_length=20, blank=True, null=True)
    data_nascimento = models.DateField()

    def __str__(self):
        return self.nome


class PessoaJuridica(Cliente):
    # 🔥 Vincula ao usuário do Django
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="pessoa_juridica",
        null=True
    )

    razao_social = models.CharField(max_length=150)
    nome_fantasia = models.CharField(max_length=150, blank=True, null=True)
    cnpj = models.CharField(max_length=14, unique=True)
    inscricao_estadual = models.CharField(max_length=20, blank=True, null=True)
    data_abertura = models.DateField()
    site = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.razao_social


class Produto(models.Model):
    nome = models.CharField(max_length=150)
    categoria = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.PositiveIntegerField()
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)

    @property
    def disponivel(self):
        return self.estoque > 0

    def __str__(self):
        return self.nome
