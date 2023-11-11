import numpy as np
import pandas as pd

emo_18 = {
    "Bothered by Things": "被事情困扰",
    "Had Trouble Keeping Mind": "记事困难",
    "Felt Depressed": "感到低落",
    "I Felt Everything I Did Was An Effort": "感觉做的一切都是徒劳",
    "I Felt Hopeful about the Future": "对未来感到充满希望",
    "I Felt Fearful": "我感到害怕",
    "My Sleep Was Restless": "睡眠质量不好",
    "I Was Happy": "我过去很开心",
    "I Felt Lonely": "我感到孤独",
    "I Could Not Get on": "我无法聚精会神",
}

df_cog = pd.read_csv("../../PFP/ModifiedData/2018-Cognition.csv", index_col="Individual ID")
df_fra = pd.read_csv('../../PFP/ModifiedData/2018-Frail.csv', index_col='ID')
df_cog.sort_index(inplace=True)
df_cog.sort_index(inplace=True)
