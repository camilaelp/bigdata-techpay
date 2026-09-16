# Etapa 2 — Execução Big Data

## 1. Ingestão

A base `avaliacao_transactions.csv` foi utilizada como entrada do pipeline. O arquivo contém 30.000 transações da TechPay registradas ao longo de 2025.

A ingestão foi realizada localmente com Python e DuckDB. O arquivo original foi mantido sem alterações, permitindo preservar os dados recebidos antes das etapas de tratamento.

## 2. Camada Raw

Na camada Raw foram definidos os tipos das 12 variáveis da base. Por exemplo, `amount` e `risk_score` foram tratados como valores numéricos, `timestamp` como data e hora e `is_fraud` como variável booleana.

A execução registrou:

**30.000 linhas na camada Raw.**

## 3. Particionamento

O particionamento foi aplicado na camada Silver utilizando `ano` e `mes`, obtidos a partir da variável `timestamp`.

Essa divisão facilita análises por período e permite que, em bases maiores, consultas de determinados meses não precisem percorrer todo o histórico.

## 4. Bronze — qualidade e limpeza

Na camada Bronze foram realizadas verificações de qualidade dos dados. Foram avaliados:

- registros duplicados em `transaction_id`;
- valores ausentes;
- valores de transação não positivos;
- `risk_score` fora do intervalo de 0 a 100;
- `credit_score` fora do intervalo de 300 a 900;
- categorias fora dos valores esperados.

Na base utilizada não foram encontrados registros que precisassem ser removidos por essas regras.

Assim, **30.000 linhas permaneceram na camada Bronze**.

Mesmo sem exclusões nesta execução, essa etapa é importante para evitar que dados inválidos avancem no pipeline caso apareçam em novas bases.

## 5. Silver — enriquecimento

Na camada Silver foram mantidas as variáveis originais e criadas novas informações a partir da data e do valor das transações, como ano, mês, dia, hora, dia da semana, período do dia e faixa de valor.

As variáveis `channel` e `merchant_category` também foram mantidas. Elas permitem analisar as transações considerando o canal utilizado e a categoria do estabelecimento.

Após o processamento, a camada Silver permaneceu com **30.000 linhas**.

## 6. Gold — agregações para análise e BI

Foram criadas duas tabelas Gold.

A primeira reúne informações por `channel` e `merchant_category`, incluindo total de transações, quantidade de fraudes, taxa de fraude, `risk_score` médio e volume financeiro.

Essa tabela resultou em **24 linhas agregadas**.

A segunda tabela organiza os dados por ano, mês, período do dia e segmento, permitindo análises temporais e comparações entre os segmentos de clientes.

Essa tabela resultou em **144 linhas agregadas**.

Essas tabelas deixam os dados preparados para as análises e visualizações da etapa seguinte.

## 7. Evidência da execução

A execução do pipeline apresentou as seguintes contagens:

- Raw: 30.000 linhas;
- Bronze: 30.000 linhas;
- Silver: 30.000 linhas;
- Gold por canal e categoria: 24 linhas;
- Gold temporal e segmento: 144 linhas.

Também foi calculada a taxa de fraude por canal. Entre os resultados observados, o canal `app` apresentou taxa de fraude de **3,79%**, seguido por `atm` (1,80%), `web` (1,74%) e `pos` (1,42%).

O resultado da execução foi registrado em arquivo de texto e em imagem do terminal.

## Respostas às perguntas do enunciado

**Quantas linhas sobreviveram da Bronze em diante?**

30.000 linhas. Nenhuma linha foi descartada pelas regras de qualidade aplicadas.

**A Silver usa `channel` e `merchant_category`?**

Sim. As duas variáveis foram mantidas e podem ser utilizadas para analisar diferenças entre canais e categorias de estabelecimento.

**Que agregações foram colocadas na Gold?**

Foram criadas duas agregações: uma por canal e categoria de estabelecimento e outra por período e segmento. A primeira permite analisar fraude e risco por tipo de transação, enquanto a segunda permite análises temporais e por perfil de cliente.