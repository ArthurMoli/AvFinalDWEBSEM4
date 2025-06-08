from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from works.models import ObraStatus
from core.models import Notificacao
from .models import Interesse

@receiver(post_save, sender=ObraStatus)
def avisar_clientes_interessados(sender, instance, created, **kwargs):
    """
    Quando uma nova etapa da obra é criada, notifica todos os clientes 
    que demonstraram interesse no imóvel
    """
    if created:
        # Busca todos os clientes interessados neste imóvel
        interessados = Interesse.objects.filter(
            imovel=instance.imovel
        ).select_related('cliente')
        
        # Cria uma notificação para cada cliente interessado
        for interesse in interessados:
            mensagem = (
                f"Obra do imóvel '{instance.imovel.titulo}' foi atualizada: "
                f"{instance.fase} ({instance.porcentagem}%)"
            )
            
            Notificacao.objects.create(
                user=interesse.cliente,
                mensagem=mensagem
            )

@receiver(post_save, sender=Interesse)
def avisar_corretor_novo_interesse(sender, instance, created, **kwargs):
    """
    Quando um cliente demonstra interesse em um imóvel, notifica o corretor
    """
    if created:
        # Pega o nome do cliente (ou username se não tiver nome completo)
        nome_cliente = instance.cliente.get_full_name() or instance.cliente.username
        
        mensagem = (
            f"{nome_cliente} demonstrou interesse no imóvel "
            f"'{instance.imovel.titulo}'"
        )
        
        # Cria notificação para o corretor (owner do imóvel)
        Notificacao.objects.create(
            user=instance.imovel.owner,
            mensagem=mensagem
        )

@receiver(post_delete, sender=Interesse)
def avisar_corretor_interesse_removido(sender, instance, **kwargs):
    """
    Quando um cliente remove interesse em um imóvel, notifica o corretor
    """
    # Pega o nome do cliente
    nome_cliente = instance.cliente.get_full_name() or instance.cliente.username
    
    mensagem = (
        f"{nome_cliente} removeu o interesse no imóvel "
        f"'{instance.imovel.titulo}'"
    )
    
    # Cria notificação para o corretor (owner do imóvel)
    Notificacao.objects.create(
        user=instance.imovel.owner,
        mensagem=mensagem
    )