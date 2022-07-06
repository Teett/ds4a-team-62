import pandas as pd

def transform_data (df):

# %% analyize missingess
# impute 3, this new category will mean that there it is not know if the patient has a sensitive condition
    transformed_df = df.copy()
    transformed_df['ACSC'] = df['ACSC'].fillna(3)
    # impute category 5 (unknown) to the ethnicity variable
    transformed_df['Ethnicity'] = df['Ethnicity'].fillna(5)
    # drop the other null values, only 24 records will be discarded
    transformed_df = transformed_df.dropna()
    # get dummies
    adm_dummies = pd.get_dummies(transformed_df, 
                                columns=['Site','Age_band','IMD_quintile','Ethnicity', 'ACSC'], 
                                drop_first=True)
    #adm_dummies = adm_dummies.drop(['Admission_ALL', 'Stay_length'], axis = 1)

    ## Re-organize the DF adm_dummies that we are gonna pass to the model in the same order the original DF was Fitted ##
    try:
        adm_dummies = adm_dummies [['DayWeek_coded','Shift_coded','Arr_Amb','Gender','Consultant_on_duty','ED bed occupancy','Inpatient_bed_occupancy',
                                'Arrival intensity', 'LAS intensity', 'LWBS intensity', 'Last_10_mins', 'Site_2.0','Site_3.0', 'Age_band_1.0',
                                'Age_band_2.0', 'Age_band_3.0', 'IMD_quintile_1.0', 'IMD_quintile_2.0', 'IMD_quintile_3.0', 'IMD_quintile_4.0',
                                'IMD_quintile_5.0','Ethnicity_2.0','Ethnicity_3.0','Ethnicity_4.0','Ethnicity_5.0','Ethnicity_6.0','ACSC_1.0', 'ACSC_3.0']]
    except:
        pass
    return adm_dummies