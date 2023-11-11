import miceforest as mf
import numpy as np
import pandas as pd

df = pd.read_csv("../../PFP/ModifiedData/frail-1.csv", index_col="ID")
df.sort_index(inplace=True)

for i in range(0, df.shape[0]):
    dfi = df.loc[df.index.values[i], "自报健康差"]
    if dfi >= 4:
        df.loc[df.index.values[i], "自报健康差"] = 1
    elif dfi < 4:
        df.loc[df.index.values[i], "自报健康差"] = 0

# 从 躯体残疾 到 哮喘
for j in range(1, 18):
    for i in range(0, df.shape[0]):
        dfi = df.iloc[i, j]
        if dfi == 2:
            df.iloc[i, j] = 0

# 从 跑或慢跑 到 管理财务
for j in range(18, 37):
    for i in range(0, df.shape[0]):
        dfi = df.iloc[i, j]
        if dfi == 3 or dfi == 4:
            df.iloc[i, j] = 1
        elif dfi == 1 or dfi == 2:
            df.iloc[i, j] = 0

emo_18 = [
    "被事情困扰",
    "记事困难",
    "感到低落",
    "感觉做的一切都是徒劳",
    "对未来感到充满希望",
    "我感到害怕",
    "睡眠质量不好",
    "我过去很开心",
    "我感到孤独",
    "我无法聚精会神",
]

for j in range(0, df.shape[0]):
    # 从 被事情困扰 到 感觉做的一切都是徒劳
    for i in range(0, 4):
        va = df.loc[df.index.values[j], emo_18[i]]
        if 1 <= va <= 4:
            df.loc[df.index.values[j], emo_18[i]] -= 1
        elif va == 9 or va == 8:
            df.loc[df.index.values[j], emo_18[i]] = np.nan
    # 从 对未来感到充满希望 到 我过去很开心
    for i in range(4, 8):
        va = df.loc[df.index.values[j], emo_18[i]]
        if 1 <= va <= 4:
            df.loc[df.index.values[j], emo_18[i]] = 3 - (va - 1)
        elif va == 9 or va == 8:
            df.loc[df.index.values[j], emo_18[i]] = np.nan
    # 从 我感到孤独 到 我无法聚精会神
    for i in range(8, 10):
        va = df.loc[df.index.values[j], emo_18[i]]
        if 1 <= va <= 4:
            df.loc[df.index.values[j], emo_18[i]] -= 1
        elif va == 9 or va == 8:
            df.loc[df.index.values[j], emo_18[i]] = np.nan

index=[]
for j in df.index.values:
    # 去除数据缺失率大于30%的个体
    # 没有去除之前：18024个
    # 去除之后：16919
    cnt = 0
    for i in range(0, df.shape[1]):
        if str(df.loc[j, df.columns.values[i]]) == 'nan':
            cnt += 1
    if cnt / df.shape[1] >= 0.3:
        index.append(j)
df.drop(index=index, inplace=True, axis=0)

# 模型插补
df_amp = mf.ampute_data(df, perc=0.25, random_state=1991)
kernel = mf.ImputationKernel(df_amp, datasets=4, save_all_iterations=True, random_state=1)

kernel.mice(2)
df = kernel.complete_data()

# 计算是否抑郁
df["抑郁"] = np.nan
for j in range(0, df.shape[0]):
    score = 0
    for i in range(0, 10):
        score += df.loc[df.index.values[j], emo_18[i]]
    if score >= 10:
        df.loc[df.index.values[j], "抑郁"] = 1
    elif score < 10:
        df.loc[df.index.values[j], "抑郁"] = 0

# 删除多余的抑郁指标
df.drop(columns=emo_18, axis=0, inplace=True)

# 计算是否衰弱
df["衰弱"] = np.nan
for j in range(0, df.shape[0]):
    score = 0.0
    for i in range(0, 40):
        if df.iloc[j, i] > 0:
            score += df.iloc[j, i]
    score /= df.shape[1] + 1

    if score >= 0.25:
        df.loc[df.index.values[j], "衰弱"] = 1
    elif score < 0.25:
        df.loc[df.index.values[j], "衰弱"] = 0

df.to_csv('Result-11/Frail.csv')

# 计算衰弱率
cnt = 0
for i in df["衰弱"]:
    if i:
        cnt += 1
print(cnt / df.shape[0])
