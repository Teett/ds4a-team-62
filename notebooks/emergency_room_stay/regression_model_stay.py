# %% libraries
import pandas as pd
import matplotlib.pyplot as plt
import pickle
from sklearn.linear_model import LinearRegression
from sklearn import model_selection
from sklearn.metrics import r2_score, make_scorer

# %% read data 
X_train = pd.read_pickle('../../data/processed/stay/X_train_stay.pickle')
X_test = pd.read_pickle('../../data/processed/stay/X_test_stay.pickle')
y_train = pd.read_pickle('../../data/processed/stay/y_train_stay.pickle')
y_test = pd.read_pickle('../../data/processed/stay/y_test_stay.pickle')

# %% run many models with default parameters

def run_exps(x_train: pd.DataFrame , y_train: pd.DataFrame, x_test: pd.DataFrame, y_test: pd.DataFrame) -> pd.DataFrame:
    '''
    Lightweight script to test 431many models and find winners
    :param x_train: training split
    :param y_train: training target vector
    :param x_test: test split
    :param y_test: test target vector
    :return: DataFrame of predictions
    '''
    
    dfs = []
    models = [
            ('LinReg', LinearRegression())
            ]
    results = []
    names = []
    scoring = {
    #'neg_mean_absolute_error': make_scorer(neg_mean_absolute_error), 
    #'neg_mean_squared_error': make_scorer(neg_mean_squared_error), 
    #'neg_median_absolute_error': make_scorer(neg_median_absolute_error), 
    'r2': make_scorer(r2_score) 
    }
    
    for name, model in models:
        kfold = model_selection.KFold(n_splits=10, shuffle=True, random_state=90210)
        cv_results = model_selection.cross_validate(model, x_train, y_train, cv = kfold, scoring= ('r2', 'neg_mean_squared_error') )
        regressor = model.fit(x_train, y_train)
        y_pred = regressor.predict(x_test)
        print(name)
        results.append(cv_results)
        names.append(name)
        this_df = pd.DataFrame(cv_results)
        this_df['model'] = name
        dfs.append(this_df)
        final = pd.concat(dfs, ignore_index=True)
        
    return [final]

models = run_exps(X_train, y_train, X_test, y_test)

#%% 

models[0].groupby('model')['test_neg_mean_squared_error', 'test_r2'].mean()

#%%
with open("../../models/stay/many_models_stay_1.pickle", "wb") as fp:   #Pickling
    pickle.dump(models, fp)


# %%
