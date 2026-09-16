from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "data" / "avaliacao_transactions.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(INPUT, parse_dates=['timestamp'])
df['mes'] = df['timestamp'].dt.to_period('M').astype(str)
df['hora'] = df['timestamp'].dt.hour

taxa = df['is_fraud'].mean()
fraudes = int(df['is_fraud'].sum())
volume = df['amount'].sum()
canal = df.groupby('channel')['is_fraud'].mean().sort_values(ascending=False)
mensal = df.groupby('mes')['is_fraud'].mean()
cat = df.groupby('merchant_category')['is_fraud'].mean().sort_values(ascending=False)
detalhe = (df.groupby(['channel','merchant_category'])['is_fraud']
             .agg(['size','sum','mean']).reset_index()
             .sort_values('mean',ascending=False).head(10))

fig = make_subplots(
    rows=3, cols=2,
    specs=[[{'type':'indicator'},{'type':'indicator'}],
           [{'type':'xy'},{'type':'xy'}],
           [{'type':'xy','colspan':2}, None]],
    subplot_titles=('Taxa geral de fraude','Fraudes identificadas',
                    'Tendência mensal','Fraude por canal',
                    'Top 10 combinações canal × categoria')
)
fig.add_trace(go.Indicator(mode='number', value=taxa*100, number={'suffix':'%','valueformat':'.2f'}),1,1)
fig.add_trace(go.Indicator(mode='number', value=fraudes),1,2)
fig.add_trace(go.Scatter(x=mensal.index, y=mensal.values*100, mode='lines+markers', name='Taxa mensal'),2,1)
fig.add_trace(go.Bar(x=canal.index, y=canal.values*100, name='Canal'),2,2)
labels = detalhe['channel'] + ' | ' + detalhe['merchant_category']
fig.add_trace(go.Bar(x=labels, y=detalhe['mean']*100, name='Canal × categoria'),3,1)
fig.update_yaxes(title_text='Taxa de fraude (%)', row=2,col=1)
fig.update_yaxes(title_text='Taxa de fraude (%)', row=2,col=2)
fig.update_yaxes(title_text='Taxa de fraude (%)', row=3,col=1)
fig.update_layout(title='TechPay — Painel de Risco e Fraude', height=1050, showlegend=False)

path = OUT/'dashboard.html'
fig.write_html(path, include_plotlyjs=True)
print(path)
print('Volume financeiro total:', volume)
