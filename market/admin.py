from django.contrib import admin
from .models import Produto,PessoaFisica,PessoaJuridica,Endereco

# Register your models here.


admin.site.register(Produto)
admin.site.register(PessoaFisica)
admin.site.register(PessoaJuridica)
admin.site.register(Endereco)