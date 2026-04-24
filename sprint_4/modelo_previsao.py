import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import sqlite3


conn = sqlite3.connect("./ecom_database.db")
df = pd.read_sql("SELECT * FROM vendas", conn)
conn.close()

df["Data_Venda"] = pd.to_datetime(df["Data_Venda"])


df["Faturamento"] = df["Valor_Unitario"] * df["Quantidade"]
df["AnoMes"] = df["Data_Venda"].dt.to_period("M")

serie = (
    df.groupby("AnoMes")["Faturamento"]
    .sum()
    .reset_index()
)

serie["AnoMes"] = serie["AnoMes"].astype(str)
serie["t"] = range(len(serie))

serie = serie[serie["Faturamento"] > 100000]

X = serie[["t"]]
y = serie["Faturamento"]

modelo = LinearRegression()
modelo.fit(X, y)


futuro = np.arange(serie["t"].max() + 1, serie["t"].max() + 4).reshape(-1, 1)
previsao = modelo.predict(futuro)

ultimo_periodo = pd.Period(serie["AnoMes"].iloc[-1], freq="M")
datas_futuras = pd.period_range(
    start=ultimo_periodo + 1,
    periods=3,
    freq="M"
).astype(str)


plt.figure(figsize=(12, 6))
plt.plot(serie["AnoMes"], y, marker="o", label="Faturamento Real")
plt.plot(datas_futuras, previsao, marker="o", linestyle="--", label="Previsão")

plt.xticks(rotation=45)
plt.title("Previsão de Faturamento Mensal - Regressão Linear")
plt.xlabel("Ano-Mês")
plt.ylabel("Faturamento")
plt.legend()
plt.tight_layout()
plt.show()