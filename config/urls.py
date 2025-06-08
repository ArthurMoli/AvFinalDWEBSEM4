from django.contrib import admin
from django.urls import path, include
from core.views import HomeView, NotificacoesView
from core import views as core_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Home pode ser acessada por "/" e "/home/"
    path("", HomeView.as_view(), name="home"),
    path("home/", HomeView.as_view(), name="home_alias"),

    # Imóveis
    path("imoveis/", include("properties.urls")),

    # Obras
    path("works/", include(("works.urls", "works"), namespace="works")),

    # Users (cadastro, perfil)
    path("users/", include("users.urls")),

    # Auth (mantém contas/)
    path("accounts/", include("django.contrib.auth.urls")),

    # logout GET-friendly → /logout/
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("notificacoes/", NotificacoesView.as_view(), name="notifications"),
    path("notificacoes/ler_todas/", core_views.marcar_todas_lidas, name="notifs_ler_todas"),
    path("notificacoes/ler/<int:pk>/", core_views.marcar_uma_lida, name="notifs_ler"),
]