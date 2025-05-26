from django.db.models.signals import post_save
from django.dispatch import receiver
from works.models import ObraStatus
from core.models import Notificacao

@receiver(post_save, sender=ObraStatus)
def avisar_cliente(sender, instance, created, **kwargs):
    if created:
        cliente = instance.imovel.owner
        msg = f"Obra de {instance.imovel.titulo} avançou para {instance.porcentagem}%"
        Notificacao.objects.create(usuario=cliente, mensagem=msg)
