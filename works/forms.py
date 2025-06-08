from django import forms
from .models import ObraStatus
from properties.models import Imovel
from django.db import models

class ObraStatusForm(forms.ModelForm):
    imovel = forms.ModelChoiceField(
        queryset=Imovel.objects.none(),
        empty_label="— selecione —",
        label="Imóvel",
    )

    class Meta:
        model  = ObraStatus
        fields = ["imovel", "fase", "porcentagem"]
        widgets = {
            'porcentagem': forms.NumberInput(attrs={
                'min': '0', 
                'max': '100',
                'placeholder': 'Ex: 25'
            })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        # mostra imóveis onde o corretor é owner
        self.fields["imovel"].queryset = Imovel.objects.filter(owner=user)

    def label_from_instance(self, obj):
        # exibe "Título – R$ preço"
        return f"{obj.titulo} – R$ {obj.preco:,.0f}"

    def clean(self):
        cleaned_data = super().clean()
        imovel = cleaned_data.get('imovel')
        porcentagem = cleaned_data.get('porcentagem')

        if imovel and porcentagem is not None:
            # Buscar a maior porcentagem já registrada para este imóvel
            maior_porcentagem = ObraStatus.objects.filter(
                imovel=imovel
            ).aggregate(
                max_pct=models.Max('porcentagem')
            )['max_pct']

            if maior_porcentagem is not None and porcentagem < maior_porcentagem:
                raise forms.ValidationError(
                    f"A porcentagem não pode ser menor que {maior_porcentagem}%. "
                    f"A obra só pode avançar, não retroceder!"
                )

            # Validação extra: não permitir mais de 100%
            if porcentagem > 100:
                raise forms.ValidationError(
                    "A porcentagem não pode ser maior que 100%."
                )

        return cleaned_data