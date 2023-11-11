import miceforest as mf
import numpy as np
import pandas as pd
from Common import CommonFunction


def is_cog_imp(sco: int, edu: int):
    if edu <= 4:
        return sco < 17
    elif 4 < edu < 8:
        return sco < 20
    elif edu >= 8:
        return sco < 24


def contain_97(row):
    '''
    Return true if the row contains 97
    '''
    for i in row:
        if i == 97:
            return True
    return False


def more_than_value(row):
    '''
    Return true if the row contains null value more than 0.05
    '''
    cnt = 0
    for i in row:
        if str(i) == 'nan':
            cnt += 1
    return cnt / row.shape[0] >= 0.05


def del_age_less(row):
    '''
    Return true if the age of row less than 45
    '''
    return str(row['Age']) == 'nan' or int(row['Age']) < 45


df = pd.read_csv('/ModifiedData/2018-Cognition.csv', index_col="Individual ID")
demo = pd.read_csv('/ModifiedData/Demographic_Background.csv', index_col='Individual ID')
df = df[[
    "Checking Year",
    "Checking Month",
    "Checking Date",
    "Checking Day",
    "Checking Season",
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
]]

df.sort_index(inplace=True)
demo.sort_index(inplace=True)

# MICE doesn't allow JSON characters
df.columns = [i.replace(":", " ") for i in df.columns]

# Delete row contains integer 97
df = CommonFunction.del_specific(df, contain_97)
df = CommonFunction.del_specific(df, more_than_value)

# Delete null value rows
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

df = CommonFunction.imputation(df)

# Calculate every person's score
df['Sum'] = df.apply(np.sum, axis=1)

CommonFunction.del_df(demo, df)

age = []
for i in demo['Year of Birth']:
    if str(i) != 'nan':
        age.append(2018 - int(i))
    else:
        age.append(np.nan)
df['Age'] = age
df['Education'] = demo['Education']

df = CommonFunction.del_specific(df, del_age_less)

df['Cognitive Impairment'] = np.nan
for j in range(0, df.shape[0]):
    a = is_cog_imp(int(df.loc[df.index.values[j], "Sum"]), int(df.loc[df.index.values[j], "Education"]))
    if a:
        df.loc[df.index.values[j], "Cognitive Impairment"] = 1
    else:
        df.loc[df.index.values[j], "Cognitive Impairment"] = 0

df.to_csv("D:\Personal\Program\MICE\Result1\Cognition.csv")
