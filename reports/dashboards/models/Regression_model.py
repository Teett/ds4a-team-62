import pickle
from sklearn.linear_model import LogisticRegressionCV

################################################################################################
# Load the model and retrieve the DataFrame with today's pacients to pass to the model
################################################################################################
with open('../../models/admission/reg_elastic_net.pickle', 'rb') as f:
    model = pickle.load(f)

def get_hosp_probabilities(adm_dummies):
    ################################################################################################
    # Run the tunned model with the selected data
    ################################################################################################
    y_prob = model.predict_proba(adm_dummies)   
    return y_prob[:,1]


def get_hosp_pred(adm_dummies):
    ################################################################################################
    # Run the tunned model with the selected data
    ################################################################################################
    y_prob =model.predict_proba(adm_dummies) 
    y_pred = (y_prob[:,1] >= 0.25).astype(int)
    return y_pred