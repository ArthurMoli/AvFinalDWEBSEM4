from django.db import models
from django.urls import reverse

class Imovel(models.Model):
    TIPO_CHOICES = [('AP', 'Apartamento'), ('CA', 'Casa')]
    STATUS_CHOICES = [('PR', 'Pronto'), ('EO', 'Em Obra')]
    titulo   = models.CharField(max_length=120)
    endereco = models.CharField(max_length=255)
    preco    = models.DecimalField(max_digits=12, decimal_places=2)
    tipo     = models.CharField(max_length=2, choices=TIPO_CHOICES)
    status   = models.CharField(max_length=2, choices=STATUS_CHOICES, default='PR')
    quartos  = models.PositiveSmallIntegerField()
    descricao= models.TextField()
    capa_url = models.URLField(
        verbose_name="URL da Imagem", 
        help_text="Cole aqui a URL da imagem do imóvel (ex: https://exemplo.com/foto.jpg)",
        default="https://via.placeholder.com/800x600/4f46e5/ffffff?text=Imóvel"
    )
    data_pub = models.DateTimeField(auto_now_add=True)
    owner    = models.ForeignKey('users.User', on_delete=models.CASCADE,
                                 related_name='imoveis')
    def get_absolute_url(self):
        return reverse("imovel", args=[self.pk])
    
    class Meta:
        permissions = [("pode_publicar", "Pode publicar imóvel")]

    def __str__(self):
        return self.titulo


class Interesse(models.Model):
    """
    Relaciona um cliente (User) com um imóvel de interesse
    """
    cliente = models.ForeignKey('users.User', on_delete=models.CASCADE, 
                               related_name='interesses')
    imovel = models.ForeignKey(Imovel, on_delete=models.CASCADE, 
                              related_name='interessados')
    data_interesse = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('cliente', 'imovel')
        verbose_name = "Interesse"
        verbose_name_plural = "Interesses"
    
    def __str__(self):
        return f"{self.cliente.get_full_name()} interessado em {self.imovel.titulo}"