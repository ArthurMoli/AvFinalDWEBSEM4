from django.db import models

from properties.models import Imovel

# Create your models here.

class ObraStatus(models.Model):
    imovel     = models.ForeignKey(Imovel, on_delete=models.CASCADE,
                                   related_name='obras')
    fase       = models.CharField(max_length=50)   # Fundação, Estrutura…
    porcentagem= models.PositiveSmallIntegerField()
    data       = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.imovel} - {self.porcentagem}%"
