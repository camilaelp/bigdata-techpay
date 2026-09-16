# Etapa 3 — Análise dos Achados

A base analisada contém 30.000 transações e 751 registros classificados como fraude, correspondendo a uma **taxa geral de 2,50%**. A análise foi direcionada a dimensões que podem apoiar decisões da área de risco: canal, categoria do estabelecimento, segmento do cliente e horário da transação.

## Análise 1 — Risco por canal

**Finding.** O canal `app` apresentou a maior taxa de fraude, **3,79%**, enquanto `atm` apresentou 1,80%, `web` 1,74% e `pos` 1,42%.

**Insight.** A diferença mostra que o risco não está distribuído de forma homogênea entre os canais. O aplicativo possui uma taxa de fraude aproximadamente 2,7 vezes maior que a observada em POS. Assim, tratar todas as transações com a mesma política de risco pode gerar controles pouco eficientes.

**Ação.** A TechPay poderia aplicar regras de autenticação ou revisão mais sensíveis ao contexto em transações de aplicativo, especialmente quando outros sinais de risco também estiverem presentes. A ação não significa bloquear automaticamente operações no app, mas utilizar o canal como uma dimensão adicional do processo de decisão.

## Análise 2 — Categoria do estabelecimento

**Finding.** A categoria `viagem` apresentou a maior taxa de fraude, **5,32%**. As demais categorias ficaram entre aproximadamente 1,96% e 2,47%.

**Insight.** A categoria de viagem concentra um nível de fraude superior ao observado no conjunto da base. Isso sugere que a natureza da compra ajuda a diferenciar o risco e deve ser considerada junto com as demais características da transação.

**Ação.** Recomenda-se que transações relacionadas a viagem recebam maior atenção no motor de risco, principalmente quando combinadas com canais e horários que também apresentam maior incidência de fraude.

## Análise 3 — Combinação canal × categoria

**Finding.** A combinação `app + viagem` apresentou taxa de fraude de aproximadamente **8,00%**, superior tanto à média do aplicativo quanto à média da categoria de viagem. Foram 99 fraudes em 1.237 transações nessa combinação.

**Insight.** A análise conjunta fornece uma informação que não aparece quando as dimensões são observadas isoladamente. O efeito combinado mostra que a priorização de risco pode ser mais precisa quando considera múltiplas características da transação ao mesmo tempo.

**Ação.** A combinação `app + viagem` pode ser utilizada como sinal de priorização para autenticação reforçada, revisão ou aplicação de um limite mais conservador quando coincidir com outros indicadores de risco.

## Análise 4 — Padrão temporal

**Finding.** As transações realizadas na madrugada, entre 0h e 4h, apresentaram taxa de fraude de aproximadamente **3,47%**, superior aos demais períodos. Quando `app`, `viagem` e `madrugada` aparecem simultaneamente, foram observadas 23 fraudes em 249 transações, uma taxa de aproximadamente **9,24%**.

**Insight.** O horário da transação acrescenta informação à análise de risco. A combinação entre horário, canal e categoria mostra que analisar várias características em conjunto pode identificar contextos com taxas de fraude mais elevadas.

**Ação.** O período da madrugada pode ser utilizado como um sinal adicional de risco, principalmente quando estiver associado a outros fatores, como transações realizadas pelo aplicativo e na categoria de viagem.

## Análise 5 — Segmento do cliente

**Finding.** O segmento `High-Risk` apresentou taxa de fraude de **9,67%**, enquanto `Standard` apresentou 2,93% e `Premium` 0,95%.

**Insight.** O segmento do cliente ajuda a diferenciar os níveis de risco, mas pode ser utilizado em conjunto com características da própria transação, como canal, categoria e horário.

**Ação.** A TechPay pode considerar o segmento como uma das variáveis utilizadas na definição das regras de análise e priorização de transações.

## Síntese gerencial

Os dados indicam que a fraude está concentrada em contextos específicos. O aplicativo, a categoria de viagem, o período da madrugada e o segmento High-Risk aparecem com taxas superiores à média. A principal recomendação é que a TechPay utilize uma política de risco contextual, combinando dimensões da transação em vez de tratar todos os eventos com a mesma regra.
