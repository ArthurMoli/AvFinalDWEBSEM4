from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django import forms
import django_filters
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied

from .models import Imovel, Interesse
from .forms import ImovelForm

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
        
        # Otimização: pré-carrega dados relacionados se usuário é cliente
        if (self.request.user.is_authenticated and 
            self.request.user.perfil == 'CL'):
            qs = qs.prefetch_related('interessados')
        
        self.filterset = ImovelFilter(self.request.GET, queryset=qs)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["filterset"] = self.filterset
        
        # Adiciona informação sobre interesses do usuário para otimizar template
        if (self.request.user.is_authenticated and 
            self.request.user.perfil == 'CL'):
            # IDs dos imóveis que o usuário tem interesse
            ctx["meus_interesses_ids"] = list(
                self.request.user.interesses.values_list('imovel_id', flat=True)
            )
        
        return ctx


# ---------- DETALHE ----------
class ImovelDetailView(DetailView):
    model = Imovel
    template_name = "properties/detail.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Verifica se o usuário logado tem interesse neste imóvel
        if self.request.user.is_authenticated:
            context['tem_interesse'] = Interesse.objects.filter(
                cliente=self.request.user,
                imovel=self.object
            ).exists()
        else:
            context['tem_interesse'] = False
            
        return context


# ---------- CRIAÇÃO ----------
class ImovelCreateView(LoginRequiredMixin,
                       PermissionRequiredMixin,
                       CreateView):
    model = Imovel
    form_class = ImovelForm
    permission_required = "properties.pode_publicar"
    template_name = "properties/form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, f'Imóvel "{form.instance.titulo}" criado com sucesso!')
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()


# ---------- EDIÇÃO ----------
class ImovelUpdateView(LoginRequiredMixin,
                       PermissionRequiredMixin,
                       UpdateView):
    model = Imovel
    form_class = ImovelForm
    permission_required = "properties.pode_publicar"
    template_name = "properties/form.html"

    def get_object(self):
        obj = super().get_object()
        # Apenas o dono pode editar
        if obj.owner != self.request.user:
            raise PermissionDenied("Você só pode editar seus próprios imóveis.")
        return obj

    def form_valid(self, form):
        messages.success(self.request, f'Imóvel "{form.instance.titulo}" atualizado com sucesso!')
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context


# ---------- EXCLUSÃO ----------
class ImovelDeleteView(LoginRequiredMixin,
                       PermissionRequiredMixin,
                       DeleteView):
    model = Imovel
    permission_required = "properties.pode_publicar"
    template_name = "properties/delete.html"
    success_url = reverse_lazy("imoveis")

    def get_object(self):
        obj = super().get_object()
        # Apenas o dono pode deletar
        if obj.owner != self.request.user:
            raise PermissionDenied("Você só pode deletar seus próprios imóveis.")
        return obj

    def form_valid(self, form):
        titulo = self.object.titulo
        messages.success(self.request, f'Imóvel "{titulo}" excluído com sucesso!')
        return super().form_valid(form)


# ---------- INTERESSE ----------
@login_required
def toggle_interesse(request, imovel_id):
    """
    Adiciona ou remove interesse do cliente em um imóvel
    """
    if request.method != 'POST':
        return redirect('imoveis')
    
    imovel = get_object_or_404(Imovel, pk=imovel_id)
    
    # Verifica se já existe interesse
    interesse, created = Interesse.objects.get_or_create(
        cliente=request.user,
        imovel=imovel
    )
    
    if not created:
        # Se já existia, remove o interesse
        interesse.delete()
        messages.success(request, f'Interesse removido de "{imovel.titulo}"')
        interessado = False
    else:
        # Se não existia, acabou de criar
        messages.success(request, f'Interesse adicionado em "{imovel.titulo}"')
        interessado = True
    
    # Se for requisição AJAX, retorna JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'interessado': interessado})
    
    return redirect('imovel', pk=imovel_id)

@login_required 
def meus_interesses(request):
    """
    Lista todos os imóveis que o cliente tem interesse
    """
    interesses = Interesse.objects.filter(
        cliente=request.user
    ).select_related('imovel').order_by('-data_interesse')
    
    return render(request, 'properties/meus_interesses.html', {
        'interesses': interesses
    })

@login_required
def meus_imoveis(request):
    """
    Lista todos os imóveis do usuário logado
    """
    imoveis = Imovel.objects.filter(
        owner=request.user
    ).order_by('-data_pub')
    
    return render(request, 'properties/meus_imoveis.html', {
        'imoveis': imoveis
    })