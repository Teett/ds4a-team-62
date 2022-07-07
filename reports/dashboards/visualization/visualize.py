import plotly.express as px
import pandas as pd

def correlation_plot(df):
    corr_df = df.copy()
    corr_df.drop(['Consultant_on_duty','DayWeek_coded','Inpatient_bed_occupancy'], axis = 1, inplace = True)
    correlations = corr_df.corr()
    corr_plot = px.imshow(correlations, text_auto = True, aspect = 'auto')
    corr_plot.update_layout(title="Variables Correlation")
    return corr_plot

def ageband_plot(df):
    '''
    Plots a bar chart from a dataframe loaded by user, that has
    fields 'Age_band' and 'Gender' according to data dictionary
    '''
    plot_df = df[['Age_band', 'Gender']].value_counts().to_frame().reset_index()
    dict_age = {0: '16-34',
                1: '35-64',
                2: '65-84',
                3: '85 and over'}
    plot_df = plot_df.replace({'Age_band': dict_age})
    dict_gen = {0: 'male', 1: 'female'}
    plot_df = plot_df.replace({'Gender': dict_gen})
    plot_df.rename(columns={'Age_band': 'age_band',
                            'Gender': 'gender',
                            0: 'patients_count'}, inplace=True)
    plot=px.bar(plot_df, x='age_band', y='patients_count',
                color='gender', width=600, height=400,
                color_discrete_sequence=px.colors.qualitative.Pastel,
                title='Age band count', text_auto=True)
    return plot

def imdquintile_plot(df):
    '''
    Plots a bar chart from a dataframe loaded by user, that has
    fields 'IMD_quintile' and 'Gender' according to data dictionary
    '''
    plot_df = df[['IMD_quintile', 'Gender']].value_counts().to_frame().reset_index()
    dict_imd = {0: 'not deprived',
                1: '1st quintile',
                2: '2nd quintile',
                3: '3rd quintile',
                4: '4th quintile',
                5: '5th quintile'}
    plot_df = plot_df.replace({'IMD_quintile': dict_imd})
    dict_gen = {0: 'male', 1: 'female'}
    plot_df = plot_df.replace({'Gender': dict_gen})
    plot_df.rename(columns={'Gender': 'gender',
                            0: 'patients_count'}, inplace=True)
    plot=px.bar(plot_df, x='IMD_quintile', y='patients_count',
                color='gender', width=600, height=400,
                color_discrete_sequence=px.colors.qualitative.Pastel,
                title='Index of multiple deprivation quintiles', text_auto=True)
    plot.update_xaxes(tickangle=90)
    return plot

def ethnicity_plot(df):
    '''
    Plots a bar chart from a dataframe loaded by user, that has
    fields 'Ethnicity' and 'Gender' according to data dictionary
    '''
    plot_df = df[['Ethnicity', 'Gender']].value_counts().to_frame().reset_index()
    dict_etn = {1: 'asian',
                2: 'black',
                3: 'mixed',
                4: 'other',
                5: 'unknown',
                6: 'white'}
    plot_df = plot_df.replace({'Ethnicity': dict_etn})
    dict_gen = {0: 'male', 1: 'female'}
    plot_df = plot_df.replace({'Gender': dict_gen})
    plot_df.rename(columns={'Ethnicity': 'ethnicity',
                            'Gender': 'gender',
                            0: 'patients_count'}, inplace=True)
    plot=px.bar(plot_df, x='ethnicity', y='patients_count',
                color='gender', width=600, height=400,
                color_discrete_sequence=px.colors.qualitative.Pastel,
                title='Ethnicity count', text_auto=True)
    return plot

def acsc_plot(df):
    '''
    Plots a bar chart from a dataframe loaded by user, that has
    fields 'ACSC' and 'Gender' according to data dictionary
    '''
    plot_df = df[['ACSC', 'Gender']].value_counts().to_frame().reset_index()
    dict_acs = {0: 'True',
                1: 'False',
                3: 'unknown'}
    plot_df = plot_df.replace({'ACSC': dict_acs})
    dict_gen = {0: 'male', 1: 'female'}
    plot_df = plot_df.replace({'Gender': dict_gen})
    plot_df.rename(columns={'Gender': 'gender',
                            0: 'patients_count'}, inplace=True)
    plot=px.bar(plot_df, x='ACSC', y='patients_count',
                color='gender', width=600, height=400,
                color_discrete_sequence=px.colors.qualitative.Pastel,
                title='Presentation because of an ambulatory care sensitive condition', 
                text_auto=True)
    return plot

