pip install 'Dash'==1.13.4

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Load Data
url = 'https://raw.githubusercontent.com/erick2024/educationstatistics/master/Education%20World%20Bank%20Stacked%20Area%20Graph%20Data%20-%20Sheet1.csv'
df = pd.read_csv(url, index_col = 'Year').stack()
df = df.reset_index()
df.columns = ['Year', 'Region', 'Value']

# Build App
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    html.H3("Gross Intake Rate at Grade 1"),
        html.Div([
        dcc.Dropdown(
            id='region',
            value=['North America'], options=[
                {'label': c, 'value': c}
                for c in df.Region.unique()
            ], multi = True),
    ],style={'display': 'inline', 'width': '15%'}),
        
        html.Div([
        dcc.Graph(id='graph'),
    ],style={'display': 'inline-block', 'width': '45%'}),
        
        html.Div([
        dcc.Graph(id='graph_2'),
    ],style={'display': 'inline-block', 'width': '55%'})
])

# Define callback to update graph
@app.callback(
    [dash.dependencies.Output('graph', 'figure'),dash.dependencies.Output('graph_2', 'figure')],
    [dash.dependencies.Input('region', 'value')]
)


def multi_output(region):

    df_query = df.query('Region == '+str(region))

    fig1 = px.line(df_query, x='Year', y='Value', color = 'Region')
    fig2 = px.area(df_query, x='Year', y='Value', color = 'Region')
    
    fig1.update_layout(
    yaxis_title='Gross Intake Rate at Grade 1',
    showlegend = False,
    )
    
    fig2.update_layout(
    yaxis_title='Gross Intake Rate at Grade 1',
    )

    fig1.update_xaxes(showspikes=True)
    fig1.update_yaxes(showspikes=True)

    return fig1, fig2


# Run app
if __name__ == '__main__':
    app.run_server(debug = True)
