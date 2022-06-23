import seaborn as sns
import plotly.express as px

def correlation_plot(df):
    correlations = df.corr()
    sns.set(rc={'figure.figsize':(12, 12)})
    sns.heatmap(correlations, cmap = "Blues")

def age_band_plot(df):
    '''
    Plots a bar chart from a dataframe loaded by user, that has
    a field called 'Age_band' according to data dictionary.
    '''
    plot_df=df['Age_band'].value_counts().to_frame().reset_index()
    dict={0 : '16-34', 1 : '35-64', 2: '65-84', 3 : '85 and over'}
    plot_df=plot_df.replace({'index': dict})
    plot_df.rename(columns={'index':'age_band', 'Age_band':'patients_count'}, inplace=True)
    plot_df.head()
    px.bar(plot_df,x='age_band', y='patients_count', 
        color_discrete_sequence =['cyan']*len(plot_df), 
        title='Age band count', text_auto=True)