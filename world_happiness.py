import pandas as pd
import numpy as np
from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px

happiness = pd.read_csv("csv/world_happiness.csv")

app = Dash()

app.layout = html.Div([
    html.H1('World Happiness Dashboard', style={'textAlign': 'center'}),
    html.P(['This dashboard shows the happiness score.',
            html.Br(),
            html.A('World Happiness Report Data Source',
                   href='https://worldhappiness.report',
                   target="_blank")],
                   style={'textAlign': 'center'}),
    dcc.RadioItems(id='region-radio', 
                   options = happiness['region'].unique(),
                    value='North America',
                    labelStyle={'display': 'inline-block', 'margin-right': '10px'}, style={'margin-bottom': '20px'}),
    dcc.Dropdown(id='country-dropdown'),
    dcc.RadioItems(id='happiness-radio', 
                   options = {
        'happiness_score': 'Happiness Score',
        'happiness_rank': 'Happiness Rank'
    },
                   value='happiness_score',
                   labelStyle={'display': 'inline-block', 'margin-right': '10px'}, style={'margin-bottom': '20px'}),
    
    html.Br(),
    html.Button(
        id='submit-button',
        n_clicks=0,
        children='Update the output'
    ),
    dcc.Graph(id='graph'),
    html.Div(id='average-div')
])

@app.callback(
       Output('country-dropdown', 'options'),
       Output('country-dropdown', 'value'),
       Input('region-radio', 'value')
)

def update_dropdown(selected_region):
    filtered_data = happiness[happiness['region'] == selected_region]
    country_options = filtered_data['country'].unique()
    return country_options, country_options[0]

@app.callback(
    Output('graph', 'figure'),
    Output('average-div', 'children'),
    Input('submit-button', 'n_clicks'),
    State('country-dropdown', 'value'),
    State('happiness-radio', 'value')
)

def update_graph(button_click, selected_country, selected_data):
    filtered_data = happiness[happiness['country'] == selected_country]
    line_fig = px.line(filtered_data, x='year', y=selected_data,
                       title=f'{selected_data} in {selected_country}')
    selected_avg = filtered_data[selected_data].mean()
    return line_fig, f'The average {selected_data} for {selected_country} is {selected_avg}'

if __name__ == "__main__":
    app.run_server(debug=True)