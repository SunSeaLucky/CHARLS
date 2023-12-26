import pandas as pd

df = pd.read_csv("Result/FinalResult (Contains 6 tables above).csv", index_col="index")

# Have cognitive impairment in just 2015
df_cog_only_15_array = []

for index, row in df.fillna(-1).iterrows():
    # print(row[4], row[6], row[8], index)
    if int(row[4]) == 1 and int(row[6]) != 1 and int(row[8]) != 1:
        df_cog_only_15_array.append(index)
# print(df_cog_only_15_array)
df.loc[df_cog_only_15_array].to_csv("Result/cog_only_15.csv")

# Never have cognitive impairment in all three years
df_cog_never_array = []

for index, row in df.fillna(-1).iterrows():
    if int(row[4]) != 1 and int(row[6]) != 1 and int(row[8]) != 1:
        df_cog_never_array.append(index)

df.loc[df_cog_never_array].to_csv("Result/cog_never.csv")
