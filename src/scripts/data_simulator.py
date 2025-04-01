import os
import time
from datetime import datetime, timedelta
import random
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from supabase import create_client, Client
from faker import Faker
import sys
import json

# Carregar variáveis de ambiente
load_dotenv()

# Configurar Supabase
try:
    supabase: Client = create_client(
        os.getenv("SUPABASE_URL", ""),
        os.getenv("SUPABASE_KEY", "")
    )
    print("Conexão com Supabase estabelecida com sucesso!")
except Exception as e:
    print(f"Erro ao conectar com Supabase: {e}")
    sys.exit(1)

fake = Faker()

def check_tables_exist():
    """
    Verifica se as tabelas necessárias existem
    """
    try:
        # Verificar tabela data_lake_metrics
        response = supabase.table("data_lake_metrics").select("id").limit(1).execute()
        print("Tabela data_lake_metrics existe e está acessível")
        
        # Verificar tabela data_warehouse_metrics
        response = supabase.table("data_warehouse_metrics").select("id").limit(1).execute()
        print("Tabela data_warehouse_metrics existe e está acessível")
        
        return True
    except Exception as e:
        print(f"Erro ao verificar tabelas: {e}")
        print("\nIMPORTANTE: Execute o script SQL de inicialização no Supabase primeiro!")
        print("O script está localizado em: src/config/init.sql")
        sys.exit(1)

def generate_data_lake_metrics(num_records: int = 1) -> pd.DataFrame:
    """
    Gera métricas simuladas para o Data Lake
    """
    now = datetime.now()
    data = []
    
    for i in range(num_records):
        timestamp = now - timedelta(minutes=i)
        record = {
            'data': timestamp.isoformat(),
            'espaco_utilizado_gb': round(random.uniform(100, 1000), 2),
            'numero_acessos': random.randint(50, 500),
            'tempo_acesso_ms': round(random.uniform(10, 200), 2)
        }
        data.append(record)
    
    return pd.DataFrame(data)

def generate_data_warehouse_metrics(num_records: int = 1) -> pd.DataFrame:
    """
    Gera métricas simuladas para o Data Warehouse
    """
    now = datetime.now()
    data = []
    
    for i in range(num_records):
        timestamp = now - timedelta(minutes=i)
        record = {
            'data': timestamp.isoformat(),
            'tempo_resposta_ms': round(random.uniform(50, 500), 2),
            'registros_processados': random.randint(1000, 10000)
        }
        data.append(record)
    
    return pd.DataFrame(data)

def insert_metrics():
    """
    Insere métricas simuladas no Supabase
    """
    try:
        # Gerar dados
        dl_metrics = generate_data_lake_metrics()
        dw_metrics = generate_data_warehouse_metrics()
        
        # Inserir dados do Data Lake
        dl_response = supabase.table("data_lake_metrics").insert(dl_metrics.to_dict('records')).execute()
        print(f"Dados inseridos na tabela data_lake_metrics: {len(dl_metrics)} registros")
        
        # Inserir dados do Data Warehouse
        dw_response = supabase.table("data_warehouse_metrics").insert(dw_metrics.to_dict('records')).execute()
        print(f"Dados inseridos na tabela data_warehouse_metrics: {len(dw_metrics)} registros")
        
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")
        sys.exit(1)

def simulate_continuous_data(interval_seconds: int = 60):
    """
    Simula dados continuamente com intervalo especificado
    """
    try:
        print(f"Iniciando simulação contínua de dados (intervalo: {interval_seconds}s)...")
        while True:
            insert_metrics()
            print(f"Dados inseridos em {datetime.now()}")
            time.sleep(interval_seconds)
    
    except KeyboardInterrupt:
        print("\nSimulação interrompida pelo usuário")
    except Exception as e:
        print(f"Erro durante a simulação: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        # Verificar se as tabelas existem
        print("Verificando existência das tabelas...")
        check_tables_exist()
        
        # Iniciar simulação contínua
        simulate_continuous_data()
    
    except Exception as e:
        print(f"Erro na execução: {e}")
        sys.exit(1) 