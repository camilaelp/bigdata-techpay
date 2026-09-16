# Big Data para Negócios — Avaliação Final

Este repositório contém os arquivos desenvolvidos para a avaliação final da disciplina Big Data para Negócios, utilizando a rota sem privilégios administrativos com DuckDB, Python e Plotly.

O projeto utiliza dados de transações da fintech fictícia TechPay para construção de um pipeline de dados e análise de padrões relacionados a risco e fraude.

## Como usar

1. Coloque `avaliacao_transactions.csv` em `data/`.
2. Crie um ambiente Python e instale as dependências de `requirements.txt`.
3. Execute `python avaliacao_final/etapa2_bigdata/pipeline.py`.
4. Execute `python avaliacao_final/etapa3_analise/analises.py`.
5. Execute `python avaliacao_final/etapa3_analise/dashboard.py`.

## Estrutura

- `avaliacao_final/etapa1_arquitetura/`: diagrama da arquitetura e justificativa das escolhas.
- `avaliacao_final/etapa2_bigdata/`: pipeline de dados, explicação das etapas e evidências de execução.
- `avaliacao_final/etapa3_analise/`: análises, relatório de achados, proposta de BI e código do dashboard.
- `requirements.txt`: dependências necessárias para execução do projeto.
- `.gitignore`: definição dos arquivos que não devem ser enviados ao repositório.

## Tecnologias utilizadas

- Python
- DuckDB
- Parquet
- Plotly

## Dashboard

O dashboard apresenta indicadores de risco e fraude da TechPay, incluindo taxa geral de fraude, quantidade de fraudes, tendência mensal, comparação entre canais e detalhamento das combinações de canal e categoria de estabelecimento.
