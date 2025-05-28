"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin              #  ← Faltava isto
from django.urls import path, include
from core.views import HomeView, NotificacoesView
from core import views as core_views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
urlpatterns = [
    path("admin/",   admin.site.urls),

    # Home pode ser acessada por "/" e "/home/"
    path("",         HomeView.as_view(),       name="home"),
    path("home/",    HomeView.as_view(),       name="home_alias"),

    # Imóveis
    path("imoveis/", include("properties.urls")),

    # Obras
    path("works/",   include(("works.urls", "works"), namespace="works")),

    # Auth (mantém contas/)
    path("accounts/", include("django.contrib.auth.urls")),

    # logout GET-friendly → /logout/

path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("notificacoes/", NotificacoesView.as_view(), name="notifications"),
    path("notificacoes/ler_todas/", core_views.marcar_todas_lidas, name="notifs_ler_todas"),
path("notificacoes/ler/<int:pk>/", core_views.marcar_uma_lida,   name="notifs_ler"),

]