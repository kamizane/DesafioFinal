# Projeto de Análise de Dados - E-commerce
Este projeto simula um cenário real de análise de dados em um e-commerce, passando por todas as etapas de um pipeline de dados profissional:
ETL → EDA/SQL → Dashboard → Modelo Preditivo → Storytelling
O objetivo não é apenas gerar gráficos, mas extrair insights de negócio a partir dos dados.

##  Objetivo
Analisar dados de vendas de um e-commerce fictício para:


Entender o comportamento de compra dos clientes


Identificar padrões de faturamento ao longo do tempo


Medir retenção de clientes (Churn Rate)


Construir um dashboard interativo para apoio à decisão


Criar um modelo preditivo para previsão de vendas

##  Etapas do Projeto

### Sprint 1 — ETL e Limpeza


Geração de dataset simulado com +5.000 vendas


Tratamento de valores nulos, duplicados e inconsistentes


Padronização de datas e valores monetários


Carga dos dados tratados em banco relacional (SQLite)



### Sprint 2 — EDA e SQL


Estatísticas descritivas com Python


Consultas SQL complexas (JOIN, GROUP BY, Window Functions)


Identificação de outliers


Segmentação de clientes com análise RFM


### Sprint 3 — Dashboard e KPIs
Criação de dashboard interativo com:


Faturamento Total


Ticket Médio


Total de Vendas


Churn Rate


Gráfico de vendas ao longo do tempo (sazonalidade)


Faturamento por cidade


Filtros dinâmicos por cidade e método de pagamento



##  Storytelling — Insights do Negócio
A análise dos dados revelou que o e-commerce apresenta alto volume de vendas e faturamento consistente ao longo do tempo, indicando um negócio saudável em termos de geração de receita.
Entretanto, ao analisar o comportamento dos clientes, foi identificado um ponto crítico: a taxa de churn.
Apesar do bom faturamento, muitos clientes realizam compras pontuais e não retornam, impactando diretamente o potencial de crescimento sustentável do negócio.
Além disso, a análise temporal mostrou padrões de sazonalidade, indicando períodos do mês com maior volume de vendas, informação valiosa para campanhas de marketing e gestão de estoque.
A análise geográfica revelou que algumas cidades concentram maior faturamento, sugerindo oportunidades para campanhas regionais e estratégias logísticas mais eficientes.
O ticket médio elevado indica que os clientes compram volumes consideráveis por transação, reforçando que o problema principal não está no valor gasto, mas sim na retenção de clientes.
Insight principal:

O maior gargalo do negócio não é vender mais, mas reter melhor os clientes existentes.


##  Dashboard Interativo
O dashboard foi desenvolvido para permitir a exploração dinâmica dos dados através de filtros e visualizações claras dos KPIs do negócio.

<img width="560" height="404" alt="image" src="https://github.com/user-attachments/assets/d66e42f9-b03c-4ad0-8cc4-c0adbdb0acab" />


##  Sprint 4 — Modelo Preditivo
Foi implementado um modelo de Regressão Linear para prever o faturamento futuro com base no histórico de vendas ao longo do tempo.
O modelo permite estimar tendências futuras e pode ser utilizado como apoio para planejamento estratégico.

##  Conclusão
Este projeto demonstra um fluxo completo de análise de dados aplicado a um cenário de e-commerce, desde a geração e tratamento dos dados até a extração de insights de negócio e construção de modelo preditivo.
Mais do que gráficos, o projeto entrega inteligência de negócio orientada por dados.

##  Tecnologias Utilizadas


Python


Pandas


SQLite


Matplotlib


Streamlit


Scikit-learn

##  Resultados Principais

A análise dos dados de vendas do e-commerce permitiu identificar padrões relevantes de comportamento do negócio e oportunidades estratégicas.

O faturamento apresentou comportamento relativamente estável ao longo do tempo, com variações mensais que indicam sazonalidade moderada.
O ticket médio elevado sugere que os clientes realizam compras de maior valor, caracterizando um modelo com foco em qualidade de venda, e não volume.
A análise de churn revelou que uma parcela significativa dos clientes não retorna após a primeira compra, indicando um desafio de retenção.
A distribuição de faturamento por cidade mostrou um cenário equilibrado, com algumas regiões apresentando maior relevância, sugerindo oportunidades de ações regionais direcionadas.
O modelo de regressão linear aplicado à série temporal mensal indicou uma tendência de estabilidade com leve queda, sugerindo possível estagnação do crescimento caso não sejam adotadas estratégias de retenção e engajamento.

##  Como Executar o Projeto
pip install -r requirements.txt


## Sprint 1 — ETL
python sprint_1/sprint_1.py

## Sprint 2 — EDA
python sprint_2/sprint2.py

## Sprint 2 — SQL
python sprint_2/sprint2_sql.py

## Sprint 3 — Dashboard
streamlit run sprint_3/dashboard.py

## Sprint 4 — Modelo
python sprint_4/modelo_previsao.py
