import sqlite3
import pandas as pd

conn = sqlite3.connect("./ecom_database.db")

df = pd.read_sql("SELECT * FROM vendas", conn)

print(df.describe())
print(df["Metodo_Pagamento"].value_counts())
print(df["Cidade_Cliente"].value_counts())
print("Ticket médio:", df["Valor_Total"].mean())
print("Maior venda:", df["Valor_Total"].max())
print("Menor venda:", df["Valor_Total"].min())

print("----------------------------------------------------------")

Q1 = df["Valor_Total"].quantile(0.25)
Q3 = df["Valor_Total"].quantile(0.75)
IQR = Q3 - Q1

outliers = df[(df["Valor_Total"] < Q1 - 1.5 * IQR) |
              (df["Valor_Total"] > Q3 + 1.5 * IQR)]

print("Quantidade de outliers:", len(outliers))

print(df[["Valor_Unitario", "Quantidade", "Valor_Total"]].corr())

print("----------------------------------------------------------")

from datetime import datetime

df["Data_Venda"] = pd.to_datetime(df["Data_Venda"])

snapshot_date = df["Data_Venda"].max() + pd.Timedelta(days=1)

rfm = df.groupby("ID_Cliente").agg({
    "Data_Venda": lambda x: (snapshot_date - x.max()).days,
    "ID_Transacao": "count",
    "Valor_Total": "sum"
})

rfm.columns = ["Recencia", "Frequencia", "Monetario"]

print(rfm.head())

rfm["R_Score"] = pd.qcut(rfm["Recencia"], 4, labels=[4,3,2,1])
rfm["F_Score"] = pd.qcut(rfm["Frequencia"].rank(method="first"), 4, labels=[1,2,3,4])
rfm["M_Score"] = pd.qcut(rfm["Monetario"], 4, labels=[1,2,3,4])

rfm["RFM_Score"] = rfm["R_Score"].astype(str) + \
                   rfm["F_Score"].astype(str) + \
                   rfm["M_Score"].astype(str)

print(rfm.sort_values("RFM_Score", ascending=False).head())