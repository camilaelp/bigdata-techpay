from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "data" / "avaliacao_transactions.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(INPUT, parse_dates=['timestamp'])
df['hora'] = df['timestamp'].dt.hour
df['mes'] = df['timestamp'].dt.month

def resumo(grupo):
    return (df.groupby(grupo)['is_fraud']
              .agg(total='size', fraudes='sum', taxa_fraude='mean')
              .sort_values('taxa_fraude', ascending=False))

resumo('channel').to_csv(OUT/'analise_canal.csv')
resumo('merchant_category').to_csv(OUT/'analise_categoria.csv')
resumo('segment').to_csv(OUT/'analise_segmento.csv')
resumo('hora').to_csv(OUT/'analise_hora.csv')

combo = resumo(['channel','merchant_category'])
combo.to_csv(OUT/'analise_canal_categoria.csv')

print('Taxa geral de fraude:', f"{df['is_fraud'].mean():.2%}")
print('\nCanal')
print(resumo('channel'))
print('\nCategoria')
print(resumo('merchant_category'))
print('\nSegmento')
print(resumo('segment'))
print('\nTop combinações canal x categoria')
print(combo.head(10))
