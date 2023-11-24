import miceforest as mf
import pandas as pd


def is_cog_imp(sco: int, edu: int):
    """
    :param sco:
    :param edu:
    :return: 是不是认知障碍
    """
    # k = 1.347
    # b = -1.293
    k = 1
    b = 0
    # print("edu: " + str(edu) + ", sco: " + str(sco))
    if edu <= 4:
        return sco < 21 * k + b
    elif 4 < edu < 8:
        return sco < 23 * k + b
    elif edu >= 8:
        return sco < 24 * k + b


def get_duplicates_and_sort(df1, df2):
    """
    :param df1:
    :param df2:
    :return: DataFrame 返回两个表的共有部分并排序
    """
    df1.sort_index(inplace=True)
    df2.sort_index(inplace=True)

    same_rows = []

    for i in df1.index.values:
        for j in df2.index.values:
            if int(i) < int(j):
                break
            elif i == j:
                same_rows.append(i)
                break

    df1.drop(index=df1.index.difference(same_rows), inplace=True)
    df2.drop(index=df2.index.difference(same_rows), inplace=True)


def merge_df(df1, df2):
    """
    :param df1:
    :param df2:
    :return: 连接两个表
    """
    get_duplicates_and_sort(df1, df2)
    df1.index.rename("ID", inplace=True)
    df2.index.rename("ID", inplace=True)
    return pd.concat([df1, df2], axis=1)


