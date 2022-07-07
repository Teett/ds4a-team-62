# %% libraries
from pyexpat import model
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import ElasticNetCV
from sklearn.metrics import mean_squared_error
import numpy as np
import seaborn as sns
import pickle

# %% read data 
X_train = pd.read_pickle('../../data/processed/stay/X_train_stay.pickle')
X_test = pd.read_pickle('../../data/processed/stay/X_test_stay.pickle')
y_train = pd.read_pickle('../../data/processed/stay/y_train_stay.pickle')
y_test = pd.read_pickle('../../data/processed/stay/y_test_stay.pickle')


sns.histplot(data = pd.DataFrame(y_train), x = "Stay_length")
#%%
modelo = ElasticNetCV(
            l1_ratio        = [0, 0.1, 0.5, 0.7, 0.9, 0.95, 0.99],
            alphas          = np.logspace(-10, 3, 100),
            cv              = 5,
            random_state    = 1995,  
            max_iter        = 4500,
            n_jobs          = 4
         )

y_train_transformed = np.log(y_train + 1)
modelo = modelo.fit(X = X_train, y = y_train)


#%%
mean_error_cv = modelo.mse_path_.mean(axis =2)

df_resultados_cv = pd.DataFrame(
                        data   = mean_error_cv.flatten(),
                        index  = pd.MultiIndex.from_product(
                                    iterables = [modelo.l1_ratio, modelo.alphas_],
                                    names     = ['l1_ratio', 'modelo.alphas_']
                                 ),
                        columns = ["mse_cv"]
                    )

df_resultados_cv['rmse_cv'] = np.sqrt(df_resultados_cv['mse_cv'])
df_resultados_cv = df_resultados_cv.reset_index().sort_values('mse_cv', ascending = True)
df_resultados_cv


#%%
fig, ax = plt.subplots(figsize=(7, 3.84))
df_resultados_cv.groupby('l1_ratio')['rmse_cv'].min().plot(ax = ax)
ax.set_title('Evolución del error CV en función de la l1_ratio')
ax.set_xlabel('l1_ratio')
ax.set_ylabel('rmse_cv');

print(f"Mejor valor de alpha encontrado: {modelo.alpha_}")
print(f"Mejor valor de l1_ratio encontrado: {modelo.l1_ratio_}")


df_coeficientes = pd.DataFrame(
                        {'predictor': X_train.columns,
                         'coef': modelo.coef_.flatten()}
                  )


#%%
fig, ax = plt.subplots(figsize=(11, 3.84))
ax.stem(df_coeficientes.predictor, df_coeficientes.coef, markerfmt=' ')
plt.xticks(rotation=90, ha='right', size=5)
ax.set_xlabel('variable')
ax.set_ylabel('coeficientes')
ax.set_title('Coeficientes del modelo');


#%%
# Predicciones test
predicciones = modelo.predict(X=X_test)
predicciones = predicciones.flatten()

df_pred = pd.DataFrame({"pred": predicciones})
df_pred["pred_exp"] = np.exp(df_pred.pred) - 1


rmse_elastic = mean_squared_error(
                y_true  = y_test,
                y_pred  = predicciones,
                squared = False
               )
print(f"El error (rmse) de test es: {rmse_elastic}")
# %%
with open("../../models/admission/reg_elastic_net.pickle", "wb") as fp:   #Pickling
    pickle.dump(model, fp)
