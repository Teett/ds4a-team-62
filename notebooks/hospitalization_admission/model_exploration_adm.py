# %% libraries
import pandas as pd
import matplotlib.pyplot as plt
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier
from sklearn import model_selection
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay, recall_score, make_scorer, f1_score, balanced_accuracy_score

# %% read data 
X_train = pd.read_pickle('../../data/processed/admission/X_train_adm.pickle')
X_test = pd.read_pickle('../../data/processed/admission/X_test_adm.pickle')
y_train = pd.read_pickle('../../data/processed/admission/y_train_adm.pickle')
y_test = pd.read_pickle('../../data/processed/admission/y_test_adm.pickle')

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
    confusion_matrices = []
    classification_reports = []
    models = [
            ('LogReg', LogisticRegression(max_iter = 500)),
            ('ElasticNet', LogisticRegression(penalty='elasticnet', 
                                              solver='saga', l1_ratio=0.5, max_iter=1500)),
            ('Lasso', LogisticRegression(penalty='elasticnet', 
                                              solver='saga', l1_ratio=1, max_iter=1500)),
            ('Ridge', LogisticRegression(penalty='elasticnet', 
                                              solver='saga', l1_ratio=0, max_iter=1500)),
            ('RF', RandomForestClassifier()),
            ('KNN', KNeighborsClassifier()),
            ('SVM', SVC()), 
            ('GNB', GaussianNB()),
            ('XGB', XGBClassifier(use_label_encoder = False))
            ]
    results = []
    names = []
    scoring = scoring = {
    'f1': make_scorer(f1_score),
    'f1_macro': make_scorer(f1_score, average='macro'),
    'f1_micro': make_scorer(f1_score, average='micro'),
    'f1_weighted': make_scorer(f1_score, average='weighted'),
    'sensitivity': make_scorer(recall_score),
    'specificity': make_scorer(recall_score,pos_label=0),
    'balanced_accuracy': make_scorer(balanced_accuracy_score),
    'roc_auc': 'roc_auc'}
    target_names = ["Not Hospitalized" , "Hospitalized"]



    for name, model in models:
        kfold = model_selection.KFold(n_splits=10, shuffle=True, random_state=90210)
        cv_results = model_selection.cross_validate(model, x_train, y_train, cv = kfold, scoring=scoring)
        clf = model.fit(x_train, y_train)
        y_pred = clf.predict(x_test)
        print(name)
        class_report = classification_report(y_test, y_pred, target_names=target_names)
        print(class_report)
        confusion = confusion_matrix(y_test, y_pred, labels=clf.classes_)
        disp = ConfusionMatrixDisplay(confusion_matrix = confusion, display_labels = clf.classes_)
        disp.plot()
        plt.show()
        results.append(cv_results)
        names.append(name)
        this_df = pd.DataFrame(cv_results)
        this_df['model'] = name
        dfs.append(this_df)
        final = pd.concat(dfs, ignore_index=True)
        confusion_matrices.append(confusion)
        classification_reports.append(class_report)
    return [final, confusion_matrices, classification_reports]

models = run_exps(X_train, y_train, X_test, y_test)
models[0].groupby('model')['test_roc_auc', 'test_sensitivity', 'test_specificity'].mean()
models[0].groupby('model')['fit_time'].mean()
with open("../../models/admission/many_models_adm_1.pickle", "wb") as fp:   #Pickling
    pickle.dump(models, fp)