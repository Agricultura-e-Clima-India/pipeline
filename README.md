# Pipeline de Dados - Sistema de Recomendação Agrícola Inteligente

## Descrição

Pipeline de dados ETL (Extração, Transformação e Carga) focado em processar dados brutos de produção agrícola. O objetivo é limpar, padronizar, enriquecer e agregar os dados para permitir análises de desempenho (produção, rendimento) por região, cultura e ano, bem como análises de volatilidade (risco).


## Estrutura de Dados

### Camada Bronze

- **Localização:** `data/bronze/`
- **Descrição:** Dados brutos, com nomes de colunas padronizados.
- **Arquivo:** `dados_brutos.csv`
- **Correções Implementadas:**
    1.  **Padronização de Nomes de Colunas:** Todos os nomes de colunas foram convertidos para o formato `snake_case` (minúsculas, com underscores), corrigindo espaços, hifens e outros caracteres especiais. Exemplos: `Area ` se torna `area`, `Jun-Sep` se torna `jun_sep`.

### Camada Silver

- **Localização:** `data/silver/`
- **Descrição:** Dados limpos, validados e consistentes. Prontos para análise e modelagem dimensional.
- **Arquivo:** `dados_limpos.csv`
- **Transformações aplicadas:**
    1.  Remoção de duplicatas.
    2.  Tratamento de valores nulos (remoção de linhas onde `state` ou `district` são nulos).
    3.  **Padronização de Valores:** Padronização de valores para `UPPER()` em colunas de texto (`state`, `district`, `crop`, `season`) antes de qualquer filtro.
    4.  **Criação da coluna-chave `state_district`** (combinando as colunas `state` e `district`).
    5.  **Filtragem de Culturas** (limitando o escopo para `MAIZE`, `RICE`, `WHEAT`, `BARLEY`).
    6.  **Remoção de dados inválidos** (linhas onde `area` ou `yield` são 0, que causam distorções).
    7.  Preenchimento de nulos restantes (mediana para numéricos, 'Desconhecido' para categóricos).

### Camada Gold

- **Localização:** `data/gold/`
- **Descrição:** Dados agregados e sumarizados, com nomes de colunas e arquivos padronizados para minúsculas. Prontos para BI e relatórios.
- **Arquivos:** Contém 7 tabelas de agregação (ex: `producao_anual_cultura.csv`, `desempenho_regiao_cultura.csv`, etc.).

## Banco de Dados (Modelagem Dimensional)

- **Tipo:** SQLite e PostgreSQL
- **Localização:** `data/pipeline_agricultura.db` (SQLite) e banco `pipeline_db` (PostgreSQL).
- **Modelagem:** Implementação de um **Schema Star** (Estrela) para otimizar consultas analíticas (no SQLite) e um schema relacional com as tabelas agregadas (no PostgreSQL).
- **Tabelas (Exemplos):**
    - **fato_producao (SQLite):** Tabela fato contendo as métricas (`production`, `yield`, dados climáticos) e **chaves estrangeiras** para as dimensões.
    - **dim_regiao (SQLite):** Tabela de dimensão para regiões (`state_district`).
    - **dim_cultura (SQLite):** Tabela de dimensão para culturas (`crop`).
    - **dim_temporada (SQLite):** Tabela de dimensão para temporadas (`season`).
    - **Tabelas Agregadas (SQLite e PostgreSQL):** As 7 tabelas da camada Gold são carregadas com nomes e colunas padronizados (ex: `producao_anual_cultura`, `desempenho_regiao_cultura`).

## Qualidade dos Dados
- Completude Geral: 100.00%
- Unicidade:
Linhas únicas: 100.00%
Duplicatas encontradas: 0
- Score Geral: 100.00%
- Classificação: EXCELENTE

## Como Executar

1.  **Configurar Variáveis de Ambiente:**
    Crie um arquivo `.env` na raiz do projeto com as credenciais do seu banco PostgreSQL. Use o `.env.example` como modelo.

2.  **Criar e ativar o ambiente virtual:**
    Certifique-se de ter o Python 3.11 ou superior instalado.
    ```bash
    python -m venv .venv
    # Windows
    .\.venv\Scripts\Activate
    # macOS/Linux
    source .venv/bin/activate
    ```
3.  **Instalar as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Executar os notebooks Jupyter na seguinte ordem:**
    1. `notebooks/01_bronze_layer.ipynb`
    2. `notebooks/02_silver_layer.ipynb`
    3. `notebooks/03_gold_layer.ipynb`
    4. `notebooks/04_load_to_sqlite.ipynb`
    5. `notebooks/05_create_database_pg_schema.ipynb`
    6. `notebooks/06_load_to_postgres.ipynb`
    7. `notebooks/analysis/data_quality_report.ipynb`    
    8. `notebooks/analysis/SQL_queries.ipynb`


Consulte o banco de dados:

O notebook `SQL_queries.ipynb` contém 12 consultas abrangentes que exploram a modelagem dimensional no banco de dados SQLite. Exemplos de análises incluídas:

| Análise | Exemplo de Consulta |
| **Benchmark** | Top 5 Regiões com Rendimento Acima da Média Nacional (RICE) |
| **Risco** | Top 5 Regiões Mais/Menos Estáveis (Volatilidade - MAIZE/WHEAT) |
| **Fatores Ideais** | Perfil Climático da Região Mais Produtiva (RICE) |
| **Tendência** | Crescimento Anual do Rendimento (WHEAT) |
| **Modelagem** | Top 10 Regiões por Produção Total (Usando JOINs com Dimensões) |