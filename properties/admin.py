from django.contrib import admin
from .models import Imovel, Interesse

@admin.register(Imovel) 
class ImovelAdmin(admin.ModelAdmin): 
    list_display = ('titulo','preco','tipo','quartos','owner')
    readonly_fields = ('owner',) 
    
    def save_model(self, request, obj, form, change): 
        if not obj.owner_id: 
            obj.owner = request.user 
        super().save_model(request, obj, form, change)

@admin.register(Interesse)
class InteresseAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'imovel', 'data_interesse')
    list_filter = ('data_interesse', 'imovel__tipo')
    search_fields = ('cliente__username', 'cliente__first_name', 'cliente__last_name', 'imovel__titulo')
    readonly_fields = ('data_interesse',)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('cliente', 'imovel')