import os
import pandas as pd

PATH = "D:/Personal/University/CollegeProject/CollegeProject-2/CHARLS/CHARLS-Database-2011/Data"
a = os.listdir(path=PATH)

for i in a:
    file = PATH + "/" + i
    try:
        df = pd.read_stata(file, index_col="ID", convert_categoricals=False)
        df.to_csv(PATH + "/" + i + ".csv")
    except Exception as e:
        pass
