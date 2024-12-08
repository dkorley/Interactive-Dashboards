import pandas as pd
from dash import Dash, dcc, Input, Output, html, State
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

# Load data
life = pd.read_csv('csv/life_expectancy.csv')
year_min = life['year'].min()
year_max = life['year'].max()

# Navbar
navbar = dbc.NavbarSimple(
    brand='Life Expectancy Dashboard',
    brand_style={'fontSize': 40, 'color': 'white'},
    children=[
        html.A('Data Source',
               href='https://ourworldindata.org/life-expectancy',
               target='_blank',
               style={'color': 'black'})
    ],
    color='primary',
    fluid=True,
    sticky='top'
)

# Range Slider
year_slider = dcc.RangeSlider(
    id='year-slider',
    min=year_min,
    max=year_max,
    value=[year_min, year_max],
    marks={i: str(i) for i in range(year_min, year_max + 1, 10)},
    step=1,
    tooltip={'placement': 'top', 'always_visible': True}
)

# Input Card
input_card = dbc.Card(
    [
        html.H5('Life expectancy by countries'),
        year_slider
    ],
    body=True,
    style={'textAlign': 'center', 'color': 'white'},
    color='primary'
)

# App layout
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    navbar,
    input_card,
    html.Br(),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in life['country'].unique()],
        multi=True
    ),
    html.Br(),
    html.Button(id='submit-button', children='Submit'),
    html.Br(),
    dcc.Graph(id='life-expectancy-graph')
])

# Callback
@app.callback(
    Output('life-expectancy-graph', 'figure'),
    Input('submit-button', 'n_clicks'),
    State('country-dropdown', 'value'),
    State('year-slider', 'value')
)
def update_output(button_click, selected_country, selected_years):
    if not selected_country:
        raise PreventUpdate
    msk = (life['country'].isin(selected_country)) & \
          (life['year'] >= selected_years[0]) & \
          (life['year'] <= selected_years[1])
    life_expectancy_filtered = life[msk]
    line_fig = px.line(
        life_expectancy_filtered,
        x='year', y='life expectancy',
        title='Life Expectancy by Country',
        color='country'
    )
    return line_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
