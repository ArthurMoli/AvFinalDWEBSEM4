from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from properties.models import Imovel
from .models import ObraStatus          # <-- importe o modelo de status

class MinhasObrasView(LoginRequiredMixin, ListView):
    template_name = "works/minhas.html"
    context_object_name = "imoveis"

    def get_queryset(self):
        return Imovel.objects.filter(owner=self.request.user)


class ObraTimelineView(LoginRequiredMixin, ListView):
    """
    Lista as etapas de construção de um único imóvel
    """
    template_name = "works/timeline.html"
    context_object_name = "etapas"

    def get_queryset(self):
        return (
            ObraStatus.objects
            .filter(imovel_id=self.kwargs["imovel_pk"])
            .order_by("-data")
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["imovel"] = Imovel.objects.get(pk=self.kwargs["imovel_pk"])
        return ctx

from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import ObraStatusForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class ObraAddView(LoginRequiredMixin,
                  PermissionRequiredMixin,
                  CreateView):
    permission_required = "properties.pode_publicar"
    form_class  = ObraStatusForm
    template_name = "works/add.html"
    success_url   = reverse_lazy("works:meus")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user   # <- aqui
        return kwargs