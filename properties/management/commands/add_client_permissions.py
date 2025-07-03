from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from users.models import User
from properties.models import Imovel


class Command(BaseCommand):
    help = 'Adiciona permissão "pode_publicar" para todos os clientes'

    def handle(self, *args, **options):
        # Obter o content type do modelo Imovel
        content_type = ContentType.objects.get_for_model(Imovel)
        
        # Obter ou criar a permissão 'pode_publicar'
        permission, created = Permission.objects.get_or_create(
            codename='pode_publicar',
            name='Pode publicar imóvel',
            content_type=content_type,
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Permissão "{permission.name}" criada com sucesso!')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Permissão "{permission.name}" já existe.')
            )
        
        # Adicionar a permissão para todos os clientes
        clientes = User.objects.filter(perfil='CL')
        count = 0
        
        for cliente in clientes:
            if not cliente.user_permissions.filter(id=permission.id).exists():
                cliente.user_permissions.add(permission)
                count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Permissão adicionada para {cliente.get_full_name()}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Permissão adicionada para {count} clientes.')
        )