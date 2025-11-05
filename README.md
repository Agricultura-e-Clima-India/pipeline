# Pipeline de Dados - Sistema de Recomendação Agrícola Inteligente

## Descrição

Pipeline de dados ETL (Extração, Transformação e Carga) focado em processar dados brutos de produção agrícola. O objetivo é limpar, padronizar, enriquecer e agregar os dados para permitir análises de desempenho (produção, rendimento) por região, cultura e ano, bem como análises de volatilidade (risco).


## Estrutura de Dados

### Camada Bronze

- **Localização:** `data/bronze/`
- **Descrição:** Dados brutos, com correções iniciais para garantir a consistência dos nomes de colunas.
- **Arquivo:** `dados_brutos.csv`
- **Correções Implementadas:**
    1.  Renomeação da coluna `Area ` (com espaço) para `Area`.
    2.  Renomeação das colunas de temperatura (ex: `JUN-SEP`) para nomes não ambíguos (ex: `TEMP_JUN_SEP`) para evitar conflito com as colunas de precipitação.

### Camada Silver

- **Localização:** `data/silver/`
- **Descrição:** Dados limpos, validados e consistentes. Prontos para análise e modelagem dimensional.
- **Arquivo:** `dados_limpos.csv`
- **Transformações aplicadas:**
    1.  Remoção de duplicatas.
    2.  Tratamento de valores nulos (remoção de linhas onde `State` ou `District` são nulos).
    3.  **Padronização Corrigida:** Padronização de valores para `UPPER()` em colunas de texto (`State`, `District`, `Crop`, `Season`) **antes** de qualquer filtro.
    4.  **Criação da coluna-chave `State District`** (combinando as colunas `State` e `District`).
    5.  **Filtragem de Culturas** (limitando o escopo para `MAIZE`, `RICE`, `WHEAT`, `BARLEY`).
    6.  **Remoção de dados inválidos** (linhas onde `Area` ou `Yield` são 0, que causam distorções).
    7.  Preenchimento de nulos restantes (mediana para numéricos, 'Desconhecido' para categóricos).

### Camada Gold

- **Localização:** `data/gold/`
- **Descrição:** Dados agregados e sumarizados, prontos para BI e relatórios.
- **Arquivos:** Contém 7 tabelas de agregação (Produção Anual, Desempenho Regional, Análise Sazonal, Tendência de Rendimento, Benchmark Regional, Perfil Climático e Volatilidade de Rendimento).

## Banco de Dados (Modelagem Dimensional)

- **Tipo:** SQLite
- **Localização:** `data/pipeline_agricultura.db`
- **Modelagem:** Implementação de um **Schema Star** (Estrela) para otimizar consultas analíticas.
- **Tabelas:**
    - **fato_producao:** Tabela fato contendo as métricas (`Production`, `Yield`, dados climáticos) e **chaves estrangeiras** para as dimensões.
    - **dim_regiao:** Tabela de dimensão para regiões (`State District`).
    - **dim_cultura:** Tabela de dimensão para culturas (`Crop`).
    - **dim_temporada:** Tabela de dimensão para temporadas (`Season`).
    - **AGREGAÇÃO 1**: Produção Anual por Cultura. 
    - **AGREGAÇÃO 2:** Desempenho por Região e Cultura
    - **AGREGAÇÃO 3:** Análise Sazonal e Climática
    - **AGREGAÇÃO 4:** Tendência de Rendimento Ano-a-Ano (Growth)
    - **AGREGAÇÃO 5:** Benchmark de Desempenho Regional (vs. Média Nacional)
    - **AGREGAÇÃO 6:** Perfil Climático por Região e Cultura
    - **AGREGAÇÃO 7:** Análise de Volatilidade (Risco) do Rendimento



## Qualidade dos Dados
- Completude Geral: 100.00%
- Unicidade:
Linhas únicas: 100.00%
Duplicatas encontradas: 0
- Score Geral: 100.00%
- Classificação: EXCELENTE

## Como Executar

1.  **Abrir ambiente virtual com dependências já instaladas:**
    ```bash
    .\ambiente_virtual\Scripts\Activate
    ```
2.  **Execução dos Notebooks:**
    ORDEM:
 • 1°    - `#bronze_layer.ipynb`
 • 2°    - `#silver_layer.ipynb`
 • 3°    - `#gold_layer.ipynb`
 • 4°    - `load_to_database.ipynb`
 • 5°    - `SQL_queries.ipynb`
 • 6°    - `data_quality_report.ipynb`    

Consulte o banco de dados:
```python
import sqlite3
conn = sqlite3.connect('data/pipeline_agricultura.db')

O notebook `SQL_queries.ipynb` contém 12 consultas abrangentes que exploram a modelagem dimensional. Exemplos de análises incluídas:

| Análise | Exemplo de Consulta |
| **Benchmark** | Top 5 Regiões com Rendimento Acima da Média Nacional (RICE) |
| **Risco** | Top 5 Regiões Mais/Menos Estáveis (Volatilidade - MAIZE/WHEAT) |
| **Fatores Ideais** | Perfil Climático da Região Mais Produtiva (RICE) |
| **Tendência** | Crescimento Anual do Rendimento (WHEAT) |
| **Modelagem** | Top 10 Regiões por Produção Total (Usando JOINs com Dimensões) |

Queries:

**QUERY 1:** Total de Registros na Tabela Fato
**QUERY 2:** Top 10 Regiões por Produção Total
**QUERY 3:** Análise Temporal (Produção por Ano)
**QUERY 4:** Resumo de Desempenho por Cultura
**QUERY 5:** Top 5 Regiões Mais Estáveis (MAIZE)
**QUERY 6:** Regiões com Melhor Desempenho vs. Média Nacional (RICE)
**QUERY 7:** Tendência de Crescimento Anual (WHEAT)
**QUERY 8:** Perfil Climático da Região Mais Produtiva (RICE)
**QUERY 9:** Desempenho Sazonal (RICE)
**QUERY 10:** Regiões com Maior Volatilidade (WHEAT)
**QUERY 11:** Análise de Produção Anual (MAIZE)
**QUERY 12:** Regiões com Pior Desempenho vs. Média Nacional (BARLEY)
