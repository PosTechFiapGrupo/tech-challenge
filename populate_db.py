"""
Script para popular o banco de dados com dados fictícios
Utiliza a biblioteca Faker para gerar dados realistas
"""

import asyncio
import random
import uuid
from decimal import Decimal
from faker import Faker
from faker.providers import automotive

from app.infrastructure.database import database
from app.infrastructure.models.cliente import ClienteModel
from app.infrastructure.models.vehicle_model import VehicleModel
from app.infrastructure.models.servico import ServicoModel
from app.infrastructure.models.inventory_item_model import InventoryItemModel
from app.infrastructure.models.ordem_servico import OrdemServicoModel
from app.infrastructure.models.ordem_servico_servico import OrdemServicoServicoModel
from app.infrastructure.models.ordem_servico_inventory_item import OrdemServicoInventoryItemModel

fake = Faker('pt_BR')
fake.add_provider(automotive)

# Dados base para geração
SERVICOS_BASE = [
    ("Troca de óleo", 80.00, 120.00),
    ("Alinhamento", 60.00, 100.00),
    ("Balanceamento", 40.00, 80.00),
    ("Troca de pneus", 200.00, 800.00),
    ("Revisão completa", 150.00, 300.00),
    ("Troca de pastilhas de freio", 120.00, 250.00),
    ("Troca de filtro de ar", 30.00, 60.00),
    ("Troca de filtro de combustível", 50.00, 90.00),
    ("Troca de velas", 80.00, 150.00),
    ("Regulagem de motor", 100.00, 200.00),
    ("Troca de correia dentada", 200.00, 400.00),
    ("Diagnóstico eletrônico", 60.00, 120.00),
    ("Lavagem completa", 25.00, 50.00),
    ("Enceramento", 40.00, 80.00),
    ("Troca de bateria", 150.00, 300.00),
]

INVENTORY_ITEMS_BASE = [
    ("Óleo de motor 5W30", "Lubrificante sintético", 45.00, 80.00),
    ("Filtro de óleo", "Filtro de óleo para motor", 15.00, 30.00),
    ("Filtro de ar", "Filtro de ar do motor", 25.00, 50.00),
    ("Filtro de combustível", "Filtro de combustível", 30.00, 60.00),
    ("Vela de ignição", "Vela de ignição NGK", 20.00, 40.00),
    ("Pastilha de freio dianteira", "Pastilha de freio cerâmica", 80.00, 150.00),
    ("Pastilha de freio traseira", "Pastilha de freio cerâmica", 70.00, 130.00),
    ("Disco de freio", "Disco de freio ventilado", 120.00, 250.00),
    ("Correia dentada", "Correia dentada Gates", 150.00, 300.00),
    ("Bateria 60Ah", "Bateria automotiva 60Ah", 200.00, 350.00),
    ("Pneu 185/65R15", "Pneu radial aro 15", 250.00, 400.00),
    ("Amortecedor dianteiro", "Amortecedor hidráulico", 180.00, 320.00),
    ("Amortecedor traseiro", "Amortecedor hidráulico", 160.00, 280.00),
    ("Fluido de freio", "Fluido de freio DOT 4", 25.00, 45.00),
    ("Aditivo de radiador", "Aditivo para radiador", 20.00, 35.00),
]

STATUS_OPTIONS = ["recebida", "em_diagnostico", "aguardando_aprovacao", "em_execucao", "finalizada", "entregue"]

async def create_clientes(session, count=20):
    """Criar clientes fictícios"""
    print(f"Criando {count} clientes...")
    clientes = []
    
    for _ in range(count):
        cliente = ClienteModel(
            id=str(uuid.uuid4()),
            nome=fake.name(),
            email=fake.email(),
            telefone=fake.phone_number(),
            cpf=fake.cpf()
        )
        clientes.append(cliente)
    
    session.add_all(clientes)
    await session.flush()
    return clientes

async def create_vehicles(session, clientes, count=30):
    """Criar veículos fictícios"""
    print(f"Criando {count} veículos...")
    vehicles = []
    
    marcas = ["Toyota", "Honda", "Ford", "Chevrolet", "Volkswagen", "Fiat", "Hyundai", "Nissan"]
    
    for _ in range(count):
        marca = random.choice(marcas)
        vehicle = VehicleModel(
            client_id=random.choice(clientes).id,
            license_plate=fake.license_plate().replace('-', ''),
            brand=marca,
            model=fake.word().title(),
            year=random.randint(2010, 2024)
        )
        vehicles.append(vehicle)
    
    session.add_all(vehicles)
    await session.flush()
    return vehicles

async def create_servicos(session):
    """Criar serviços baseados na lista predefinida"""
    print(f"Criando {len(SERVICOS_BASE)} serviços...")
    servicos = []
    
    for descricao, min_preco, max_preco in SERVICOS_BASE:
        preco = round(random.uniform(min_preco, max_preco), 2)
        servico = ServicoModel(
            id=str(uuid.uuid4()),
            descricao=descricao,
            preco=Decimal(str(preco))
        )
        servicos.append(servico)
    
    session.add_all(servicos)
    await session.flush()
    return servicos

