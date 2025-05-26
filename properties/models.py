from django.db import models
from django.urls import reverse
class Imovel(models.Model):
    TIPO_CHOICES = [('AP', 'Apartamento'), ('CA', 'Casa')]
    titulo   = models.CharField(max_length=120)
    endereco = models.CharField(max_length=255)
    preco    = models.DecimalField(max_digits=12, decimal_places=2)
    tipo     = models.CharField(max_length=2, choices=TIPO_CHOICES)
    quartos  = models.PositiveSmallIntegerField()
    descricao= models.TextField()
    capa     = models.ImageField(upload_to='imoveis/')
    data_pub = models.DateTimeField(auto_now_add=True)
    owner    = models.ForeignKey('users.User', on_delete=models.CASCADE,
                                 related_name='imoveis')
    def get_absolute_url(self):
        return reverse("imovel", args=[self.pk])
    class Meta:
        permissions = [("pode_publicar", "Pode publicar imóvel")]

    def __str__(self):
        return self.titulo
