from django import forms
from .models import Imovel

class ImovelForm(forms.ModelForm):
    class Meta:
        model = Imovel
        exclude = ("owner",)             # ← não exibe o campo owner
        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 4}),
            "preco":     forms.NumberInput(attrs={"step": "0.01"}),
        }
        labels = {
            "titulo": "Título do Imóvel",
            "endereco": "Endereço Completo",
            "preco": "Preço (R$)",
            "tipo": "Tipo de Imóvel",
            "quartos": "Número de Quartos",
            "descricao": "Descrição Detalhada",
            "capa": "Imagem de Capa",
        }