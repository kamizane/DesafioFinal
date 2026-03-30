import sqlite3
import pandas as pd

# Conectar ao banco
conn = sqlite3.connect("./ecom_database.db")

def executar_query(titulo, query):
    print(f"\n--- {titulo} ---")
    df = pd.read_sql(query, conn)
    print(df)

# 1) Vendas por cidade
executar_query(
    "Vendas por Cidade",
    """
    SELECT Cidade_Cliente,
           SUM(Valor_Total) AS Total_Vendas
    FROM vendas
    GROUP BY Cidade_Cliente
    ORDER BY Total_Vendas DESC;
    """
)

# 2) Top 5 clientes que mais gastaram
executar_query(
    "Top 5 Clientes",
    """
    SELECT ID_Cliente,
           SUM(Valor_Total) AS Total_Gasto
    FROM vendas
    GROUP BY ID_Cliente
    ORDER BY Total_Gasto DESC
    LIMIT 5;
    """
)

# 3) Ranking de clientes (Window Function)
executar_query(
    "Ranking de Clientes",
    """
    SELECT ID_Cliente,
           SUM(Valor_Total) AS Total_Gasto,
           RANK() OVER (ORDER BY SUM(Valor_Total) DESC) AS Ranking
    FROM vendas
    GROUP BY ID_Cliente;
    """
)

# 4) Vendas por mês (análise temporal)
executar_query(
    "Vendas por Mês",
    """
    SELECT strftime('%Y-%m', Data_Venda) AS Ano_Mes,
           SUM(Valor_Total) AS Total_Vendas
    FROM vendas
    GROUP BY Ano_Mes
    ORDER BY Ano_Mes;
    """
)

conn.close()