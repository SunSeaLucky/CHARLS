import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import pearsonr

import sys

sys.path.append("Operator")
import Operator

cog_new = pd.read_csv("cog_new.csv", index_col="ID")
cog = pd.read_csv("cog.csv", index_col="ID")


cog_new.rename(columns={"score": "new_score"}, inplace=True)
res = Operator.merge_df(cog_new, cog)

new = res["new_score"]
old = res["score"]


z1 = np.polyfit(new, old, 1)  # 用4次多项式拟合
print(z1)
p1 = np.poly1d(z1)
print(p1)  # 在屏幕上打印拟合多项式

print(pearsonr(new, old))
# plt.figure(figsize=(10, 10), dpi=100)
plt.scatter(new, old)
plt.show()
