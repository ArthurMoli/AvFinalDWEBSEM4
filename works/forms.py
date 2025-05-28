# works/forms.py
from django import forms
from .models import ObraStatus, Imovel

class ObraStatusForm(forms.ModelForm):
    imovel = forms.ModelChoiceField(
        queryset=Imovel.objects.none(),
        empty_label="— selecione —",
        label="Imóvel",
    )

    class Meta:
        model  = ObraStatus
        fields = ["imovel", "fase", "porcentagem"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")          # passado pela view
        super().__init__(*args, **kwargs)

        # mostra imóveis onde o corretor é owner
        self.fields["imovel"].queryset = Imovel.objects.filter(owner=user)

    def label_from_instance(self, obj):
        # exibe “Título – R$ preço”
        return f"{obj.titulo} – R$ {obj.preco:,.0f}"
