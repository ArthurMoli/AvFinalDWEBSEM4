from django.urls import path
from .views import SignUpView, ProfileUpdateView, profile_view

app_name = 'users'

urlpatterns = [
    path('cadastrar/', SignUpView.as_view(), name='signup'),
    path('perfil/', profile_view, name='profile_view'),
    path('perfil/editar/', ProfileUpdateView.as_view(), name='profile_edit'),
]