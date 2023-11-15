import numpy as np
import pandas as pd
import sys

sys.path.append("Operator")
from Operator import Operator


PATHS = {
    "2015": {
        "HSF_PATH": "D:/Personal/University/CollegeProject/CollegeProject-2/CHARLS/CHARLS-Database-2015/Data/Health_Status_and_Functioning.dta",
        "DB_PATH": "D:/Personal/University/CollegeProject/CollegeProject-2/CHARLS/CHARLS-Database-2015/Data/Demographic_Background.dta",
    },
    "2013": {
        "HSF_PATH": "D:/Personal/University/CollegeProject/CollegeProject-2/CHARLS/CHARLS-Database-2013/Data/Health_Status_and_Functioning.dta",
        "DB_PATH": "D:/Personal/University/CollegeProject/CollegeProject-2/CHARLS/CHARLS-Database-2013/Data/Demographic_Background.dta",
    },
    "2011": {
        "HSF_PATH": "D:/Personal/University/CollegeProject/CollegeProject-2/CHARLS/CHARLS-Database-2011/Data/health_status_and_functioning.dta",
        "DB_PATH": "D:/Personal/University/CollegeProject/CollegeProject-2/CHARLS/CHARLS-Database-2011/Data/demographic_background.dta",
    },
}

# 2011 -----
a = pd.read_stata(PATHS["2011"]["HSF_PATH"], index_col="ID", convert_categoricals=False)
b = pd.read_stata(PATHS["2011"]["DB_PATH"], index_col="ID", convert_categoricals=False)
y2011_resource = a.merge(b, on="ID")

y2011 = Operator.DataOperator(2011, "MMSE", y2011_resource)

cog = y2011.calculate_MMSE_indicators()

y2011.df.to_csv("1.csv")
