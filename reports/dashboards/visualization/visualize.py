import seaborn as sns
import plotly.express as px

def correlation_plot(df):
    correlations = df.corr()
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

def logistic_regression_plot(regression_df):
    '''
    Plots a logistic regression plot of the provided df.
    '''
    plot = px.scatter(regression_df, x='rowname', y='fitted', color='admitted')