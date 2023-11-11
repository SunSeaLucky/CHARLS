import miceforest as mf
import pandas as pd
import os
import numpy as np


class CommonFunction:

    def imputation(df):
        df_amp = mf.ampute_data(df, perc=0.25, random_state=1991)
        kernel = mf.ImputationKernel(df_amp, datasets=4, save_all_iterations=True, random_state=1)
        kernel.mice(2)
        return kernel.complete_data()

    def del_df(df1, df2):
        """
        Make df1 and df2 have same rows
        """
        df1.sort_index(inplace=True)
        df2.sort_index(inplace=True)

        same_rows = []

        for i in df1.index.values:
            for j in df2.index.values:
                if int(i) < int(j):
                    break
                elif i == j:
                    same_rows.append(i);
                    break

        df1.drop(index=df1.index.difference(same_rows), inplace=True)
        df2.drop(index=df2.index.difference(same_rows), inplace=True)

    def del_specific(df, func):
        rows = []
        for i in range(0, df.shape[0]):
            if func(df.iloc[i, :]):
                rows.append(df.index.values[i])
        return df.drop(index=rows, axis=0)

    def dta_to_csv(filepath: str):
        data = pd.io.stata.read_stata(filepath)
        data.to_csv(filepath.split('.')[0] + ".csv", encoding='ansi')

    def all_dta_to_csv(file_path):
        all_files = os.listdir(file_path)
        for i in all_files:
            try:
                CommonFunction.dta_to_csv(file_path + '\\' + i)
            except:
                print('Has code problem with ' + i)

    def change_space_to_nan(df):
        for i in range(0, df.shape[0]):
            for j in range(0, df.shape[1]):
                if str(df.iloc[i, j] == ' '):
                    df.iloc[i, j] == np.nan
        return df
