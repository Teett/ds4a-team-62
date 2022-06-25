import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pickle
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import confusion_matrix, recall_score, f1_score, classification_report, make_scorer, precision_recall_curve, auc
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.model_selection import RandomizedSearchCV
X_train = pd.read_pickle('../../data/processed/admission/X_train_adm.pickle')
X_test = pd.read_pickle('../../data/processed/admission/X_test_adm.pickle')
y_train = pd.read_pickle('../../data/processed/admission/y_train_adm.pickle')
y_test = pd.read_pickle('../../data/processed/admission/y_test_adm.pickle')


# ## Build preliminary SVM
pred_labels = ["Not Hospitalized" , "Hospitalized"]

# Elastic net

## Build Initial Logistic Regression with CV
alpha_range = [0, 0.3, 0.5, 0.7, 0.9, 1]
elastic_net_class = LogisticRegressionCV(cv = 10, solver = 'saga', penalty = 'elasticnet', max_iter = 1500,
                                         random_state = 1995, scoring = "recall", n_jobs = 6, l1_ratios = alpha_range)

elastic_net_class.fit(X_train, y_train)

elastic_net_y_pred = elastic_net_class.predict(X_test)
elastic_net_y_prob =elastic_net_class.predict_proba(X_test) 


### Evaluation

#### Precision Recall Curve

precision, recall, thresholds = precision_recall_curve(y_test, elastic_net_y_prob[:, 1]) 
   #retrieve probability of being 1(in second column of probs_y)
pr_auc = auc(recall, precision)

plt.title("Precision-Recall vs Threshold Chart")
plt.plot(thresholds, precision[: -1], "b--", label="Precision")
plt.plot(thresholds, recall[: -1], "r--", label="Recall")
plt.ylabel("Precision, Recall")
plt.xlabel("Threshold")
plt.legend(loc="lower left")
plt.ylim([0,1])


#### Test Confusion Matrix
elastic_net_confusion = confusion_matrix(y_test, elastic_net_y_pred)
elastic_net_disp = ConfusionMatrixDisplay(confusion_matrix = elastic_net_confusion, display_labels = pred_labels)
elastic_net_disp.plot()
plt.show()


#### Modified threshold
y_pred = (elastic_net_y_prob[:,1] >= 0.25).astype(int)
modified_threshold_conf = confusion_matrix(y_test, y_pred)
modified_threshold_disp = ConfusionMatrixDisplay(confusion_matrix = modified_threshold_conf, display_labels = pred_labels)
modified_threshold_disp.plot()
plt.show()

print(classification_report(y_test, y_pred, target_names = pred_labels))
recall_score(y_test, y_pred)
f1_score(y_test, y_pred)

#### Test classification report
print(classification_report(y_test, elastic_net_y_pred, target_names = pred_labels))
recall_score(y_test, elastic_net_y_pred)
f1_score(y_test, elastic_net_y_pred)
# Model properties
elastic_net_coefs = pd.concat([pd.DataFrame(X_train.columns),pd.DataFrame(np.transpose(elastic_net_class.coef_))], axis = 1)
elastic_net_coefs

elastic_net_class.Cs_
elastic_net_class.l1_ratios_
elastic_net_class.coefs_paths_
elastic_net_class.l1_ratio_[0]
elastic_net_class.C_
elastic_net_class.scores_

with open("../../models/admission/model_1_elastic_net_tunned.pickle", "wb") as fp:   #Pickling
    pickle.dump(elastic_net_class, fp)