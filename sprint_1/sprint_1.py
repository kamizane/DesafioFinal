import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import sqlite3

# 1) GERAÇÃO DO DATASET
def gerar_data():
    start = datetime(2023, 1, 1)
    end = datetime(2025, 1, 1)
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

n = 6000  # número de linhas

produtos = [
    "Notebook", "Smartphone", "Fone Bluetooth", "Teclado Mecânico",
    "Mouse Gamer", "Monitor", "Cadeira Gamer", "Webcam",
    "Tablet", "Carregador Portátil"
]

categorias = {
    "Notebook": "Informática",
    "Smartphone": "Telefonia",
    "Fone Bluetooth": "Acessórios",
    "Teclado Mecânico": "Periféricos",
    "Mouse Gamer": "Periféricos",
    "Monitor": "Informática",
    "Cadeira Gamer": "Móveis",
    "Webcam": "Periféricos",
    "Tablet": "Telefonia",
    "Carregador Portátil": "Acessórios"
}

metodos_pagamento = ["Cartão de Crédito", "Cartão de Débito", "Pix", "Boleto"]
cidades = ["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Curitiba",
           "Porto Alegre", "Brasília", "Salvador", "Recife", "Fortaleza", "Campinas"]

data = []

for i in range(n):
    produto = random.choice(produtos)
    quantidade = np.random.randint(1, 6)
    valor_unitario = round(np.random.uniform(20, 5000), 2)

    data.append({
        "ID_Transacao": f"T{i+1:06d}",
        "Data_Venda": gerar_data(),
        "ID_Cliente": f"C{np.random.randint(1,1200):04d}",
        "Cidade_Cliente": random.choice(cidades),
        "Nome_Produto": produto,
        "Categoria_Produto": categorias[produto],
        "Metodo_Pagamento": random.choice(metodos_pagamento),
        "Valor_Unitario": valor_unitario,
        "Quantidade": quantidade,
        "Valor_Total": valor_unitario * quantidade
    })

df = pd.DataFrame(data)

df.loc[5, "Cidade_Cliente"] = None
df.loc[10, "Valor_Unitario"] = None
df = pd.concat([df, df.iloc[[0]]])

# 2) LIMPEZA DE DADOS (ETL)

print("Iniciando limpeza...")

# Remover duplicados
df.drop_duplicates(inplace=True)

# Tratar nulos
df["Cidade_Cliente"].fillna("Desconhecido", inplace=True)
df["Valor_Unitario"].fillna(df["Valor_Unitario"].mean(), inplace=True)

# Recalcular valor total caso tenha sido afetado
df["Valor_Total"] = df["Valor_Unitario"] * df["Quantidade"]


# 3) PADRONIZAÇÃO DE FORMATOS

df["Data_Venda"] = pd.to_datetime(df["Data_Venda"])
df["Valor_Unitario"] = df["Valor_Unitario"].astype(float).round(2)
df["Valor_Total"] = df["Valor_Total"].astype(float).round(2)

# 4) SALVAR CSV TRATADO

df.to_csv("./ecom_data.csv", index=False)
print("CSV gerado com sucesso!")

# 5) CARGA EM BANCO RELACIONAL (SQLite)

conn = sqlite3.connect("./ecom_database.db")
df.to_sql("vendas", conn, if_exists="replace", index=False)
conn.close()

print("Dados carregados no banco SQLite com sucesso!")