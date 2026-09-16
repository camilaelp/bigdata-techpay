# Etapa 1 — Arquitetura de Big Data

## Visão geral da solução

A arquitetura proposta para a TechPay foi organizada em etapas, desde a entrada dos dados das transações até a apresentação das informações em um dashboard. As transações são realizadas pelos canais app, web, POS e ATM e, para esta atividade, estão disponíveis no arquivo `avaliacao_transactions.csv`.

Foi escolhida a rota sem privilégios administrativos apresentada na disciplina, utilizando ferramentas que podem ser executadas localmente. O objetivo é manter os dados organizados em diferentes camadas, separando os dados originais dos dados tratados e daqueles preparados para análise.

O fluxo proposto segue a sequência:

**Origem dos dados → Ingestão → Raw → Bronze → Silver → Gold → Dashboard**

O arquivo CSV recebido é mantido como fonte original dos dados. Após as etapas de tratamento, os dados podem ser armazenados em formato Parquet. Esse formato é adequado para análises porque organiza os dados de maneira mais eficiente para consultas e preserva melhor os tipos das variáveis quando comparado ao CSV.

## Escolha da ferramenta de ingestão

Para esta atividade, foi escolhida uma solução que pode ser executada localmente, utilizando Python e DuckDB. Essa escolha permite realizar a ingestão e o tratamento dos dados sem depender da instalação e manutenção de um cluster.

Como a base da avaliação possui 30 mil registros e foi disponibilizada em um arquivo CSV, o processamento em lote (batch) é suficiente para o objetivo do trabalho.

Uma alternativa seria utilizar HDFS e Hive em um cluster, que também é uma das opções apresentadas na disciplina. Essa alternativa seria mais adequada em situações com volumes muito maiores de dados ou com várias fontes sendo processadas em um ambiente distribuído. Para esta atividade, a solução local é suficiente para executar e demonstrar todas as etapas do pipeline.

## Estratégia de particionamento

A estratégia proposta é organizar os dados da camada Silver por `ano` e `mes`, informações obtidas a partir da variável `timestamp`.

Essa escolha foi feita porque várias análises de risco e fraude podem ser realizadas por período. Por exemplo, a empresa pode querer comparar a taxa de fraude entre diferentes meses ou acompanhar sua evolução ao longo do ano.

Em uma base com um histórico maior, essa organização permite consultar apenas os períodos necessários, sem precisar percorrer todos os dados disponíveis.

Foi escolhida a divisão mensal, em vez da diária, porque a base atual possui 30 mil registros e não existe necessidade de criar muitas divisões pequenas. Caso o volume de dados aumentasse bastante e as consultas passassem a ser feitas principalmente por dia, essa estratégia poderia ser modificada.

## Camadas do pipeline

A camada **Raw** mantém os dados da forma como foram recebidos, preservando a fonte original.

Na camada **Bronze**, são realizadas verificações de qualidade dos dados, como identificação de registros duplicados, valores ausentes, tipos incorretos e valores que não estejam de acordo com o esperado para cada variável.

Na camada **Silver**, os dados já tratados são preparados para facilitar as análises. Nessa etapa, podem ser criadas novas informações a partir das variáveis existentes, como hora da transação, dia da semana, mês, período do dia e faixa de valor.

As variáveis `channel` e `merchant_category` também são mantidas na Silver porque permitem analisar se existem diferenças no comportamento das transações e das fraudes entre os canais e as diferentes categorias de estabelecimento.

Por fim, a camada **Gold** reúne informações agregadas e preparadas para as análises de negócio e para o dashboard. A proposta é criar agregações que permitam analisar fraude e risco por canal, categoria de estabelecimento, período e segmento de clientes.

Dessa forma, o dashboard pode utilizar informações que já foram organizadas e resumidas anteriormente, sem precisar refazer todo o processamento da base a cada consulta.

## Pontos de falha e aumento do volume de dados

A solução proposta é adequada para a base utilizada nesta atividade. Entretanto, se o volume e a complexidade dos dados aumentassem significativamente, principalmente com crescimento contínuo do histórico, várias fontes de dados e vários usuários acessando as informações ao mesmo tempo, uma solução baseada em uma única máquina poderia apresentar limitações.

Nesse cenário, uma alternativa seria utilizar armazenamento distribuído ou armazenamento em nuvem e ferramentas capazes de dividir o processamento entre diferentes recursos computacionais, como o Spark.

Outro ponto de atenção seria a quantidade de arquivos e partições geradas ao longo do tempo. Por isso, seria necessário acompanhar a organização desses arquivos, além de registrar as execuções do pipeline e realizar verificações de qualidade dos dados.

Também seria importante permitir que uma etapa pudesse ser executada novamente com segurança caso ocorresse alguma falha durante o processamento.

## Mudança para detecção de fraude em tempo real

A arquitetura utilizada nesta atividade trabalha em **batch**, ou seja, os dados são recebidos e processados em lotes.

Se a TechPay precisasse detectar fraudes em tempo real, seria necessário modificar principalmente a forma de entrada e processamento das transações. Em vez de esperar a formação de um arquivo para iniciar o processamento, cada nova transação poderia ser enviada para um sistema de eventos, como Kafka, e analisada assim que fosse realizada.

Nesse caso, uma ferramenta de processamento de dados em tempo real poderia avaliar o risco da transação antes da decisão final de aprovação ou bloqueio.

O processamento em batch ainda poderia continuar existindo para manter o histórico das transações, realizar análises gerenciais, gerar indicadores e auxiliar no desenvolvimento de modelos de risco. A principal diferença seria a criação de um fluxo adicional de baixa latência para as decisões que precisam acontecer imediatamente.
