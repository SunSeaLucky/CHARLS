import miceforest as mf
import numpy as np
import pandas as pd


def del_df(df1, df2):
    drop_rows = []
    for i in df1.index.values:
        flag = True
        for j in df2.index.values:
            if i == j:
                flag = False
        if flag:
            drop_rows.append(i)

    df1.drop(axis=0, index=drop_rows, inplace=True)

    drop_rows.clear()
    for i in df2.index.values:
        flag = True
        for j in df1.index.values:
            if i == j:
                flag = False
        if flag:
            drop_rows.append(i)
    df2.drop(axis=0, index=drop_rows, inplace=True)


def is_cog_imp(sco: int, edu: int):
    if edu <= 4:
        return sco < 17
    elif 4 < edu < 8:
        return sco < 20
    elif edu >= 8:
        return sco < 24


df = pd.read_csv('/ModifiedData/2018-Cognition.csv', index_col="Individual ID")
demo = pd.read_csv('/ModifiedData/Demographic_Background.csv', index_col='Individual ID')
col = [
    "Checking Year",
    "Checking Season",
    "Checking Date",
    "Checking Day",
    "Checking Month",
    "Checking State",
    "Checking County",
    "Checking City",
    "Checking Floor",
    "Checking Address",
    "Repeated Time 1: Ball",
    "Repeated Time 1: Flag",
    "Repeated Time 1: Tree",
    "Specific Result-11 from 100-7",
    "Specific Result-11 from dc014_w4_2-7",
    "Specific Result-11 from dc014_w4_3-7",
    "Specific Result-11 from dc014_w4_4-7",
    "Specific Result-11 from dc014_w4_5-7",
    "Use Pen Paper or Other Instruments for Mathmatics",
    "Delayed Recall: Ball Flag Tree",
    "Delayed Recall: Ball Flag Tree.1",
    "Delayed Recall: Ball Flag Tree.2",
    "Watch Correct",
    "Pencil Correct",
    "Repeat Correct",
    "Read Correct",
    "Hand Correct",
    "Folds Correct",
    "Leg Correct",
    "Sentence Correct",
    "Draw Correct",
]
df = df[col]

df.sort_index(inplace=True)
demo.sort_index(inplace=True)

# MICE doesn't allow JSON characters
df.columns = [i.replace(":", " ") for i in df.columns]

# Delete row contains integer 97
drop_columns = []
for i in range(0, df.shape[0]):
    for j in range(0, df.shape[1]):
        if df.iloc[i, j] == 97:
            drop_columns.append(df.index.values[i])
df.drop(index=drop_columns, inplace=True, axis=0)

# Delete null-value rows
df.dropna(how="all", inplace=True)

for i in range(0, df.shape[0]):
    # Process columns 0~9
    for j in range(0, 10):
        if df.iloc[i, j] == 5:
            df.iloc[i, j] = 0

    # Process columns 10~12
    for j in range(10, 13):
        a = df.iloc[i, j]
        if 1 <= a < 4:
            df.iloc[i, j] = 1
        elif str(a) == 'nan':
            df.iloc[i, j] = 0

    # Process columns contains "Special Result-11"
    for j in range(13, 18):
        a = df.iloc[i, j]
        if str(a) != 'nan':
            if int(a) == 100 - (i - 12) * 7:
                df.iloc[i, j] = 1
            else:
                df.iloc[i, j] = 0

    # Process "Use Paper or Pen"
    if df.iloc[i, 18] == 2:
        df.iloc[i, 18] = 1
    elif df.iloc[i, 18] == 1:
        df.iloc[i, 18] = 0

    for j in range(19, 22):
        a = df.iloc[i, j]
        if 1 <= a < 4:
            df.iloc[i, j] = 1
        elif str(a) == 'nan':
            df.iloc[i, j] = 0

    for j in range(22, 25):
        if df.iloc[i, j] == 5:
            df.iloc[i, j] = 0

    if df.iloc[i, 25] == 5:
        df.iloc[i, 25] = 0
    elif df.iloc[i, 25] == 2:
        df.iloc[i, 25] = 1

    for j in range(26, 31):
        if df.iloc[i, j] == 5:
            df.iloc[i, j] = 0

# Use MICE model to fill missing values
df_amp = mf.ampute_data(df, perc=0.25, random_state=1991)
kernel = mf.ImputationKernel(df_amp, datasets=4, save_all_iterations=True, random_state=1)
kernel.mice(2)
df = kernel.complete_data()

# Calculate every person's score
df['Sum'] = df.apply(np.sum, axis=1)

del_df(demo, df)
age = []
for i in demo['Year of Birth']:
    if str(i) != 'nan':
        age.append(2018 - int(i))
    else:
        age.append(np.nan)
df['Age'] = age
df['Education'] = demo['Education']
drop_rows = []
# print(df.shape, demo.shape)
for i in range(0, df.shape[0]):
    if str(df.loc[df.index.values[i], 'Age']) == 'nan' or int(df.loc[df.index.values[i], 'Age']) < 45:
        drop_rows.append(df.index.values[i])
df.drop(axis=0, index=drop_rows, inplace=True)

# If somebody's score greater than 20, we assume that he doesn't have cognitive impairment
df['Cognitive Impairment'] = np.nan
for j in range(0, df.shape[0]):
    a = is_cog_imp(int(df.loc[df.index.values[j], "Sum"]), int(df.loc[df.index.values[j], "Education"]))
    if a:
        df.loc[df.index.values[j], "Cognitive Impairment"] = 1
    else:
        df.loc[df.index.values[j], "Cognitive Impairment"] = 0

df.to_csv("Result-11\Cognition.csv")
