from django import forms
from .models import ObraStatus, Imovel

class ObraStatusForm(forms.ModelForm):
    class Meta:
        model = ObraStatus
        fields = ["imovel", "fase", "porcentagem"]
    def __init__(self, *a, **kw):
        user = kw.pop("user")
        super().__init__(*a, **kw)
        # mostra só imóveis do corretor
        self.fields["imovel"].queryset = Imovel.objects.filter(owner=user)
