from django.shortcuts import render

# Create your views here.
from django.db.models import Count, Sum
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView
from properties.models import Imovel

class DashboardView(PermissionRequiredMixin, TemplateView):
    permission_required = 'auth.view_user'
    template_name = 'reports/dashboard.html'
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['total_imoveis'] = Imovel.objects.count()
        ctx['total_valor']   = Imovel.objects.aggregate(Sum('preco'))['preco__sum']
        return ctx
