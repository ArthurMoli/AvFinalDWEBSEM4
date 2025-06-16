#!/usr/bin/env python3
import os
import django
from decimal import Decimal

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from properties.models import Imovel
from users.models import User

# Pega o primeiro usuário corretor ou cria um usuário de exemplo
try:
    corretor = User.objects.filter(perfil='CO').first()
    if not corretor:
        corretor = User.objects.first()
    print(f"👤 Usando usuário: {corretor.username}")
except:
    print("❌ Nenhum usuário encontrado. Crie um usuário primeiro.")
    exit()

# Lista de imóveis de exemplo com dados realistas
imoveis_exemplo = [
    {
        'titulo': 'Apartamento Garden no Jardim Europa',
        'endereco': 'Rua Augusta, 1500 - Jardim Europa, São Paulo - SP',
        'preco': Decimal('850000.00'),
        'tipo': 'AP',
        'quartos': 3,
        'descricao': '''Apartamento garden de alto padrão com 156m², localizado em uma das regiões mais nobres de São Paulo. 
        
Características:
• 3 quartos sendo 1 suíte master com closet
• Sala ampla com pé direito duplo
• Cozinha americana planejada
• Área gourmet privativa com churrasqueira
• 2 vagas de garagem cobertas
• Condomínio com piscina, academia e salão de festas

Apartamento todo reformado com acabamentos de primeira linha. Pronto para morar!''',
        'capa_url': 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800&h=600'
    },
    {
        'titulo': 'Casa Térrea Moderna no Alphaville',
        'endereco': 'Alameda Araguaia, 2000 - Alphaville, Barueri - SP',
        'preco': Decimal('1200000.00'),
        'tipo': 'CA',
        'quartos': 4,
        'descricao': '''Casa térrea moderna em condomínio fechado de alto padrão no Alphaville.

Detalhes do imóvel:
• 4 suítes com armários planejados
• Living integrado com jardim
• Cozinha gourmet equipada
• Piscina aquecida com deck
• Espaço gourmet com forno de pizza
• Home office
• 4 vagas de garagem
• Terreno de 500m² / Construção de 320m²

Segurança 24h e área de lazer completa do condomínio.''',
        'capa_url': 'https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800&h=600'
    },
    {
        'titulo': 'Studio Compacto na Vila Madalena',
        'endereco': 'Rua Harmonia, 800 - Vila Madalena, São Paulo - SP',
        'preco': Decimal('420000.00'),
        'tipo': 'AP',
        'quartos': 1,
        'descricao': '''Studio moderno e funcional no coração da Vila Madalena, perfeito para jovens profissionais.

Características:
• 35m² otimizados com móveis planejados
• Varanda integrada
• Cozinha americana
• 1 vaga de garagem
• Andar alto com vista livre
• A 5 minutos do metrô

Prédio novo com rooftop, coworking e bike sharing. Excelente para investimento ou moradia!''',
        'capa_url': 'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600'
    },
    {
        'titulo': 'Cobertura Duplex com Vista Mar',
        'endereco': 'Av. Atlântica, 3000 - Copacabana, Rio de Janeiro - RJ',
        'preco': Decimal('3500000.00'),
        'tipo': 'AP',
        'quartos': 4,
        'descricao': '''Cobertura duplex espetacular com vista panorâmica para o mar de Copacabana.

Primeiro andar:
• Salão de 120m² com vista mar
• 4 suítes amplas
• Cozinha planejada
• Lavabo
• Dependência completa

Segundo andar:
• Terraço de 200m² com piscina
• Churrasqueira e forno de pizza  
• Sauna seca
• Jardim suspenso
• Vista 360° da cidade

Prédio com apenas 2 coberturas, portaria 24h.''',
        'capa_url': 'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&h=600'
    },
    {
        'titulo': 'Casa Colonial no Centro Histórico',
        'endereco': 'Rua do Carmo, 150 - Centro Histórico, Paraty - RJ',
        'preco': Decimal('2800000.00'),
        'tipo': 'CA',
        'quartos': 5,
        'descricao': '''Belíssima casa colonial restaurada no centro histórico de Paraty, tombada pelo patrimônio.

Características únicas:
• 5 quartos amplos com pé direito alto
• Salões nobres com piso original
• Pátio interno com jardim tropical  
• Cozinha rústica com fogão a lenha
• Biblioteca com mezanino
• Adega climatizada
• Área de 450m²

Ideal para pousada boutique ou residência de alto padrão. Oportunidade única!''',
        'capa_url': 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&h=600'
    }
]

# Cria os imóveis
print("\n📝 Criando imóveis de exemplo...")
for dados in imoveis_exemplo:
    imovel = Imovel.objects.create(
        owner=corretor,
        **dados
    )
    print(f"✅ Criado: {imovel.titulo}")

print(f"\n🎉 Total de {len(imoveis_exemplo)} imóveis criados com sucesso!")