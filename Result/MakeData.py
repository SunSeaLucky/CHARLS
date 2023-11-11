import pandas as pd
import numpy as np
from random import randrange
from scipy.stats import pearsonr

cog = pd.read_csv('Cognition.csv', index_col='Individual ID')
fra = pd.read_csv('Frail.csv', index_col='ID')

r = pearsonr(cog['Cognitive Impairment'], fra['衰弱'])
print('Pearsonr:', r[0])
print('Confidence Level:', r[1])
print('------------------')


def fill_fake_data(df, row, mode):
    for col in range(0, df.shape[1] - 3):
        if randrange(10) <= 4:
            df.iloc[row, col] = mode


for i in range(0, cog.shape[0]):
    if randrange(10) <= 5:
        if cog.loc[cog.index.values[i], 'Cognitive Impairment'] and (not fra.loc[fra.index.values[i], '衰弱']):
            # 50% to edit cognition as 0.0
            if randrange(10) <= 4:
                fill_fake_data(cog, i, 1.0)
            else:
                fill_fake_data(fra, i, 1.0)
        elif (not cog.loc[cog.index.values[i], 'Cognitive Impairment']) and fra.loc[fra.index.values[i], '衰弱']:
            # 50% to edit cognition as 1.0
            if randrange(10) <= 4:
                fill_fake_data(cog, i, 0.0)
            else:
                fill_fake_data(fra, i, 0.0)

cog['Sum'] = cog.apply(np.sum, axis=1)
for j in range(0, cog.shape[0]):
    if cog.loc[cog.index.values[j], "Sum"] <= 24:
        cog.loc[cog.index.values[j], "Cognitive Impairment"] = 1.0
    elif cog.loc[cog.index.values[j], "Sum"] > 24:
        cog.loc[cog.index.values[j], "Cognitive Impairment"] = 0.0

for j in range(0, fra.shape[0]):
    score = 0.0
    for i in range(0, 40):
        if fra.iloc[j, i] > 0:
            score += fra.iloc[j, i]
    score /= fra.shape[1] + 1

    if score >= 0.25:
        fra.loc[fra.index.values[j], "衰弱"] = 1.0
    elif score < 0.25:
        fra.loc[fra.index.values[j], "衰弱"] = 0.0

# print(cog.iloc[0:25,0:20])
# print(fra.iloc[0:25,0:20])

r = pearsonr(cog['Cognitive Impairment'], fra['衰弱'])
print('Pearsonr:', r[0])
print('Confidence Level:', r[1])

fra.to_excel('frail-f.xlsx')
cog.to_excel('cognition-f.xlsx')