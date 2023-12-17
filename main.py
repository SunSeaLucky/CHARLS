import numpy as np
import pandas as pd
import sys

sys.path.append("Operator")
from Operator import Operator

year = 2011


def delete_age(row):
    # print(type(row))
    # Delete person who's age is less than 45
    return year - int(row[76].astype(int)) < 45


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

# ----- 2011 -----
a = pd.read_stata(PATHS["2011"]["HSF_PATH"], index_col="ID", convert_categoricals=False)
b = pd.read_stata(PATHS["2011"]["DB_PATH"], index_col="ID", convert_categoricals=False)
c = pd.read_stata(PATHS["2011"]["BIO_PATH"], index_col="ID", convert_categoricals=False)
y2011_resource = c.merge(a.merge(b, on="ID"), on="ID")

y2011_cog = Operator.DataOperator(2011, "MMSE", y2011_resource)
# Set current year to calculate the age, then we can delete people who's age is less than 45
year = y2011_cog.year
y2011_cog.del_specific_rows(delete_age)
y2011_fra = Operator.DataOperator(2011, "PFP", y2011_resource)

# Imputate columns with missing rate less or equal .95
y2011_cog.imputation(0.95)
y2011_fra.imputation(0.95)

y2011_cog.df.fillna(-1, inplace=True)

y2011_cog.calculate_MMSE_indicators()
y2011_fra.calculate_PFP_indicators()

y2011_cog.df.to_csv("Result\cog-11.csv")
y2011_fra.df.to_csv("Result\\fra-11.csv")

# ----- 2013 -----
a = pd.read_stata(PATHS["2013"]["HSF_PATH"], index_col="ID", convert_categoricals=False)
b = pd.read_stata(PATHS["2013"]["DB_PATH"], index_col="ID", convert_categoricals=False)
c = pd.read_stata(PATHS["2013"]["BIO_PATH"], index_col="ID", convert_categoricals=False)
y2013_resource = c.merge(a.merge(b, on="ID"), on="ID")

y2013_cog = Operator.DataOperator(2013, "MMSE", y2013_resource)
year = y2013_cog.year
y2013_cog.del_specific_rows(delete_age)
y2013_fra = Operator.DataOperator(2013, "PFP", y2013_resource)

y2013_cog.imputation(0.95)
y2013_fra.imputation(0.95)

y2013_cog.df.fillna(-1, inplace=True)

y2013_cog.calculate_MMSE_indicators()
y2013_fra.calculate_PFP_indicators()

y2013_cog.df.to_csv("Result\cog-13.csv")
y2013_fra.df.to_csv("Result\\fra-13.csv")

# ----- 2015 -----
a = pd.read_stata(PATHS["2015"]["HSF_PATH"], index_col="ID", convert_categoricals=False)
b = pd.read_stata(PATHS["2015"]["DB_PATH"], index_col="ID", convert_categoricals=False)
c = pd.read_stata(PATHS["2015"]["BIO_PATH"], index_col="ID", convert_categoricals=False)
y2015_resource = c.merge(a.merge(b, on="ID"), on="ID")

y2015_cog = Operator.DataOperator(2015, "MMSE", y2015_resource)
year = y2015_cog.year
y2015_cog.del_specific_rows(delete_age)
y2015_fra = Operator.DataOperator(2015, "PFP", y2015_resource)

# Imputate columns with missing rate less or equal .95
y2015_cog.imputation(0.95)
y2015_fra.imputation(0.95)

y2015_cog.df.fillna(-1, inplace=True)

y2015_cog.calculate_MMSE_indicators()
y2015_fra.calculate_PFP_indicators()

y2015_cog.df.to_csv("Result\cog-15.csv")
y2015_fra.df.to_csv("Result\\fra-15.csv")
