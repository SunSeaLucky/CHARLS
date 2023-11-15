import numpy as np
import pandas as pd
import sys

sys.path.append("Operator")
from Operator import Operator


PATHS = {
    "2015": {
        "HSF_PATH": "D:/Personal/University/CollegeProject/CollegeProject-2/CHARLS/CHARLS-Database-2015/Data/Health_Status_and_Functioning.dta",
        "DB_PATH": "D:/Personal/University/CollegeProject/CollegeProject-2/CHARLS/CHARLS-Database-2015/Data/Demographic_Background.dta",
        "BIO_PATH": "D:/Personal/University/CollegeProject/CollegeProject-2/CHARLS/CHARLS-Database-2015/Data/Biomarker.dta",
    },
    "2013": {
        "HSF_PATH": "D:/Personal/University/CollegeProject/CollegeProject-2/CHARLS/CHARLS-Database-2013/Data/Health_Status_and_Functioning.dta",
        "DB_PATH": "D:/Personal/University/CollegeProject/CollegeProject-2/CHARLS/CHARLS-Database-2013/Data/Demographic_Background.dta",
        "BIO_PATH": "D:/Personal/University/CollegeProject/CollegeProject-2/CHARLS/CHARLS-Database-2013/Data/Biomarker.dta",
    },
    "2011": {
        "HSF_PATH": "D:/Personal/University/CollegeProject/CollegeProject-2/CHARLS/CHARLS-Database-2011/Data/health_status_and_functioning.dta",
        "DB_PATH": "D:/Personal/University/CollegeProject/CollegeProject-2/CHARLS/CHARLS-Database-2011/Data/demographic_background.dta",
        "BIO_PATH": "D:/Personal/University/CollegeProject/CollegeProject-2/CHARLS/CHARLS-Database-2011/Data/biomarkers.dta",
    },
}

# 2011 -----
a = pd.read_stata(PATHS["2011"]["HSF_PATH"], index_col="ID", convert_categoricals=False)
b = pd.read_stata(PATHS["2011"]["DB_PATH"], index_col="ID", convert_categoricals=False)
c = pd.read_stata(PATHS["2011"]["BIO_PATH"], index_col="ID", convert_categoricals=False)
y2011_resource = c.merge(a.merge(b, on="ID"), on="ID")

y2011_cog = Operator.DataOperator(2011, "MMSE", y2011_resource)
y2011_fra = Operator.DataOperator(2011, "PFP", y2011_resource)

y2011_cog.calculate_MMSE_indicators()
y2011_fra.calculate_PFP_indicators()

y2011_cog.df.to_csv("cog.csv")
y2011_fra.df.to_csv("fra.csv")
