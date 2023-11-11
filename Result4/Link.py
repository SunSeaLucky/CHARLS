import pandas as pd
from Common import CommonFunction

cog = pd.read_csv('Cognition.csv', index_col='Individual ID')
fra = pd.read_csv('D:\Personal\Program\MICE\Result4\Frail-2.csv', index_col='ID')

CommonFunction.del_df(cog, fra)

cog.index.rename('ID', inplace=True)

res = pd.concat([fra, cog], axis=1)
res.to_csv('Res.csv')
# res.to_excel('Res.xlsx')
