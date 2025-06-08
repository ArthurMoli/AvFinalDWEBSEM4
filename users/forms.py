from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """
    Formulário customizado para criação de usuários
    """
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="Nome",
        widget=forms.TextInput(attrs={
            'class': 'field',
            'placeholder': 'Seu nome'
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label="Sobrenome",
        widget=forms.TextInput(attrs={
            'class': 'field',
            'placeholder': 'Seu sobrenome'
        })
    )
    
    email = forms.EmailField(
        required=True,
        label="E-mail",
        widget=forms.EmailInput(attrs={
            'class': 'field',
            'placeholder': 'seu@email.com'
        })
    )
    
    telefone = forms.CharField(
        max_length=20,
        required=False,
        label="Telefone (opcional)",
        widget=forms.TextInput(attrs={
            'class': 'field',
            'placeholder': '(11) 99999-9999'
        })
    )
    
    perfil = forms.ChoiceField(
        choices=User.PERFIL_CHOICES,
        required=True,
        label="Tipo de Conta",
        widget=forms.RadioSelect(attrs={
            'class': 'perfil-radio'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'telefone', 'perfil', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customizar widgets dos campos herdados
        self.fields['username'].widget.attrs.update({
            'class': 'field',
            'placeholder': 'Escolha um nome de usuário'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'field',
            'placeholder': 'Crie uma senha segura'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'field',
            'placeholder': 'Confirme sua senha'
        })
        
        # Labels customizados
        self.fields['username'].label = "Nome de Usuário"
        self.fields['password1'].label = "Senha"
        self.fields['password2'].label = "Confirmar Senha"

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este e-mail já está em uso.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.telefone = self.cleaned_data['telefone']
        user.perfil = self.cleaned_data['perfil']
        
        if commit:
            user.save()
            
            # Se for corretor, dar permissão automaticamente
            if user.perfil == 'CO':
                from django.contrib.auth.models import Permission
                permission = Permission.objects.get(codename='pode_publicar')
                user.user_permissions.add(permission)
                
        return user


class ProfileUpdateForm(forms.ModelForm):
    """
    Formulário para atualizar perfil do usuário
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'telefone')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'field'}),
            'last_name': forms.TextInput(attrs={'class': 'field'}),
            'email': forms.EmailInput(attrs={'class': 'field'}),
            'telefone': forms.TextInput(attrs={'class': 'field'}),
        }
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
            'telefone': 'Telefone',
        }