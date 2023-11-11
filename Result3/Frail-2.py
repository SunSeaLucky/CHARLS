import pandas as pd
from Common import CommonFunction

# 某条记录缺失率为此数值以上即删除
missing_rate = 0.05
final_file_name = 'Res.csv'

# 2015体检信息表
bio_2015_file_path = 'D:\Personal\Program\MICE\ModifiedData\\2015-biomarkers.dta'
# 2015健康与状态信息表
hsf_2015_file_path = 'D:\Personal\Program\MICE\ModifiedData\\2015-hsf.dta'
# 2015家庭信息
db_2015_file_path = 'D:\Personal\Program\MICE\ModifiedData\\2015-Demographic_Background.csv'
# 2018年的健康状态信息表抽取得来的认知障碍表
cog_2018_file_path = 'D:\Personal\Program\MICE\Result3\Cognition.csv'

bio = pd.read_stata(bio_2015_file_path, index_col='ID', convert_categoricals=False)
hsf = pd.read_stata(hsf_2015_file_path, index_col='ID', convert_categoricals=False)
cog = pd.read_csv(cog_2018_file_path, index_col='Individual ID')
# 读入性别 使用[[]]是为了读入一个DataFrame而非数组
gender = pd.read_csv(db_2015_file_path, index_col='ID')[['ba000_w2_3']]
fra = pd.DataFrame()


def more_than_value(row):
    cnt = 0
    for i in row:
        if str(i) == 'nan':
            cnt += 1
    return cnt / row.shape[0] >= missing_rate


CommonFunction.del_df(bio, hsf)

# ---指标抽取---

# 体重减轻
fra['weight'] = bio['ql002']
fra['height'] = bio['qi002']

# 握力退减
fra['left_hand_m1'] = bio['qc003']
fra['left_hand_m2'] = bio['qc005']
fra['right_hand_m1'] = bio['qc004']
fra['right_hand_m2'] = bio['qc006']

# 步速减慢
fra['walking_speed_time_m1'] = bio['qg002']
fra['walking_speed_time_m2'] = bio['qg003']

# 体力活动水平减弱
fra['do_vigorous_activities_10mins'] = hsf['da051_1_']
fra['do_moderate_physical_effort_10mins'] = hsf['da051_2_']
fra['walking_at_least_10mins'] = hsf['da051_3_']

# 自报疲劳
fra['could_not_get_going'] = hsf['dc018']
fra['felt_everything_i_did_was_an_effort'] = hsf['dc012']

CommonFunction.del_df(cog, fra)
CommonFunction.del_df(fra, gender)

frail_array = []

fra = CommonFunction.del_specific(fra, more_than_value)

# ---对刚刚抽取的指标按照PFP量表进行计算---
for i in fra.index.values:
    score = 0

    # 1.体重减轻
    BMI = float(fra.loc[i, 'weight']) / ((float(fra.loc[i, 'height']) / 100) ** 2)
    score += 1 if BMI <= 18.5 else 0
    # 2.握力退减
    avg = (float(fra.loc[i, 'left_hand_m1']) + float(fra.loc[i, 'left_hand_m2']) + float(
        fra.loc[i, 'right_hand_m1']) + float(fra.loc[i, 'right_hand_m1'])) / 4
    item_score = 0
    # 男性
    if gender.loc[i, 'ba000_w2_3'] == 1:
        if BMI <= 20.6 and avg >= 25.2:
            item_score = 1
        elif 20.6 < BMI <= 23.2 and avg >= 28.5:
            item_score = 1
        elif 23.2 < BMI < 25.9 and avg >= 30:
            item_score = 1
        elif BMI >= 25.9 and avg >= 30:
            item_score = 1
    # 女性
    elif gender.loc[i, 'ba000_w2_3'] == 2:
        if BMI <= 20 and avg >= 15:
            item_score = 1
        elif 20 < BMI <= 22.1 and avg >= 17.5:
            item_score = 1
        elif 22.1 < BMI < 24.8 and avg >= 17.5:
            item_score = 1
        elif BMI >= 24.8 and avg >= 20:
            item_score = 1
    score += item_score

    # 3.步速减慢
    item_score = 0
    # 男性
    if gender.loc[i, 'ba000_w2_3'] == 1:
        if float(fra.loc[i, 'height']) <= 163 and float(fra.loc[i, 'height']) / 2.5 >= 0.45:
            item_score = 1
        elif float(fra.loc[i, 'height']) > 163 and float(fra.loc[i, 'height']) / 2.5 > 0.48:
            item_score = 1
    # 女性
    elif gender.loc[i, 'ba000_w2_3'] == 2:
        if float(fra.loc[i, 'height']) <= 151 and float(fra.loc[i, 'height']) / 2.5 >= 0.36:
            item_score = 1
        elif float(fra.loc[i, 'height']) > 151 and float(fra.loc[i, 'height']) / 2.5 > 0.43:
            item_score = 1

    # 4.体力活动水平减弱
    if fra.loc[i, 'do_vigorous_activities_10mins'] == 1 \
            or fra.loc[i, 'do_moderate_physical_effort_10mins'] == 1 \
            or fra.loc[i, 'walking_at_least_10mins'] == 1:
        score += 1

    # 5.自报疲劳
    if float(fra.loc[i, 'could_not_get_going']) + float(fra.loc[i, 'felt_everything_i_did_was_an_effort']) - 2 >= 3:
        score += 1

    frail_array.append(1 if score >= 3 else 0)

fra['frail'] = frail_array

CommonFunction.del_df(fra, cog)

cog.index.rename('ID', inplace=True)

res = pd.concat([fra, cog], axis=1)
res.to_csv(final_file_name)
