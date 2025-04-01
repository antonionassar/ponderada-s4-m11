-- Criar tabela para métricas do Data Lake
CREATE TABLE IF NOT EXISTS public.data_lake_metrics (
    id BIGSERIAL PRIMARY KEY,
    data TIMESTAMP WITH TIME ZONE NOT NULL,
    espaco_utilizado_gb DECIMAL NOT NULL,
    numero_acessos INTEGER NOT NULL,
    tempo_acesso_ms DECIMAL NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- Criar tabela para métricas do Data Warehouse
CREATE TABLE IF NOT EXISTS public.data_warehouse_metrics (
    id BIGSERIAL PRIMARY KEY,
    data TIMESTAMP WITH TIME ZONE NOT NULL,
    tempo_resposta_ms DECIMAL NOT NULL,
    registros_processados INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- Configurar RLS (Row Level Security)
ALTER TABLE public.data_lake_metrics ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.data_warehouse_metrics ENABLE ROW LEVEL SECURITY;

-- Criar políticas de acesso
CREATE POLICY "Enable read access for all users" ON public.data_lake_metrics
    FOR SELECT USING (true);

CREATE POLICY "Enable insert for authenticated users only" ON public.data_lake_metrics
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Enable read access for all users" ON public.data_warehouse_metrics
    FOR SELECT USING (true);

CREATE POLICY "Enable insert for authenticated users only" ON public.data_warehouse_metrics
    FOR INSERT WITH CHECK (true); 