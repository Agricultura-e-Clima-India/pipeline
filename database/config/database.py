import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env para o ambiente
load_dotenv()

# --- Leitura das Variáveis de Ambiente ---
PG_USER = os.getenv('PG_USER', 'postgres')
PG_PASSWORD = os.getenv('PG_PASSWORD', 'postgres')
PG_HOST = os.getenv('PG_HOST', 'localhost')
PG_PORT = os.getenv('PG_PORT', '5432')
PG_DATABASE = os.getenv('PG_DATABASE', 'pipeline_db')

# ----------------------------------------

def get_connection_string(db_name=None):
    """Retorna string de conexão PostgreSQL para o banco de dados especificado."""
    database = db_name if db_name else PG_DATABASE
    return f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{database}"

def get_engine(db_name=None):
    """Retorna SQLAlchemy engine para o banco de dados especificado."""
    return create_engine(get_connection_string(db_name))

def create_database_if_not_exists():
    """Cria o banco de dados no PostgreSQL se ele não existir."""
    try:
        # Primeiro, verifica-se a existência do banco de dados.
        engine = get_engine('postgres')
        with engine.connect() as connection:
            result = connection.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{PG_DATABASE}'"))
            exists = result.scalar() == 1

        # Se o banco de dados já existe, não faz mais nada.
        if exists:
            print(f"Banco de dados '{PG_DATABASE}' já existe.")
            return

        # Se não existe, cria-se uma engine com autocommit para a criação.
        # A conexão anterior (do bloco 'with' acima) já foi fechada.
        print(f"Banco de dados '{PG_DATABASE}' não encontrado. Criando...")
        autocommit_engine = create_engine(get_connection_string('postgres'), isolation_level='AUTOCOMMIT')
        with autocommit_engine.connect() as connection:
            connection.execute(text(f'CREATE DATABASE "{PG_DATABASE}"'))
        autocommit_engine.dispose()
        print(f"Banco de dados '{PG_DATABASE}' criado com sucesso.")

    except Exception as e:
        print(f"Erro ao verificar ou criar o banco de dados: {e}")
        raise