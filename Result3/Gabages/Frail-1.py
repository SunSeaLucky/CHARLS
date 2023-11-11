import pandas as pd
from Common import CommonFunction

bio_2015_file_path = '/ModifiedData/2015-biomarkers.dta'
hsf_2015_file_path = '/ModifiedData/2015-hsf.dta'

bio = pd.read_stata(bio_2015_file_path, index_col='ID',convert_categoricals=False)
hsf = pd.read_stata(hsf_2015_file_path, index_col='ID',convert_categoricals=False)
CommonFunction.del_df(bio, hsf)

fra = pd.DataFrame()

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

fra.to_csv('Frail-1.csv')