class DataOperator:
    def __init__(self, year: int, scale: str, source_df):
        self.year = year
        self.scale = scale
        self.source_df = source_df
        self.df = pd.DataFrame()
        self.indicators = {
            2018: {
                "PFP": [
                    "ql002",
                    "qi002",
                    "qc003",
                    "qc004",
                    "qc005",
                    "qc006",
                    "qg002",
                    "qg003",
                    "da051_1_",
                    "da051_2_",
                    "da051_3_",
                    "dc018",
                    "dc012",
                    "rgender",
                ],
                "MMSE": [
                    "dc001_w4",
                    "dc002_w4",
                    "dc003_w4",
                    "dc005_w4",
                    "dc006_w4",
                    "dc007_w4",
                    "dc008_w4",
                    "dc009_w4",
                    "dc010_w4",
                    "dc012_w4",
                    "dc013_w4_1_s1",
                    "dc013_w4_1_s2",
                    "dc013_w4_1_s3",
                    "dc014_w4_1_1",
                    "dc014_w4_2_1",
                    "dc014_w4_3_1",
                    "dc014_w4_4_1",
                    "dc014_w4_5_1",
                    "dc015_w4_s1",
                    "dc015_w4_s2",
                    "dc015_w4_s3",
                    "dc016_w4",
                    "dc017_w4",
                    "dc018_w4",
                    "dc019_w4",
                    "dc020_w4",
                    "dc021_w4",
                    "dc022_w4",
                    "dc023_w4",
                    "dc024_w4",
                    "bd001_w2_4",  # highest_level_of_education_attained
                ],
                "new_MMSE": [
                    "dc001_w4",
                    "dc002_w4",
                    "dc003_w4",
                    "dc005_w4",
                    "dc006_w4",
                    "dc004",
                    "dc028_w4_s1",
                    "dc028_w4_s2",
                    "dc028_w4_s3",
                    "dc028_w4_s4",
                    "dc028_w4_s5",
                    "dc028_w4_s6",
                    "dc028_w4_s7",
                    "dc028_w4_s8",
                    "dc028_w4_s9",
                    "dc014_w4_1_1",
                    "dc014_w4_2_1",
                    "dc014_w4_3_1",
                    "dc014_w4_4_1",
                    "dc014_w4_5_1",
                    "da007_1_",
                    "da007_2_",
                    "da007_3_",
                    "da007_4_",
                    "da007_5_",
                    "da007_6_",
                    "da007_7_",
                    "da007_8_",
                    "da007_9_",
                    "da007_10_",
                    "da007_11_",
                    "da007_13_",
                    "da007_14_",
                    "da008_1_",
                    "da008_5_",
                    "da008_11_",
                    "da013_s1",
                    "da013_s2",
                    "da013_s3",
                    "da013_s4",
                    "da013_s5",
                    "da016_s1",
                    "da016_s2",
                    "da016_s3",
                    "da016_s4",
                    "da016_s5",
                    "da016_s6",
                    "da018_w4_s1",
                    "da018_w4_s2",
                    "da018_w4_s3",
                    "da018_w4_s4",
                    "da018_w4_s5",
                    "da018_w4_s6",
                    "da019_w4_s1",
                    "da019_w4_s2",
                    "da019_w4_s3",
                    "da019_w4_s4",
                    "da019_w4_s5",
                    "da019_w4_s6",
                    "da005_5_",
                    "da007_12_",
                    "da017_s2",
                    "da056_s1",
                    "da056_s2",
                    "db009",
                    "db007",
                    "da032",
                    "da033",
                    "da034",
                    "da056_w3_s1",
                    "da056_w3_s2",
                    "da056_w3_s3",
                    "da056_w3_s4",
                    "db006",
                    "dc025_w4",
                    "bd001_w2_4",
                    "ba004_w3_1",
                    "ba000_w2_3",
                ],
            },
            2015: {
                "PFP": [
                    "ql002",
                    "qi002",
                    "qc003",
                    "qc004",
                    "qc005",
                    "qc006",
                    "qg002",
                    "qg003",
                    "da051_1_",
                    "da051_2_",
                    "da051_3_",
                    "dc018",
                    "dc012",
                    "ba000_w2_3",
                ],
                "MMSE": [
                    "dc001s1",
                    "dc001s2",
                    "dc001s3",
                    "dc002",
                    "dc003",
                    "dc004",
                    "dc027s1",
                    "dc027s2",
                    "dc027s3",
                    "dc027s4",
                    "dc027s5",
                    "dc027s6",
                    "dc027s7",
                    "dc027s8",
                    "dc027s9",
                    "dc019",
                    "dc020",
                    "dc021",
                    "dc022",
                    "dc023",
                    "da007_1_",
                    "da007_2_",
                    "da007_3_",
                    "da007_4_",
                    "da007_5_",
                    "da007_6_",
                    "da007_7_",
                    "da007_8_",
                    "da007_9_",
                    "da007_10_",
                    "da007_11_",
                    "da007_12_",
                    "da007_13_",
                    "da007_14_",
                    "da008_1_",
                    "da008_5_",
                    "da008_11_",
                    "da013s1",
                    "da013s2",
                    "da013s3",
                    "da013s4",
                    "da013s5",
                    "da016s1",
                    "da016s2",
                    "da016s3",
                    "da016s4",
                    "da016s5",
                    "da016s6",
                    "da018s1",
                    "da018s2",
                    "da018s3",
                    "da018s4",
                    "da018s5",
                    "da018s6",
                    "da019s1",
                    "da019s2",
                    "da019s3",
                    "da019s4",
                    "da019s5",
                    "da019s6",
                    "da005_5_",
                    "da007_12_",
                    "da017",
                    "da056s1",
                    "da056s2",
                    "db009",
                    "db007",
                    "db006",
                    "da032",
                    "da033",
                    "da034",
                    "da056_w3s1",
                    "da056_w3s2",
                    "da056_w3s3",
                    "da056_w3s4",
                    "db006",
                    "dc025",
                    "bd001",
                    "ba004",
                    "ba000_w2_3",
                ],
            },
            2013: {
                "PFP": [
                    "ql002",
                    "qi002",
                    "qc003",
                    "qc004",
                    "qc005",
                    "qc006",
                    "qg002",
                    "qg003",
                    "da051_1_",
                    "da051_2_",
                    "da051_3_",
                    "dc018",
                    "dc012",
                    "ba000_w2_3",
                ],
                "MMSE": [
                    "dc001s1",
                    "dc001s2",
                    "dc001s3",
                    "dc002",
                    "dc003",
                    "dc004",
                    "dc027s1",
                    "dc027s2",
                    "dc027s3",
                    "dc027s4",
                    "dc027s5",
                    "dc027s6",
                    "dc027s7",
                    "dc027s8",
                    "dc027s9",
                    "dc019",
                    "dc020",
                    "dc021",
                    "dc022",
                    "dc023",
                    "da007_1_",
                    "da007_2_",
                    "da007_3_",
                    "da007_4_",
                    "da007_5_",
                    "da007_6_",
                    "da007_7_",
                    "da007_8_",
                    "da007_9_",
                    "da007_10_",
                    "da007_11_",
                    "da007_12_",
                    "da007_13_",
                    "da007_14_",
                    "da008_1_",
                    "da008_5_",
                    "da008_11_",
                    "da013s1",
                    "da013s2",
                    "da013s3",
                    "da013s4",
                    "da013s5",
                    "da016s1",
                    "da016s2",
                    "da016s3",
                    "da016s4",
                    "da016s5",
                    "da016s6",
                    "da018s1",
                    "da018s2",
                    "da018s3",
                    "da018s4",
                    "da018s5",
                    "da018s6",
                    "da019s1",
                    "da019s2",
                    "da019s3",
                    "da019s4",
                    "da019s5",
                    "da019s6",
                    "da005_5_",
                    "da007_12_",
                    "da017",
                    "da056s1",
                    "da056s2",
                    "db009",
                    "db007",
                    "db006",
                    "da032",
                    "da033",
                    "da034",
                    "da056_w3s1",
                    "da056_w3s2",
                    "da056_w3s3",
                    "da056_w3s4",
                    "db006",
                    "dc025",
                    "bd001",
                    "ba004",
                    "ba000_w2_3",
                ],
            },
            2011: {
                "PFP": [
                    "ql002",
                    "qi002",
                    "qc003",
                    "qc004",
                    "qc005",
                    "qc006",
                    "qg002",
                    "qg003",
                    "da051_1_",
                    "da051_2_",
                    "da051_3_",
                    "dc018",
                    "dc012",
                    "rgender",
                ],
                "MMSE": [
                    "dc001s1",
                    "dc001s2",
                    "dc001s3",
                    "dc002",
                    "dc003",
                    "dc004",
                    "dc027s1",
                    "dc027s2",
                    "dc027s3",
                    "dc027s4",
                    "dc027s5",
                    "dc027s6",
                    "dc027s7",
                    "dc027s8",
                    "dc027s9",
                    "dc019",
                    "dc020",
                    "dc021",
                    "dc022",
                    "dc023",
                    "da007_1_",
                    "da007_2_",
                    "da007_3_",
                    "da007_4_",
                    "da007_5_",
                    "da007_6_",
                    "da007_7_",
                    "da007_8_",
                    "da007_9_",
                    "da007_10_",
                    "da007_11_",
                    "da007_12_",
                    "da007_13_",
                    "da007_14_",
                    "da008_1_",
                    "da008_5_",
                    "da008_11_",
                    "da013s1",
                    "da013s2",
                    "da013s3",
                    "da013s4",
                    "da013s5",
                    "da016s1",
                    "da016s2",
                    "da016s3",
                    "da016s4",
                    "da016s5",
                    "da016s6",
                    "da018s1",
                    "da018s2",
                    "da018s3",
                    "da018s4",
                    "da018s5",
                    "da018s6",
                    "da019s1",
                    "da019s2",
                    "da019s3",
                    "da019s4",
                    "da019s5",
                    "da019s6",
                    "da005_5_",
                    "da017s2",
                    "da056s1",
                    "da056s2",
                    "db009",
                    "db007",
                    "da032",
                    "da033",
                    "da034",
                    "da057_8_",
                    "da057_9_",
                    "da057_10_",
                    "da057_11_",
                    "db006",
                    "dc025",
                    "bd001",
                    "ba002_1",
                    "rgender",
                ],
            },
        }

        self.df = source_df[self.indicators[self.year][self.scale]]

    def get_df(self):
        return self.df

    def calculate_PFP_indicators(self):
        # gender_code = 'ba000_w2_3' if year != 2011 else 'rgender'
        indicators = self.indicators[self.year][self.scale]
        frail_array = []

        for i in self.df.index.values:
            score = 0

            # 1.体重减轻
            BMI = float(self.df.loc[i, indicators[0]]) / (
                (float(self.df.loc[i, indicators[0]]) / 100) ** 2
            )
            score += 1 if BMI <= 18.5 else 0
            # 2.握力退减
            avg = (
                float(self.df.loc[i, indicators[2]])
                + float(self.df.loc[i, indicators[4]])
                + float(self.df.loc[i, indicators[3]])
                + float(self.df.loc[i, indicators[5]])
            ) / 4
            item_score = 0
            # 男性
            if self.df.loc[i, indicators[13]] == 1:
                if BMI <= 20.6 and avg >= 25.2:
                    item_score = 1
                elif 20.6 < BMI <= 23.2 and avg >= 28.5:
                    item_score = 1
                elif 23.2 < BMI < 25.9 and avg >= 30:
                    item_score = 1
                elif BMI >= 25.9 and avg >= 30:
                    item_score = 1
            # 女性
            elif self.df.loc[i, indicators[13]] == 2:
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
            if self.df.loc[i, indicators[13]] == 1:
                if (
                    float(self.df.loc[i, indicators[1]]) <= 163
                    and float(self.df.loc[i, indicators[1]]) / 2.5 >= 0.45
                ):
                    item_score = 1
                elif (
                    float(self.df.loc[i, indicators[1]]) > 163
                    and float(self.df.loc[i, indicators[1]]) / 2.5 > 0.48
                ):
                    item_score = 1
            # 女性
            elif self.df.loc[i, indicators[13]] == 2:
                if (
                    float(self.df.loc[i, indicators[1]]) <= 151
                    and float(self.df.loc[i, indicators[1]]) / 2.5 >= 0.36
                ):
                    item_score = 1
                elif (
                    float(self.df.loc[i, indicators[1]]) > 151
                    and float(self.df.loc[i, indicators[1]]) / 2.5 > 0.43
                ):
                    item_score = 1
            score += item_score

            # 4.体力活动水平减弱
            if (
                self.df.loc[i, indicators[8]] == 1
                or self.df.loc[i, indicators[9]] == 1
                or self.df.loc[i, indicators[10]] == 1
            ):
                score += 1

            # 5.自报疲劳
            if (
                float(self.df.loc[i, indicators[11]])
                + float(self.df.loc[i, indicators[12]])
                - 2
                >= 3
            ):
                score += 1

            frail_array.append(1 if score >= 3 else 0)
        self.df["frail"] = frail_array

    def calculate_MMSE_indicators(self):
        if self.year == 2018 and self.scale == "MMSE":
            self.__calculate_MMSE_2018()
            return
        indicators = self.indicators[self.year][self.scale]
        cognition_array = []
        score_array = []
        for i in self.df.index.values:
            score = 0
            # 1
            score += 1 if int(self.df.loc[i, indicators[0]]) == 1 else 0
            # 2
            score += 1 if int(self.df.loc[i, indicators[1]]) == 1 else 0
            # 3
            score += 1 if int(self.df.loc[i, indicators[2]]) == 1 else 0
            # 4
            score += 1 if int(self.df.loc[i, indicators[3]]) == 1 else 0
            # 5
            score += 1 if int(self.df.loc[i, indicators[4]]) == 1 else 0
            # 6-10
            score += 6 - int(self.df.loc[i, indicators[5]])
            # 11
            score += (
                1
                if int(self.df.loc[i, indicators[6]]) == 1
                or int(self.df.loc[i, indicators[7]]) == 2
                or int(self.df.loc[i, indicators[8]]) == 3
                else 0
            )
            # 12
            score += (
                1
                if int(self.df.loc[i, indicators[9]]) == 4
                or int(self.df.loc[i, indicators[10]]) == 5
                or int(self.df.loc[i, indicators[11]]) == 6
                else 0
            )
            # 13
            score += (
                1
                if int(self.df.loc[i, indicators[12]]) == 7
                or int(self.df.loc[i, indicators[13]]) == 8
                or int(self.df.loc[i, indicators[14]]) == 9
                else 0
            )
            # 14
            score += 1 if int(self.df.loc[i, indicators[15]]) == 93 else 0
            # 15
            score += 1 if int(self.df.loc[i, indicators[16]]) == 86 else 0
            # 16
            score += 1 if int(self.df.loc[i, indicators[17]]) == 79 else 0
            # 17
            score += 1 if int(self.df.loc[i, indicators[18]]) == 72 else 0
            # 18
            score += 1 if int(self.df.loc[i, indicators[19]]) == 65 else 0
            # 19
            score += (
                1
                if int(self.df.loc[i, indicators[6]]) == 1
                and int(self.df.loc[i, indicators[7]]) == 2
                and int(self.df.loc[i, indicators[8]]) == 3
                else 0
            )
            # 20
            score += (
                1
                if int(self.df.loc[i, indicators[9]]) == 4
                and int(self.df.loc[i, indicators[10]]) == 5
                and int(self.df.loc[i, indicators[11]]) == 6
                else 0
            )
            # 21
            score += (
                1
                if int(self.df.loc[i, indicators[12]]) == 7
                and int(self.df.loc[i, indicators[13]]) == 8
                and int(self.df.loc[i, indicators[14]]) == 9
                else 0
            )

            tmp = False
            for j in range(1, 15):
                if int(self.df.loc[i, indicators[19 + j]]) == 1:
                    tmp = True
                    break
            if (
                int(self.df.loc[i, indicators[34]]) == 1
                or int(self.df.loc[i, indicators[35]]) == 1
                or int(self.df.loc[i, indicators[36]])
            ):
                tmp = True
            for j in range(1, 6):
                if 1 <= int(self.df.loc[i, indicators[36 + j]]) <= 4:
                    tmp = True
                    break
            for j in range(1, 7):
                if 1 <= int(self.df.loc[i, indicators[41 + j]]) <= 5:
                    tmp = True
                    break
            for j in range(1, 7):
                if 1 <= int(self.df.loc[i, indicators[47 + j]]) <= 5:
                    tmp = True
                    break
            for j in range(1, 7):
                if 1 <= int(self.df.loc[i, indicators[53 + j]]) <= 5:
                    tmp = True
                    break
            # 22-23
            score += 2 if tmp else 0
            # 24
            tmp = 0
            tmp += 0.3 if int(self.df.loc[i, indicators[60]]) != 1 else 0
            tmp += 0.3 if int(self.df.loc[i, indicators[31]]) != 1 else 0
            tmp += 0.2 if int(self.df.loc[i, indicators[62]]) == 1 else 0
            tmp += 0.2 if int(self.df.loc[i, indicators[63]]) == 1 else 0
            score += 1 if tmp >= 0.5 else 0
            # 25
            score += 1 if 1 <= int(self.df.loc[i, indicators[64]]) <= 2 else 0
            # 26
            score += 1 if 1 <= int(self.df.loc[i, indicators[65]]) <= 2 else 0
            # 27
            score += 1 if 1 <= int(self.df.loc[i, indicators[75]]) <= 2 else 0
            # 28
            tmp = 0
            tmp += 0.2 if int(self.df.loc[i, indicators[66]]) != 1 else 0
            tmp += 0.2 if int(self.df.loc[i, indicators[67]]) in [4, 5] else 0
            tmp += 0.2 if int(self.df.loc[i, indicators[68]]) in [4, 5] else 0
            tmp += 0.3 if int(self.df.loc[i, indicators[69]]) == 1 else 0
            tmp += 0.3 if int(self.df.loc[i, indicators[70]]) == 1 else 0
            tmp += 0.3 if int(self.df.loc[i, indicators[71]]) == 1 else 0
            tmp += 0.3 if int(self.df.loc[i, indicators[72]]) == 1 else 0
            tmp += 0.3 if int(self.df.loc[i, indicators[75]]) in [1, 2] else 0
            score += 1 if tmp >= 0.5 else 0
            # 29
            tmp = 0
            tmp += 0.5 if int(self.df.loc[i, indicators[69]]) == 1 else 0
            tmp += 0.5 if int(self.df.loc[i, indicators[70]]) == 1 else 0
            tmp += 0.5 if int(self.df.loc[i, indicators[71]]) == 1 else 0
            tmp += 0.5 if int(self.df.loc[i, indicators[72]]) == 1 else 0
            tmp += 0.4 if int(self.df.loc[i, indicators[64]]) not in [2, 3, 4] else 0
            score += 1 if tmp >= 0.5 else 0
            # 30
            score += 1 if int(self.df.loc[i, indicators[74]]) == 1 else 0
            score_array.append(score)
            # print(int(self.df.loc[i, indicators[75]]))
            cognition_array.append(
                1 if is_cog_imp(score, int(self.df.loc[i, indicators[75]])) else 0
            )
        self.df["cognition_impairment"] = cognition_array
        self.df["score"] = score_array

    def __calculate_MMSE_2018(self):
        indicators = self.indicators[self.year][self.scale]
        cognition_array = []
        score_array = []
        for i in self.df.index.values:
            score = 0
            # 1~10
            for j in range(1, 11):
                score += 1 if int(self.df.loc[i, indicators[j - 1]]) == 1 else 0
            # 11~13
            for j in range(11, 14):
                score += 1 if 1 <= int(self.df.loc[i, indicators[j - 1]]) < 4 else 0
            # 14~18
            for j in range(14, 19):
                score += (
                    1
                    if int(self.df.loc[i, indicators[j - 1]]) == (100 - 7 * (j - 13))
                    else 0
                )
            # 19~21
            for j in range(19, 22):
                score += 1 if 1 <= int(self.df.loc[i, indicators[j - 1]]) < 4 else 0

            # 22~30
            for j in range(22, 31):
                score += 1 if int(self.df.loc[i, indicators[j - 1]]) in [1, 2] else 0
            score_array.append(score)
            cognition_array.append(
                1 if is_cog_imp(score, self.df.loc[i, indicators[30]]) else 0
            )
        self.df["cognition_impairment"] = cognition_array
        self.df["score"] = score_array

    def del_specific_rows(self, func):
        """
        删除满足函数func条件的行
        """
        rows = []
        for i in range(0, self.df.shape[0]):
            if func(self.df.iloc[i, :]):
                rows.append(self.df.index.values[i])
        self.df.drop(index=rows, axis=0, inplace=True)

    def imputation(self, rate):
        # Etract columns with missing rate less than rate to imputate
        # Reason: if a columns only have 5% data, imputation will not have a good result
        columns_not_null = []
        for i in self.df.columns.values:
            if self.df[i].isnull().sum() / self.df.shape[0] <= rate:
                columns_not_null.append(i)

        imputate_df = self.df[columns_not_null]
        df_amp = mf.ampute_data(imputate_df, perc=0.25, random_state=1991)
        kernel = mf.ImputationKernel(
            df_amp, datasets=4, save_all_iterations=True, random_state=1
        )
        kernel.mice(2)
        imputate_df = kernel.complete_data()

        columns_null = []
        for i in self.df.columns.values:
            if i not in columns_not_null:
                columns_null.append(i)
        rest_df = self.df[columns_null]

        # imputate_df.to_csv("imputate_df.csv")

        # rest_df.to_csv("rest_df.csv")
        self.df = rest_df.merge(imputate_df, on="ID")
