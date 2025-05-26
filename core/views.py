from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from properties.models import Imovel
from .models import Notificacao

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kw):
        ctx = super().get_context_data(**kw)
        ctx["imoveis"] = Imovel.objects.order_by("-data_pub")[:12]
        return ctx

class NotificacoesView(LoginRequiredMixin, TemplateView):
    template_name = "core/notifications.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["notificacoes"] = Notificacao.objects.filter(
            usuario=self.request.user
        ).order_by("-created_at")
        return ctx