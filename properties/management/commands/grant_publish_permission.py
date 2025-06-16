from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

User = get_user_model()

class Command(BaseCommand):
    help = 'Concede permissão de publicar imóveis para todos os usuários existentes'

    def handle(self, *args, **options):
        # Obtém a permissão
        permission = Permission.objects.get(codename='pode_publicar')
        
        # Obtém todos os usuários
        users = User.objects.all()
        
        # Contador de usuários atualizados
        updated_count = 0
        
        for user in users:
            if not user.has_perm('properties.pode_publicar'):
                user.user_permissions.add(permission)
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Permissão concedida para: {user.username}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nTotal de usuários atualizados: {updated_count}'
            )
        )