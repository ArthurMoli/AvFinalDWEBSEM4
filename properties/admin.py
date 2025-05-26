from django.contrib import admin

# Register your models here.
# properties/admin.py
from django.contrib import admin
from .models import Imovel
@admin.register(Imovel) 
class ImovelAdmin(admin.ModelAdmin): list_display = ('titulo','preco','tipo','quartos','owner')
readonly_fields = ('owner',) 
def save_model(self, request, obj, form, change): 
    if not obj.owner_id: obj.owner = request.user 
    super().save_model(request, obj, form, change)
