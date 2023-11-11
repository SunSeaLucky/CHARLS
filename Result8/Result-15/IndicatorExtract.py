# extract 2015 data

import pandas as pd
import Operator

frail_missing_rate = 0.7
cognition_missing_rate = 0.7
delete_people_age_less_than = 45
imputate_frail = True
imputate_cognitioin = True
debug_middle_result = True
show_result_shape = True


def frail_more_than_value(row):
    cnt = 0
    for i in row:
        if str(i) == 'nan':
            cnt += 1
    return cnt / row.shape[0] >= frail_missing_rate


def cognition_more_than_value(row):
    cnt = 0
    for i in row:
        if str(i) == 'nan':
            cnt += 1
    return cnt / row.shape[0] >= cognition_missing_rate


def age_less_than(row):
    return int(row.loc[row.index.values[0], 'ba004_w3_1']) < delete_people_age_less_than


# files' path
biomarkers_path = 'D:\Personal\\University\CollegeProject\CollegeProject-2\CHARLS\CHARLS-Database-2015\Data\Biomarker.dta'
health_status_and_functioning_path = 'D:\Personal\\University\CollegeProject\CollegeProject-2\CHARLS\CHARLS-Database-2015\Data\Health_Status_and_Functioning.dta'
interviewer_observation_path = 'D:\Personal\\University\CollegeProject\CollegeProject-2\CHARLS\CHARLS-Database-2011\Data\interviewer_observation.dta'
demographic_background_path = 'D:\Personal\\University\CollegeProject\CollegeProject-2\CHARLS\CHARLS-Database-2015\Data\Demographic_Background.dta'

# dataframes
biomarkers = pd.read_stata(biomarkers_path, index_col='ID', convert_categoricals=False)
health_status_and_functioning = pd.read_stata(health_status_and_functioning_path, index_col='ID', convert_categoricals=False)
interviewer_observation = pd.read_stata(interviewer_observation_path, index_col='ID', convert_categoricals=False)
demographic_background = pd.read_stata(demographic_background_path, index_col='ID', convert_categoricals=False)

# indicators to extract

# Extract same person
# Operator.remove_duplicates_and_sort(biomarkers, health_status_and_functioning)
# Operator.remove_duplicates_and_sort(biomarkers, demographic_background)
# Operator.remove_duplicates_and_sort(biomarkers, health_status_and_functioning)
#
# Operator.remove_duplicates_and_sort(health_status_and_functioning, interviewer_observation)
source_df = Operator.merge_df(demographic_background,
                              Operator.merge_df(interviewer_observation,
                                                Operator.merge_df(biomarkers, health_status_and_functioning)))

source_df.to_csv('5.csv')
# Create new operator object
frail = Operator.DataOperator(2015, 'PFP', source_df)
cognition = Operator.DataOperator(2015, 'MMSE', source_df)

# cognition.del_specific_rows(age_less_than)
# frail.del_specific_rows(frail_more_than_value)
# cognition.del_specific_rows(cognition_more_than_value)

if debug_middle_result:
    frail.get_df().to_csv('1.csv')
    cognition.get_df().to_csv('2.csv')

if imputate_frail:
    frail.imputation()
if imputate_cognitioin:
    cognition.imputation()

frail.calculate_PFP_indicators(2015)
cognition.calculate_MMSE_indicators(2015)

res = Operator.merge_df(frail.get_df(), cognition.get_df())
if show_result_shape:
    print(res.shape)

res.to_csv('15-res.csv')
