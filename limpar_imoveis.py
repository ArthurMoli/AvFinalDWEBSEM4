#!/usr/bin/env python3
import os
import django

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from properties.models import Imovel, Interesse
from works.models import ObraStatus

# Conta quantos registros existem antes
total_imoveis = Imovel.objects.count()
total_interesses = Interesse.objects.count()
total_obras = ObraStatus.objects.count()

print(f"📊 Registros encontrados:")
print(f"   - Imóveis: {total_imoveis}")
print(f"   - Interesses: {total_interesses}")
print(f"   - Status de obras: {total_obras}")

# Deleta todos os registros
# As relações com ON_DELETE=CASCADE vão deletar automaticamente Interesse e ObraStatus
print("\n🗑️  Deletando todos os imóveis...")
Imovel.objects.all().delete()

# Verifica os resultados
imoveis_restantes = Imovel.objects.count()
interesses_restantes = Interesse.objects.count()
obras_restantes = ObraStatus.objects.count()

print("\n✅ Todos os imóveis foram removidos com sucesso!")
print(f"\n📊 Registros restantes:")
print(f"   - Imóveis: {imoveis_restantes}")
print(f"   - Interesses: {interesses_restantes}")
print(f"   - Status de obras: {obras_restantes}")