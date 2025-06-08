from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, ProfileUpdateForm
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpView(CreateView):
    """
    View para cadastro de novos usuários
    """
    model = User
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        # Salva o usuário
        response = super().form_valid(form)
        
        # Faz login automático após cadastro
        login(self.request, self.object)
        
        # Mensagem de boas-vindas
        perfil_nome = "Corretor" if self.object.perfil == 'CO' else "Cliente"
        messages.success(
            self.request, 
            f'Bem-vindo(a), {self.object.first_name}! '
            f'Sua conta de {perfil_nome} foi criada com sucesso.'
        )
        
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Criar Conta'
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    View para atualizar perfil do usuário
    """
    model = User
    form_class = ProfileUpdateForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Perfil atualizado com sucesso!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Meu Perfil'
        return context


@login_required
def profile_view(request):
    """
    View simples para exibir perfil
    """
    return render(request, 'users/profile_view.html', {
        'user': request.user,
        'title': 'Meu Perfil'
    })