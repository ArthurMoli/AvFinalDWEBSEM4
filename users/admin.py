from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User     # seu modelo customizado

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # adiciona seus novos campos no formulário de edição
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Informações adicionais", {
            "fields": ("perfil", "telefone", "avatar"),
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Informações adicionais", {
            "fields": ("perfil",),
        }),
    )

    list_display = (
        "username", "email", "first_name", "last_name",
        "perfil", "is_staff"
    )
