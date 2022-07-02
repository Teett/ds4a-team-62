import requests
import pandas as pd

def get_generate_df ():
    url = 'http://localhost:5000/consulta_admisiones_de_hoy'
    r = requests.get(url)
    response = r.json()

    daily_admissions = pd.DataFrame.from_dict(data = response['Respuesta'])
    
    daily_admissions.drop(['Stay_length','Admission_ALL','createdAt','currentDate','id','nombreArchivo','updatedAt'], axis = 1, inplace = True)
    daily_admissions.rename(columns = {'Inpatient_beoccupancy': 'Inpatient_bed_occupancy'}, inplace = True)

    daily_admissions = daily_admissions.astype({"ACSC": float,
                                                "Age_band": float,
                                                "Ethnicity": float,
                                                "Site": float,
                                                "IMD_quintile": float,
                                                "DayWeek_coded": int,
                                                "Shift_coded": int,
                                                "Arr_Amb": int,
                                                "Gender": int,
                                                "Consultant_on_duty": int,
                                                "ED bed occupancy": float,
                                                "Inpatient_bed_occupancy": float,
                                                "Arrival intensity": int,
                                                "LAS intensity": float,
                                                "LWBS intensity": float,
                                                "Last_10_mins": int})
    return daily_admissions
