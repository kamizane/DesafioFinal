import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

##
st.set_page_config(
    page_title="Dashboard E-commerce",
    page_icon="📊",
    layout="wide"
)


@st.cache_data
def carregar_dados():
    conn = sqlite3.connect("./ecom_database.db")
    df = pd.read_sql("SELECT * FROM vendas", conn)
    conn.close()

    df["Data_Venda"] = pd.to_datetime(df["Data_Venda"], errors="coerce")
    df = df.dropna(subset=["Data_Venda"])

    # Remover NaN das colunas usadas nos filtros e gráficos
    df["Cidade_Cliente"] = df["Cidade_Cliente"].fillna("Não informado")
    df["Metodo_Pagamento"] = df["Metodo_Pagamento"].fillna("Não informado")
    df["Categoria_Produto"] = df["Categoria_Produto"].fillna("Não informado")

    # Garantir tipos numéricos
    df["Valor_Total"] = pd.to_numeric(df["Valor_Total"], errors="coerce")
    df["Valor_Unitario"] = pd.to_numeric(df["Valor_Unitario"], errors="coerce")
    df["Quantidade"] = pd.to_numeric(df["Quantidade"], errors="coerce")

    df = df.dropna(subset=["Valor_Total", "Valor_Unitario", "Quantidade"])

    return df


def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def calcular_churn(df_base, dias_churn=90):
    if df_base.empty:
        return 0

    snapshot_date = df_base["Data_Venda"].max()

    ultima_compra = (
        df_base.groupby("ID_Cliente")["Data_Venda"]
        .max()
        .reset_index()
    )

    ultima_compra["Dias_Sem_Comprar"] = (
        snapshot_date - ultima_compra["Data_Venda"]
    ).dt.days

    clientes_churn = ultima_compra[
        ultima_compra["Dias_Sem_Comprar"] > dias_churn
    ]

    return (len(clientes_churn) / len(ultima_compra)) * 100



df_original = carregar_dados()

#filtros
st.sidebar.title("🔎 Filtros")

data_min = df_original["Data_Venda"].min().date()
data_max = df_original["Data_Venda"].max().date()

if "periodo" not in st.session_state:
    st.session_state["periodo"] = (data_min, data_max)

if "cidades" not in st.session_state:
    st.session_state["cidades"] = []

if "metodos" not in st.session_state:
    st.session_state["metodos"] = []

if "categorias" not in st.session_state:
    st.session_state["categorias"] = []

if st.sidebar.button("🔄 Limpar filtros", use_container_width=True):
    st.session_state["periodo"] = (data_min, data_max)
    st.session_state["cidades"] = []
    st.session_state["metodos"] = []
    st.session_state["categorias"] = []
    st.rerun()

cidades_opcoes = sorted(df_original["Cidade_Cliente"].dropna().unique())
metodos_opcoes = sorted(df_original["Metodo_Pagamento"].dropna().unique())
categorias_opcoes = sorted(df_original["Categoria_Produto"].dropna().unique())

periodo = st.sidebar.date_input(
    "Período de venda",
    min_value=data_min,
    max_value=data_max,
    key="periodo"
)

cidades = st.sidebar.multiselect(
    "Cidade do Cliente",
    options=cidades_opcoes,
    placeholder="Todas as cidades",
    key="cidades"
)

metodos = st.sidebar.multiselect(
    "Método de Pagamento",
    options=metodos_opcoes,
    placeholder="Todos os métodos",
    key="metodos"
)

categorias = st.sidebar.multiselect(
    "Categoria do Produto",
    options=categorias_opcoes,
    placeholder="Todas as categorias",
    key="categorias"
)

st.sidebar.caption(
    "Filtros vazios significam que todos os valores serão considerados."
)

##filtros
df = df_original.copy()

if isinstance(periodo, tuple) and len(periodo) == 2:
    inicio, fim = periodo
    df = df[
        (df["Data_Venda"].dt.date >= inicio) &
        (df["Data_Venda"].dt.date <= fim)
    ]

