# %% libraries
import pandas as pd
import missingno as msno
from sklearn.model_selection import train_test_split

# read the data
raw_er_admission = pd.read_excel('../../data/raw/er_admission.xlsx', sheet_name = 'Data')

# %% analyize missingess
raw_er_admission.head()
msno.matrix(raw_er_admission)
msno.heatmap(raw_er_admission)
raw_er_admission.isna().sum()
# Only significant missing values are on ACSC and Ethnicity, treatment will be decided for these and the rest of the missingness discarded

# impute 3, this new category will mean that there it is not know if the patient has a sensitive condition
er_admission = raw_er_admission.copy()
er_admission['ACSC'] = raw_er_admission['ACSC'].fillna(3)
# impute category 5 (unknown) to the ethnicity variable
er_admission['Ethnicity'] = raw_er_admission['Ethnicity'].fillna(5)
# drop the other null values, only 24 records will be discarded
er_admission = er_admission.dropna()
# %% get dummies
adm_dummies = pd.get_dummies(er_admission, 
                            columns=['Site','Age_band','IMD_quintile','Ethnicity', 'ACSC'], 
                            drop_first=True)
adm_dummies.head()
adm_dummies.isna().sum()
# %% Train test splits
# The reasoning behind the elimination of both variables is that none is known once the patient arrives to the ER
X_train_stay, X_test_stay, y_train_stay, y_test_stay = train_test_split(adm_dummies.drop(['Admission_ALL', 'Stay_length'], axis = 1), 
                                                                        adm_dummies["Stay_length"], test_size=0.2, random_state=1337)

X_train_adm, X_test_adm, y_train_adm, y_test_adm = train_test_split(adm_dummies.drop(['Admission_ALL', 'Stay_length'], axis = 1), 
                                                                        adm_dummies["Admission_ALL"], test_size=0.2, random_state=1337,
                                                                        stratify=adm_dummies["Admission_ALL"])
