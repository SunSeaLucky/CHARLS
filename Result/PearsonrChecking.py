from scipy.stats import pearsonr
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


cog = pd.read_csv('Cognition.csv', index_col='Individual ID')
fra = pd.read_csv('Frail.csv', index_col='ID')

cog.sort_index(inplace=True)
fra.sort_index(inplace=True)

del_df(cog, fra)

cog.index.rename('ID', inplace=True)

res = pd.concat([fra, cog], axis=1)
res.to_csv('D:\Personal\Program\MICE\Result\Res.csv',encoding='utf-8')
res.to_excel('D:\Personal\Program\MICE\Result\Res.xlsx')

cog.to_csv('Result-11/Cog.csv')
fra.to_csv('Result-11/Fra.csv')

r = pearsonr(cog['Cognitive Impairment'], fra['衰弱'])
print('Pearsonr:', r[0])