if cidades:
    df = df[df["Cidade_Cliente"].isin(cidades)]

if metodos:
    df = df[df["Metodo_Pagamento"].isin(metodos)]

if categorias:
    df = df[df["Categoria_Produto"].isin(categorias)]

##header
st.title("📊 Dashboard de Vendas - E-commerce")
st.markdown(
    "Acompanhe os principais indicadores de vendas, retenção de clientes, "
    "comportamento temporal e desempenho por cidade."
)

st.divider()

##
if df.empty:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")
    st.stop()

faturamento = df["Valor_Total"].sum()
ticket_medio = df["Valor_Total"].mean()
total_vendas = len(df)
clientes_unicos = df["ID_Cliente"].nunique()
churn_rate = calcular_churn(df)

col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])

col1.metric("💰 Faturamento", formatar_moeda(faturamento))
col2.metric("🧾 Ticket Médio", formatar_moeda(ticket_medio))
col3.metric("📦 Vendas", f"{total_vendas:,}".replace(",", "."))
col4.metric("👥 Clientes", f"{clientes_unicos:,}".replace(",", "."))
col5.metric("🚨 Churn Rate", f"{churn_rate:.2f}%")

st.divider()

##graficos
col_graf1, col_graf2 = st.columns([2, 1])

with col_graf1:
    st.subheader("📈 Faturamento Mensal")

    vendas_mes = (
        df.groupby(df["Data_Venda"].dt.to_period("M"))["Valor_Total"]
        .sum()
        .reset_index()
    )

    vendas_mes["Data_Venda"] = vendas_mes["Data_Venda"].astype(str)

    fig, ax = plt.subplots(figsize=(10, 4.2))
    ax.plot(
        vendas_mes["Data_Venda"],
        vendas_mes["Valor_Total"],
        marker="o",
        linewidth=2
    )

    ax.set_xlabel("Ano-Mês")
    ax.set_ylabel("Faturamento")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(True, alpha=0.3)

    st.pyplot(fig, use_container_width=True)

with col_graf2:
    st.subheader("💳 Pagamento")

    pagamento_vendas = (
        df.groupby("Metodo_Pagamento")["Valor_Total"]
        .sum()
        .sort_values(ascending=True)
    )

    fig_pag, ax_pag = plt.subplots(figsize=(6, 4.2))
    ax_pag.barh(pagamento_vendas.index, pagamento_vendas.values)
    ax_pag.set_xlabel("Faturamento")
    ax_pag.grid(True, axis="x", alpha=0.3)

    st.pyplot(fig_pag, use_container_width=True)

##graficos
col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    st.subheader("🏙️ Top 10 Cidades")

    cidade_vendas = (
        df.groupby("Cidade_Cliente")["Valor_Total"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values(ascending=True)
    )

    fig2, ax2 = plt.subplots(figsize=(8, 4.2))
    ax2.barh(cidade_vendas.index, cidade_vendas.values)
    ax2.set_xlabel("Faturamento")
    ax2.grid(True, axis="x", alpha=0.3)

    st.pyplot(fig2, use_container_width=True)

with col_graf4:
    st.subheader("🛍️ Top 10 Categorias")

    categoria_vendas = (
        df.groupby("Categoria_Produto")["Valor_Total"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .sort_values(ascending=True)
    )

    fig3, ax3 = plt.subplots(figsize=(8, 4.2))
    ax3.barh(categoria_vendas.index, categoria_vendas.values)
    ax3.set_xlabel("Faturamento")
    ax3.grid(True, axis="x", alpha=0.3)

    st.pyplot(fig3, use_container_width=True)

st.divider()

##tabela
st.subheader("📋 Dados Filtrados")

col_info1, col_info2 = st.columns([1, 3])

with col_info1:
    st.info(f"Registros filtrados: **{len(df)}**")

with col_info2:
    st.caption("Amostra das 20 primeiras linhas após aplicação dos filtros.")

st.dataframe(
    df.head(20),
    use_container_width=True,
    hide_index=True
)
