import os
import time
from datetime import datetime
from prometheus_client import start_http_server, Gauge, Counter
from dotenv import load_dotenv
from supabase import create_client, Client
import sys

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

# Definir métricas do Prometheus
# Métricas do Data Lake
dl_espaco_utilizado = Gauge('data_lake_espaco_utilizado_gb', 'Espaço utilizado no Data Lake em GB')
dl_numero_acessos = Gauge('data_lake_numero_acessos', 'Número de acessos ao Data Lake')
dl_tempo_acesso = Gauge('data_lake_tempo_acesso_ms', 'Tempo médio de acesso ao Data Lake em ms')

# Métricas do Data Warehouse
dw_tempo_resposta = Gauge('data_warehouse_tempo_resposta_ms', 'Tempo de resposta do Data Warehouse em ms')
dw_registros_processados = Gauge('data_warehouse_registros_processados', 'Número de registros processados no Data Warehouse')

# Contador de atualizações
updates_total = Counter('telemetry_updates_total', 'Total number of metric updates')

def get_latest_metrics():
    """
    Obtém as métricas mais recentes do Supabase
    """
    try:
        # Obter últimas métricas do Data Lake
        dl_response = supabase.table("data_lake_metrics") \
            .select("*") \
            .order('data', desc=True) \
            .limit(1) \
            .execute()
        
        if dl_response.data:
            dl_metrics = dl_response.data[0]
            dl_espaco_utilizado.set(dl_metrics['espaco_utilizado_gb'])
            dl_numero_acessos.set(dl_metrics['numero_acessos'])
            dl_tempo_acesso.set(dl_metrics['tempo_acesso_ms'])
            print(f"Métricas do Data Lake atualizadas: {dl_metrics}")
        
        # Obter últimas métricas do Data Warehouse
        dw_response = supabase.table("data_warehouse_metrics") \
            .select("*") \
            .order('data', desc=True) \
            .limit(1) \
            .execute()
        
        if dw_response.data:
            dw_metrics = dw_response.data[0]
            dw_tempo_resposta.set(dw_metrics['tempo_resposta_ms'])
            dw_registros_processados.set(dw_metrics['registros_processados'])
            print(f"Métricas do Data Warehouse atualizadas: {dw_metrics}")
        
        updates_total.inc()
        
    except Exception as e:
        print(f"Erro ao obter métricas: {e}")

def main():
    try:
        # Iniciar servidor HTTP do Prometheus na porta 8000, acessível de qualquer interface
        start_http_server(8000, addr='0.0.0.0')
        print("Servidor de métricas iniciado em http://0.0.0.0:8000")
        
        while True:
            get_latest_metrics()
            print(f"Métricas atualizadas em {datetime.now()}")
            time.sleep(60)  # Atualizar métricas a cada minuto
            
    except Exception as e:
        print(f"Erro no servidor de métricas: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServidor interrompido pelo usuário")
    except Exception as e:
        print(f"Erro na execução do servidor: {e}")
        sys.exit(1) 