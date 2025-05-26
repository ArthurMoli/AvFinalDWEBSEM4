# properties/views.py
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django import forms
import django_filters

from .models import Imovel
from .forms import ImovelForm  # já criado na opção A

# ---------- FILTRO ----------
class ImovelFilter(django_filters.FilterSet):
    preco__lte = django_filters.NumberFilter(
        field_name="preco",
        lookup_expr="lte",
        label="Preço máx. (R$)",
        widget=forms.NumberInput(attrs={"placeholder": "até quanto?"})
    )

    class Meta:
        model = Imovel
        fields = ["tipo", "quartos", "preco__lte"]


# ---------- LISTA ----------
class ImovelListView(ListView):
    model = Imovel
    template_name = "properties/list.html"
    paginate_by = 6

    def get_queryset(self):
        qs = super().get_queryset().order_by("-data_pub")
        self.filterset = ImovelFilter(self.request.GET, queryset=qs)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["filterset"] = self.filterset
        return ctx


# ---------- DETALHE ----------
class ImovelDetailView(DetailView):
    model = Imovel
    template_name = "properties/detail.html"


# ---------- CRIAÇÃO ----------
class ImovelCreateView(LoginRequiredMixin,
                       PermissionRequiredMixin,
                       CreateView):
    model = Imovel
    form_class = ImovelForm         # ModelForm que exclui 'owner'
    permission_required = "properties.pode_publicar"
    template_name = "properties/form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user     # resolve IntegrityError
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()       # redireciona para /imoveis/<id>/
