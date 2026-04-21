import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

##### Para executar esse dashboard, rode o comando: streamlit run dashboard.py

st.set_page_config(layout="wide")


# Conexão com banco

conn = sqlite3.connect("./ecom_database.db")
df = pd.read_sql("SELECT * FROM vendas", conn)
conn.close()

df["Data_Venda"] = pd.to_datetime(df["Data_Venda"])

# CÁLCULO DE CHURN RATE
snapshot_date = df["Data_Venda"].max()

ultima_compra = df.groupby("ID_Cliente")["Data_Venda"].max().reset_index()
ultima_compra["Dias_Sem_Comprar"] = (snapshot_date - ultima_compra["Data_Venda"]).dt.days

clientes_churn = ultima_compra[ultima_compra["Dias_Sem_Comprar"] > 90]
churn_rate = (len(clientes_churn) / ultima_compra.shape[0]) * 100

# FILTROS
st.sidebar.title("Filtros")

cidades = st.sidebar.multiselect(
    "Cidade",
    options=df["Cidade_Cliente"].unique(),
    default=df["Cidade_Cliente"].unique()
)

metodos = st.sidebar.multiselect(
    "Método de Pagamento",
    options=df["Metodo_Pagamento"].unique(),
    default=df["Metodo_Pagamento"].unique()
)

df = df[
    (df["Cidade_Cliente"].isin(cidades)) &
    (df["Metodo_Pagamento"].isin(metodos))
]


# KPIs
faturamento = df["Valor_Total"].sum()
ticket_medio = df["Valor_Total"].mean()
total_vendas = len(df)
col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Faturamento Total", f"R$ {faturamento:,.2f}")
col2.metric("🧾 Ticket Médio", f"R$ {ticket_medio:,.2f}")
col3.metric("📦 Total de Vendas", total_vendas)
col4.metric("🚨 Churn Rate", f"{churn_rate:.2f}%")

# SÉRIE TEMPORAL
st.subheader("Vendas ao longo do tempo")

vendas_mes = df.groupby(df["Data_Venda"].dt.to_period("M"))["Valor_Total"].sum()
vendas_mes.index = vendas_mes.index.astype(str)

fig, ax = plt.subplots()
ax.plot(vendas_mes.index, vendas_mes.values)
ax.set_xlabel("Ano-Mês")
ax.set_ylabel("Faturamento")
plt.xticks(rotation=45)

st.pyplot(fig)

# Vendas por cidade
st.subheader("Faturamento por Cidade")

cidade_vendas = df.groupby("Cidade_Cliente")["Valor_Total"].sum()

fig2, ax2 = plt.subplots()
ax2.bar(cidade_vendas.index, cidade_vendas.values)
plt.xticks(rotation=45)

st.pyplot(fig2)