import pandas as pd
from dash import Dash, dcc, html, dash_table, Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

electricity = pd.read_csv('csv/electricity.csv')

year_min = electricity['Year'].min()
year_max = electricity['Year'].max()

app = Dash(external_stylesheets=[dbc.themes.SOLAR])

app.layout = html.Div([
    html.H1("Electricity Prices by US State"),
    dcc.RangeSlider(
        id='year-slider',
        min= year_min,
        max= year_max,
        value=[year_min, year_max],
        marks={i:str(i) for i in range(year_min, year_max+1)}
    ),
    dcc.Graph(id='map-graph'),
    dash_table.DataTable(id='price-info')
])

@app.callback(
    Output('map-graph', 'figure'),
    Input('year-slider', 'value')
)

def update_map(selected_years):
    filtered_data = electricity[(electricity['Year'] >= selected_years[0]) & (electricity['Year'] <= selected_years[1])]
    avg_px_electricity = filtered_data.groupby('US_State')['Residential Price'].mean().reset_index()

    map_fig = px.choropleth(avg_px_electricity,
                            locations='US_State',
                            locationmode='USA-states',
                            color='Residential Price',
                            scope='usa',
                            color_continuous_scale='reds')
    return map_fig

@app.callback(
    Output('price-info', 'data'),
    Input('map-graph', 'clickData'),
    Input('year-slider', 'value')
)

def update_datatable(clicked_data, selected_years):
    if clicked_data is None:
        return []
    else:
        us_state = clicked_data['points'][0]['location']
        filtered_electricity = electricity[(electricity['Year'] >= selected_years[0]) &
                                        (electricity['Year'] <= selected_years[1]) &    
            (electricity['US_State']==us_state)]
    return filtered_electricity.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)