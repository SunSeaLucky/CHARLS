# extract 2013 data

import pandas as pd

import Operator

frail_missing_rate = 0.1
cognition_missing_rate = 0.7
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


# files' path
biomarkers_path = 'D:\Personal\\University\CollegeProject\CollegeProject-2\CHARLS\CHARLS-Database-2013\Data\Biomarker.dta'
health_status_and_functioning_path = 'D:\Personal\\University\CollegeProject\CollegeProject-2\CHARLS\CHARLS-Database-2013\Data\Health_Status_and_Functioning.dta'
interviewer_observation_path = 'D:\Personal\\University\CollegeProject\CollegeProject-2\CHARLS\CHARLS-Database-2013\Data\Interviewer_Observation.dta'
demographic_background_path = 'D:\Personal\\University\CollegeProject\CollegeProject-2\CHARLS\CHARLS-Database-2013\Data\Demographic_Background.dta'

# dataframes
biomarkers = pd.read_stata(biomarkers_path, index_col='ID', convert_categoricals=False)
health_status_and_functioning = pd.read_stata(health_status_and_functioning_path, index_col='ID', convert_categoricals=False)
interviewer_observation = pd.read_stata(interviewer_observation_path, index_col='ID', convert_categoricals=False)
demographic_background = pd.read_stata(demographic_background_path, index_col='ID', convert_categoricals=False)

# Extract same person
# Operator.remove_duplicates_and_sort(biomarkers, health_status_and_functioning)
# Operator.remove_duplicates_and_sort(biomarkers, demographic_background)
# Operator.remove_duplicates_and_sort(biomarkers, health_status_and_functioning)
#
# Operator.remove_duplicates_and_sort(health_status_and_functioning, interviewer_observation)
source_df = Operator.merge_df(demographic_background,
                              Operator.merge_df(interviewer_observation,
                                                Operator.merge_df(biomarkers, health_status_and_functioning)))

# Create new operator object
frail = Operator.DataOperator(2013, 'PFP', source_df)
cognition = Operator.DataOperator(2013, 'MMSE', source_df)

frail.del_specific_rows(frail_more_than_value)
cognition.del_specific_rows(cognition_more_than_value)

if debug_middle_result:
    frail.get_df().to_csv('1.csv')
    cognition.get_df().to_csv('2.csv')

if imputate_frail:
    frail.imputation()
if imputate_cognitioin:
    cognition.imputation()

frail.calculate_PFP_indicators(2013)
cognition.calculate_MMSE_indicators(2013)

res = Operator.merge_df(frail.get_df(), cognition.get_df())
if show_result_shape:
    print(res.shape)

res.to_csv('13-res.csv')