async def create_inventory_items(session):
    """Criar itens de inventário baseados na lista predefinida"""
    print(f"Criando {len(INVENTORY_ITEMS_BASE)} itens de inventário...")
    items = []
    
    for nome, descricao, min_preco, max_preco in INVENTORY_ITEMS_BASE:
        preco = round(random.uniform(min_preco, max_preco), 2)
        quantidade = random.randint(5, 100)
        item = InventoryItemModel(
            name=nome,
            description=descricao,
            quantity=quantidade,
            minimum_stock=random.randint(3, 10),
            unit_price=Decimal(str(preco))
        )
        items.append(item)
    
    session.add_all(items)
    await session.flush()
    return items

async def create_ordens_servico(session, clientes, vehicles, servicos, count=50):
    """Criar ordens de serviço fictícias"""
    print(f"Criando {count} ordens de serviço...")
    ordens = []
    
    for _ in range(count):
        cliente = random.choice(clientes)
        # Filtrar veículos do cliente selecionado
        cliente_vehicles = [v for v in vehicles if v.client_id == cliente.id]
        if not cliente_vehicles:
            continue
            
        vehicle = random.choice(cliente_vehicles)
        
        ordem = OrdemServicoModel(
            id=str(uuid.uuid4()),
            cliente_id=cliente.id,
            vehicle_id=vehicle.id,
            mecanico_id=str(uuid.uuid4()),
            atendente_id=str(uuid.uuid4()),
            status=random.choice(STATUS_OPTIONS),
            data_abertura=fake.date_time_this_year()
        )
        
        # Se finalizada, adicionar data de fechamento
        if ordem.status in ["finalizada", "entregue"]:
            ordem.data_fechamento = fake.date_time_between(
                start_date=ordem.data_abertura,
                end_date='now'
            )
        
        ordens.append(ordem)
    
    session.add_all(ordens)
    await session.flush()
    return ordens

async def create_ordem_servico_servicos(session, ordens, servicos):
    """Criar relações entre ordens de serviço e serviços"""
    print("Criando relações ordem_servico <-> serviços...")
    relacoes = []
    
    for ordem in ordens:
        # Cada OS terá entre 1 e 4 serviços
        num_servicos = random.randint(1, 4)
        servicos_escolhidos = random.sample(servicos, num_servicos)
        
        for servico in servicos_escolhidos:
            # O valor será automaticamente copiado do preço atual do serviço
            relacao = OrdemServicoServicoModel(
                ordem_servico_id=ordem.id,
                servico_id=servico.id,
                valor_servico=servico.preco,  # Copia o valor atual
                observacoes=fake.sentence() if random.choice([True, False]) else None
            )
            relacoes.append(relacao)
    
    session.add_all(relacoes)
    await session.flush()
    return relacoes

async def create_ordem_servico_inventory_items(session, ordens, items):
    """Criar relações entre ordens de serviço e itens de inventário"""
    print("Criando relações ordem_servico <-> itens de inventário...")
    relacoes = []
    
    for ordem in ordens:
        # Nem toda OS terá itens, apenas 70%
        if random.random() > 0.7:
            continue
            
        # Cada OS terá entre 1 e 3 itens
        num_items = random.randint(1, 3)
        items_escolhidos = random.sample(items, num_items)
        
        for item in items_escolhidos:
            quantidade = random.randint(1, 5)
            # O valor será automaticamente copiado do preço atual do item
            relacao = OrdemServicoInventoryItemModel(
                ordem_servico_id=ordem.id,
                inventory_item_id=item.id,
                quantidade=quantidade,
                valor_unitario=item.unit_price  # Copia o valor atual
            )
            relacoes.append(relacao)
    
    session.add_all(relacoes)
    await session.flush()
    return relacoes

async def populate_database():
    """Função principal para popular o banco de dados"""
    print("Iniciando população do banco de dados...")
    
    session_gen = database.get_session()
    session = await session_gen.__anext__()
    
    try:
        # Criar dados em ordem de dependência
        clientes = await create_clientes(session, 25)
        vehicles = await create_vehicles(session, clientes, 40)
        servicos = await create_servicos(session)
        items = await create_inventory_items(session)
        ordens = await create_ordens_servico(session, clientes, vehicles, servicos, 60)
        
        # Criar relações
        await create_ordem_servico_servicos(session, ordens, servicos)
        await create_ordem_servico_inventory_items(session, ordens, items)
        
        await session.commit()
        print("✅ Banco de dados populado com sucesso!")
        
        # Estatísticas
        print(f"📊 Estatísticas:")
        print(f"   - {len(clientes)} clientes criados")
        print(f"   - {len(vehicles)} veículos criados")
        print(f"   - {len(servicos)} serviços criados")
        print(f"   - {len(items)} itens de inventário criados")
        print(f"   - {len(ordens)} ordens de serviço criadas")
        
    except Exception as e:
        await session.rollback()
        print(f"❌ Erro ao popular banco de dados: {e}")
        raise
    finally:
        await session.close()
        # Fechar conexões do pool de forma explícita
        await database.close()

if __name__ == "__main__":
    asyncio.run(populate_database())
