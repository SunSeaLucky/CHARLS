import pandas as pd

df_cog = pd.read_csv("Result/cog-11.csv", index_col="ID", dtype={"ID": str})
df_fra = pd.read_csv("Result/fra-11.csv", index_col="ID", dtype={"ID": str})

df_cog.index = df_cog.index.str[:-1] + "0" + df_cog.index.str[-1]
df_fra.index = df_fra.index.str[:-1] + "0" + df_fra.index.str[-1]

df_cog.to_csv("Result/cog-11.csv")
df_fra.to_csv("Result/fra-11.csv")
