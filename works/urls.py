from django.urls import path
from .views import MinhasObrasView, ObraAddView, ObraTimelineView

app_name = "works"
urlpatterns = [
    path("", MinhasObrasView.as_view(), name="meus"),          # <-- name="meus"
    path("<int:imovel_pk>/", ObraTimelineView.as_view(), name="timeline"),
    path("adicionar/", ObraAddView.as_view(), name="add"),

]