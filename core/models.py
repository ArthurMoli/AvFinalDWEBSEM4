from django.db import models

# Create your models here.

class Notificacao(models.Model):
    usuario   = models.ForeignKey('users.User', on_delete=models.CASCADE)
    mensagem  = models.CharField(max_length=255)
    lida      = models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True)
