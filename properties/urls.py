from django.urls import path
from .views import ImovelListView, ImovelDetailView, ImovelCreateView
urlpatterns = [
    path("",            ImovelListView.as_view(),   name="imoveis"),
    path("novo/",       ImovelCreateView.as_view(), name="imovel_novo"),
    path("<int:pk>/",   ImovelDetailView.as_view(), name="imovel"),
]
