import seaborn as sns

def correlation_plot(df):
    correlations = df.corr()
    sns.set(rc={'figure.figsize':(12, 12)})
    sns.heatmap(correlations, cmap = "Blues")