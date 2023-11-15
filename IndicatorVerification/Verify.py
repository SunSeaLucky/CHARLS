import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import pearsonr
import sys

sys.path.append("Operator")
import Operator

cognition_missing_rate = 0.5


def cognition_more_than_value(row):
    cnt = 0
    for i in row:
        if str(i) == "nan":
            cnt += 1
    return cnt / row.shape[0] >= cognition_missing_rate


health_status_and_functioning_path = "D:\Personal\\University\CollegeProject\CollegeProject-2\CHARLS\CHARLS-Database-2018\Data\Health_Status_and_Functioning.dta"
demographic_background_path = "D:\Personal\\University\CollegeProject\CollegeProject-2\CHARLS\CHARLS-Database-2018\Data\Demographic_Background.dta"
cognition_path = "D:\Personal\\University\CollegeProject\CollegeProject-2\CHARLS\CHARLS-Database-2018\Data\Cognition.dta"
health_status_and_functioning = pd.read_stata(
    health_status_and_functioning_path, index_col="ID", convert_categoricals=False
)
demographic_background = pd.read_stata(
    demographic_background_path, index_col="ID", convert_categoricals=False
)
cognition = pd.read_stata(cognition_path, index_col="ID", convert_categoricals=False)

source_df = Operator.merge_df(
    health_status_and_functioning, Operator.merge_df(cognition, demographic_background)
)

cog = Operator.DataOperator(2018, "MMSE", source_df)
cog_new = Operator.DataOperator(2018, "new_MMSE", source_df)

cog.del_specific_rows(cognition_more_than_value)
cog_new.del_specific_rows(cognition_more_than_value)

cog.df.fillna(-1, inplace=True)
cog_new.df.fillna(-1, inplace=True)

cog.calculate_MMSE_indicators()
cog_new.calculate_MMSE_indicators()

cog_new.df.rename(
    columns={"cognition_impairment": "cognition_impairment_new"}, inplace=True
)
verification = Operator.merge_df(
    cog.df["cognition_impairment"], cog_new.df["cognition_impairment_new"]
)

# cog.get_df().to_csv('cog.csv')
# cog_new.get_df().to_csv('cog_new.csv')
# verification.to_csv('verification.csv')

cog_new.df.rename(columns={"score": "new_score"}, inplace=True)
res = Operator.merge_df(cog_new.df, cog.df)

new = res["new_score"]
old = res["score"]

print(pearsonr(new, old))
# plt.figure(figsize=(10, 10), dpi=100)
plt.scatter(new, old)
plt.show()
