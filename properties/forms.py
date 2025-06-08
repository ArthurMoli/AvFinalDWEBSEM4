from django import forms
from .models import Imovel

class ImovelForm(forms.ModelForm):
    class Meta:
        model = Imovel
        exclude = ("owner",)
        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 4}),
            "preco": forms.NumberInput(attrs={"step": "0.01"}),
            "capa_url": forms.URLInput(attrs={
                "placeholder": "https://exemplo.com/foto-do-imovel.jpg"
            }),
        }
        labels = {
            "titulo": "Título do Imóvel",
            "endereco": "Endereço Completo",
            "preco": "Preço (R$)",
            "tipo": "Tipo de Imóvel",
            "quartos": "Número de Quartos",
            "descricao": "Descrição Detalhada",
            "capa_url": "URL da Imagem",
        }

    def clean_capa_url(self):
        url = self.cleaned_data.get('capa_url')
        if url:
            # Verificações básicas de URL de imagem
            if not any(url.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
                # Se não termina com extensão de imagem, ainda aceita (pode ser serviço como Unsplash)
                pass
            
            # Validação adicional: deve começar com http/https
            if not (url.startswith('http://') or url.startswith('https://')):
                raise forms.ValidationError("A URL deve começar com http:// ou https://")
                
        return url