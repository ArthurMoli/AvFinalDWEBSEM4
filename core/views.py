from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from properties.models import Imovel
from .models import Notificacao
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404


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
            user=self.request.user
        ).order_by("-created_at")
        return ctx
    
@login_required
def marcar_todas_lidas(request):
    Notificacao.objects.filter(user=request.user, lida=False).update(lida=True)
    return redirect("notifications")

@login_required
def marcar_uma_lida(request, pk):
    n = get_object_or_404(Notificacao, pk=pk, user=request.user)
    n.lida = True
    n.save(update_fields=["lida"])
    return redirect("notifications")