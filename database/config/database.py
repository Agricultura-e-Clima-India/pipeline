import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env para o ambiente
load_dotenv()

# --- Leitura das Variáveis de Ambiente ---
# Lemos as variáveis do .env. Se não existirem,
# usamos um valor padrão (similar ao que você tinha).
PG_USER = os.getenv('PG_USER', 'postgres')
PG_PASSWORD = os.getenv('PG_PASSWORD', 'postgres')
PG_HOST = os.getenv('PG_HOST', 'localhost')
PG_PORT = os.getenv('PG_PORT', '5432')
PG_DATABASE = os.getenv('PG_DATABASE', 'pipeline_db') # Default do seu código original

# ----------------------------------------

def get_connection_string():
    """Retorna string de conexão PostgreSQL lida do .env"""
    return f"postgresql://{PG_USER}:{PG_PASSWORD}@" \
           f"{PG_HOST}:{PG_PORT}/{PG_DATABASE}"

def get_engine():
    """Retorna SQLAlchemy engine"""
    return create_engine(get_connection_string())