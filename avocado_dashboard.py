import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Output, Input
import numpy as np

avocado = pd.read_csv('csv/avocado.csv')
app = Dash()

app.layout = html.Div([
    html.H1("Avocado Prices Dashboard", style={'textAlign': 'center', 'color': 'darkblue'}),
    dcc.Dropdown(id='geography-dropdown',
                 options=avocado['geography'].unique(),
                 value='New York'),
    dcc.Graph(id='price-graph')
])

@app.callback(
    Output('price-graph', 'figure'),
    Input('geography-dropdown', 'value')
)

def update_graph(selected_geography):
    filtered_avocado = avocado[avocado['geography']==selected_geography]
    fig = px.line(filtered_avocado, x='date', y='average_price', color='type',
                  title=f'Avocado Prices in {selected_geography}')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)