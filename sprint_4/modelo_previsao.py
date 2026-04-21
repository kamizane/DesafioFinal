import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# -----------------------------
# Carregar dados do SQLite
# -----------------------------
import sqlite3

conn = sqlite3.connect("ecommerce.db")
df = pd.read_sql("SELECT * FROM vendas", conn)

df["Data_Venda"] = pd.to_datetime(df["Data_Venda"])

# -----------------------------
# Faturamento diário (série temporal)
# -----------------------------
df["Faturamento"] = df["Valor_Unitario"] * df["Quantidade"]

serie = (
    df.groupby("Data_Venda")["Faturamento"]
    .sum()
    .reset_index()
    .sort_values("Data_Venda")
)

# -----------------------------
# Transformar data em número (regressão precisa disso)
# -----------------------------
serie["Dia_Num"] = (serie["Data_Venda"] - serie["Data_Venda"].min()).dt.days

X = serie[["Dia_Num"]]
y = serie["Faturamento"]

# -----------------------------
# Treinar modelo
# -----------------------------
modelo = LinearRegression()
modelo.fit(X, y)

# -----------------------------
# Prever próximos 30 dias
# -----------------------------
futuro = np.arange(serie["Dia_Num"].max()+1,
                   serie["Dia_Num"].max()+31).reshape(-1,1)

previsao = modelo.predict(futuro)

datas_futuras = pd.date_range(
    serie["Data_Venda"].max() + pd.Timedelta(days=1),
    periods=30
)

# -----------------------------
# Plot
# -----------------------------
plt.figure(figsize=(12,6))
plt.plot(serie["Data_Venda"], y)
plt.plot(datas_futuras, previsao)
plt.title("Previsão de Faturamento - Regressão Linear")
plt.show()