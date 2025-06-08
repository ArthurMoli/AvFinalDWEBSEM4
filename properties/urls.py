from django.urls import path
from .views import (
    ImovelListView, ImovelDetailView, ImovelCreateView,
    ImovelUpdateView, ImovelDeleteView,
    toggle_interesse, meus_interesses, meus_imoveis
)

urlpatterns = [
    path("", ImovelListView.as_view(), name="imoveis"),
    path("novo/", ImovelCreateView.as_view(), name="imovel_novo"),
    path("meus-interesses/", meus_interesses, name="meus_interesses"),
    path("meus-imoveis/", meus_imoveis, name="meus_imoveis"),
    path("<int:pk>/", ImovelDetailView.as_view(), name="imovel"),
    path("<int:pk>/editar/", ImovelUpdateView.as_view(), name="imovel_editar"),
    path("<int:pk>/excluir/", ImovelDeleteView.as_view(), name="imovel_excluir"),
    path("<int:imovel_id>/interesse/", toggle_interesse, name="toggle_interesse"),
]