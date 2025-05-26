from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    CLIENTE = 'CL'
    CORRETOR = 'CO'
    PERFIL_CHOICES = [(CLIENTE, 'Cliente'), (CORRETOR, 'Corretor')]
    perfil = models.CharField(max_length=2, choices=PERFIL_CHOICES)
    telefone = models.CharField(max_length=20, blank=True)
    avatar   = models.ImageField(upload_to='avatars/', blank=True)

    def __str__(self):
        return self.get_full_name()