def patients_per_week(df):
    plot_df = df[['DayWeek_coded', 'Shift_coded']].value_counts().to_frame().reset_index()
    dict_week = { 1: 'Monday',
                2: 'Tuesday',
                3: 'Wednesday',
                4: 'Thursday',
                5: 'Friday',
                6: 'Saturday',
                7: 'Sunday'  }
    plot_df = plot_df.replace({'DayWeek_coded': dict_week})
    dict_shift = {0: 'Night', 1: 'Day'}
    plot_df = plot_df.replace({'Shift_coded': dict_shift})
    plot_df
    plot_df.rename(columns={'DayWeek_coded': 'Day of Week', 'Shift_coded': 'Shift', 0: 'patients_count'}, inplace=True)
    plot=px.bar(plot_df, x='Day of Week', y='patients_count',
                color='Shift',
                color_discrete_sequence=px.colors.qualitative.Pastel,
                title='Amount of patiens per day of Week', 
                text_auto=True)
    return plot

def ambulance_ratio_week(df):
    plot_df = df.groupby(['DayWeek_coded','Shift_coded']).mean()['LAS intensity'].to_frame().reset_index()
    dict_week = { 1: 'Monday',
                2: 'Tuesday',
                3: 'Wednesday',
                4: 'Thursday',
                5: 'Friday',
                6: 'Saturday',
                7: 'Sunday'  }
    plot_df = plot_df.replace({'DayWeek_coded': dict_week})
    dict_shift = {0: 'Night', 1: 'Day'}
    plot_df = plot_df.replace({'Shift_coded': dict_shift})
    plot_df
    plot_df.rename(columns={'DayWeek_coded': 'Day of Week', 'Shift_coded': 'Shift'}, inplace=True)
    plot=px.bar(plot_df, x='Day of Week', y='LAS intensity',
                color='Shift',
                #color_discrete_sequence=px.colors.qualitative.Pastel,
                title='Arrival by ambulance ratio per day of week', 
                text_auto=True,
                )
    return plot

def ambulance_shift_ratio(df):
    plot_df = df.groupby('Shift_coded').mean()['LAS intensity'].to_frame().reset_index()
    dict_shift = {0: 'Night', 1: 'Day'}
    plot_df = plot_df.replace({'Shift_coded': dict_shift})
    plot = px.bar(plot_df, x = 'LAS intensity', y ='Shift_coded', orientation = 'h', title = 'Ratio of arrivals by ambulance in each Shift')
    plot.update_layout( yaxis_title= "Shift", xaxis_title = 'Ambulance Arrival Intensity Ratio')
    return plot

def admissions_plot(pred_result,df):
    y_pred_list = pred_result.tolist()
    df['Status'] = y_pred_list
    plot_df = df[['Site', 'Status']].value_counts().to_frame().reset_index()
    dict_site = {  1: 'Site 1',
                2: 'Site 2',
                3: 'Site 3' }
    plot_df = plot_df.replace({'Site': dict_site})
    dict_admissions = {0: 'Expected Admission', 1: 'Might Not be Admitted'}
    plot_df = plot_df.replace({'Status': dict_admissions})
    plot_df
    plot_df.rename(columns={0: 'patients_count'}, inplace=True)
    plot=px.bar(plot_df, x='Site', y='patients_count',
                color='Status',
                title='Admissions Predictions', 
                text_auto=True)
    return plot

def logistic_regression_plot(regression_df, color = 'y_pred', opacity = 0.8):
    '''
    Plots a logistic regression plot of the provided df.
    '''
    #plot_df = regression_df.sort_values(by = ['y_prob'])
    regression_df.y_pred = regression_df.y_pred.astype(str)
    plot = px.scatter(regression_df, x='row_number', y='y_prob', color=color, 
                      opacity = opacity, height = 1000, width = 1200)
    plot.update_layout(shapes=[
    # adds line at y=5
    dict(
      type= 'line',
      xref= 'paper', x0= 0, x1= 1,
      yref= 'y', y0= 0.25, y1= 0.25,
      line = dict(color = 'Red')
    )
    ])
    plot.update_traces(marker={'size': 15})
    return plot