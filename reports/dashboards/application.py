import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, dash_table
import pandas as pd
import plotly.express as px
import dash_labs as dl
import pickle


app = dash.Dash(__name__, plugins=[dl.plugins.pages], external_stylesheets=[dbc.themes.FLATLY],)
#app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


# the style arguments for the sidebar. We use position:fixed and a fixed width

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 130,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


################################################################################################
# Load the data and create the map
################################################################################################

df = pd.read_csv('../../data/raw/superstore.csv', parse_dates=['Order Date', 'Ship Date'])
raw_er_admission = pd.read_excel('../../data/raw/er_admission.xlsx', sheet_name = 'Data')

##Create ScatterPlot of variable correlations:

#corr_variables = visualize.correlation_plot(raw_er_admission)

correlations = raw_er_admission.corr()
corr_variables = px.imshow(correlations, text_auto = True, aspect = 'auto')

corr_variables.update_layout(
    title="Variables Correlation"
)

##Histogram for admitted and stay length

graph_hist = raw_er_admission.loc[:,['Stay_length','Gender']]
graph_hist['Gender'] = graph_hist['Gender'].apply(lambda x: "Female" if(x == 1) else "Male")
graph_hist
 
hist_fig = px.histogram(graph_hist, x="Stay_length", color="Gender")

##DataTable to change later (its just an example of a table)

table_df = raw_er_admission.loc[:,['Gender','Age_band','Stay_length','Admission_ALL']].head()

## Create the TreeMap

Treemap_fig = px.treemap(
    df,
    path=["Category", "Sub-Category", "State"],
    values="Sales",
    color_discrete_sequence=px.colors.qualitative.Dark24,
)

#Create the Scatter_fig
Scatter_fig = px.scatter(
    df,
    x="Sales",
    y="Profit",
    color="Category",
    hover_data=["State", "Sub-Category", "Order ID", "Product Name"],
)
Scatter_fig.update_layout(
    title="Sales vs. Profit in selected states", paper_bgcolor="#F8F9F9"
)

################################################################################################
# Load the model
################################################################################################
with open('../../models/admission/model_1_elastic_net_tunned.pickle', 'rb') as f:
    model = pickle.load(f)

################################################################################################
# Transform the data
################################################################################################
# %% analyize missingess
# impute 3, this new category will mean that there it is not know if the patient has a sensitive condition
er_admission = raw_er_admission.copy()
er_admission['ACSC'] = raw_er_admission['ACSC'].fillna(3)
# impute category 5 (unknown) to the ethnicity variable
er_admission['Ethnicity'] = raw_er_admission['Ethnicity'].fillna(5)
# drop the other null values, only 24 records will be discarded
er_admission = er_admission.dropna()
# get dummies
adm_dummies = pd.get_dummies(er_admission, 
                            columns=['Site','Age_band','IMD_quintile','Ethnicity', 'ACSC'], 
                            drop_first=True)
adm_dummies = adm_dummies.drop(['Admission_ALL', 'Stay_length'], axis = 1)
adm_dummies.head()
# %%
################################################################################################
# Run the tunned model with the selected data
################################################################################################
y_prob =model.predict_proba(adm_dummies) 
y_pred = (y_prob[:,1] >= 0.25).astype(int)

#Top menu, items get from all pages registered with plugin.pages

navbar = dbc.NavbarSimple([

    dbc.NavItem(dbc.NavLink( "Home", href='/')),
    dbc.NavItem(dbc.NavLink( "Dashboard", href='/dashboard')),
    dbc.NavItem(dbc.NavLink( "Descriptive Analytics", href="/analytics")),
    dbc.NavItem(dbc.NavLink( "The Model", href="/the-model")),
    # dbc.DropdownMenu(
    #     [

    #         dbc.DropdownMenuItem(page["name"], href=page["path"])
    #         for page in dash.page_registry.values()
    #         if page["module"] != "pages.not_found_404"
    #     ],
    #     nav=True,
    #     label="Descriptive Analytics",
    # ),
    dbc.NavItem(dbc.NavLink("The Team", href="/the-team")),
    ],
    brand="DS4A Project - Team 62",
    color="primary",
    dark=True,
    className="mb-2",
)

## Content###

content = html.Div(id="page-content", style=CONTENT_STYLE)

### Layout####
app.layout = html.Div(
    [
    dbc.Row(
            [
                html.H1('CLINICAL OUTCOME RISK ASSESTMENT TOOL',style={'textAlign': 'center'}),
                html.Hr()
                ],
            className = 'title'
            ),
    dbc.Container(
    [
        navbar,
        dl.plugins.page_container,
    ],
    className="dbc",
    fluid=True,
    ),
    ]
)

if __name__ == "__main__":
    app.run_server(port=8888)