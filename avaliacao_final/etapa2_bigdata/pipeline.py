from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "data" / "avaliacao_transactions.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)
DB = OUT / "techpay.duckdb"

con = duckdb.connect(str(DB))

# RAW: leitura tipada do arquivo original
con.execute(f"""
CREATE OR REPLACE TABLE raw_transactions AS
SELECT
    CAST(transaction_id AS BIGINT) AS transaction_id,
    CAST(customer_id AS BIGINT) AS customer_id,
    CAST(amount AS DOUBLE) AS amount,
    CAST(transaction_type AS VARCHAR) AS transaction_type,
    CAST(channel AS VARCHAR) AS channel,
    CAST(merchant_category AS VARCHAR) AS merchant_category,
    CAST(timestamp AS TIMESTAMP) AS timestamp,
    CAST(status AS VARCHAR) AS status,
    CAST(risk_score AS DOUBLE) AS risk_score,
    CAST(segment AS VARCHAR) AS segment,
    CAST(credit_score AS INTEGER) AS credit_score,
    CAST(is_fraud AS BOOLEAN) AS is_fraud
FROM read_csv_auto('{INPUT.as_posix()}', header=true);
""")

# BRONZE: deduplicação e validações de domínio
con.execute("""
CREATE OR REPLACE TABLE bronze_transactions AS
WITH dedup AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY transaction_id ORDER BY timestamp) AS rn
    FROM raw_transactions
)
SELECT * EXCLUDE (rn)
FROM dedup
WHERE rn = 1
  AND transaction_id IS NOT NULL
  AND customer_id IS NOT NULL
  AND amount > 0
  AND timestamp IS NOT NULL
  AND risk_score BETWEEN 0 AND 100
  AND credit_score BETWEEN 300 AND 900
  AND channel IN ('app','web','pos','atm')
  AND merchant_category IN ('varejo','viagem','eletronico','alimentacao','servicos','saude')
  AND transaction_type IN ('compra','saque','transferencia','pagamento')
  AND status IN ('approved','declined');
""")

# SILVER: enriquecimento analítico
con.execute("""
CREATE OR REPLACE TABLE silver_transactions AS
SELECT *,
    EXTRACT(YEAR FROM timestamp)::INTEGER AS ano,
    EXTRACT(MONTH FROM timestamp)::INTEGER AS mes,
    EXTRACT(DAY FROM timestamp)::INTEGER AS dia,
    EXTRACT(HOUR FROM timestamp)::INTEGER AS hora,
    STRFTIME(timestamp, '%A') AS dia_semana,
    CASE
        WHEN EXTRACT(HOUR FROM timestamp) BETWEEN 0 AND 4 THEN 'madrugada'
        WHEN EXTRACT(HOUR FROM timestamp) BETWEEN 5 AND 11 THEN 'manha'
        WHEN EXTRACT(HOUR FROM timestamp) BETWEEN 12 AND 17 THEN 'tarde'
        ELSE 'noite'
    END AS periodo_dia,
    CASE
        WHEN amount < 50 THEN 'ate_50'
        WHEN amount < 200 THEN '50_199'
        WHEN amount < 1000 THEN '200_999'
        ELSE '1000_mais'
    END AS faixa_valor
FROM bronze_transactions;
""")

# GOLD 1: canal + categoria
con.execute("""
CREATE OR REPLACE TABLE gold_risco_canal_categoria AS
SELECT
    channel,
    merchant_category,
    COUNT(*) AS total_transacoes,
    SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) AS fraudes,
    AVG(CASE WHEN is_fraud THEN 1.0 ELSE 0.0 END) AS taxa_fraude,
    AVG(risk_score) AS risk_score_medio,
    SUM(amount) AS volume_financeiro
FROM silver_transactions
GROUP BY 1,2;
""")

# GOLD 2: tempo + segmento
con.execute("""
CREATE OR REPLACE TABLE gold_risco_temporal_segmento AS
SELECT
    ano, mes, periodo_dia, segment,
    COUNT(*) AS total_transacoes,
    SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) AS fraudes,
    AVG(CASE WHEN is_fraud THEN 1.0 ELSE 0.0 END) AS taxa_fraude,
    AVG(risk_score) AS risk_score_medio,
    SUM(amount) AS volume_financeiro
FROM silver_transactions
GROUP BY 1,2,3,4;
""")

# Persistência em Parquet; Silver particionada por ano/mês
con.execute(f"COPY bronze_transactions TO '{(OUT/'bronze_transactions.parquet').as_posix()}' (FORMAT PARQUET);")
con.execute(f"COPY silver_transactions TO '{(OUT/'silver').as_posix()}' (FORMAT PARQUET, PARTITION_BY (ano, mes), OVERWRITE_OR_IGNORE);")
con.execute(f"COPY gold_risco_canal_categoria TO '{(OUT/'gold_risco_canal_categoria.parquet').as_posix()}' (FORMAT PARQUET);")
con.execute(f"COPY gold_risco_temporal_segmento TO '{(OUT/'gold_risco_temporal_segmento.parquet').as_posix()}' (FORMAT PARQUET);")

for tabela in ['raw_transactions','bronze_transactions','silver_transactions','gold_risco_canal_categoria','gold_risco_temporal_segmento']:
    n = con.execute(f"SELECT COUNT(*) FROM {tabela}").fetchone()[0]
    print(f"{tabela}: {n} linhas")

print("\nFraude por canal:")
print(con.execute("""
SELECT channel, COUNT(*) total, SUM(is_fraud::INT) fraudes,
       ROUND(100*AVG(is_fraud::INT),2) taxa_fraude_pct
FROM silver_transactions GROUP BY 1 ORDER BY taxa_fraude_pct DESC
""").df().to_string(index=False))

con.close()
