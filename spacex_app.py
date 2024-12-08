# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import wget

# Download the CSV file
space_launch_dash = wget.download("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv(space_launch_dash)
spacex_df.drop('Unnamed: 0', axis=1, inplace=True)

# Calculate min and max payload for later use
min_payload = spacex_df['Payload Mass (kg)'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()

# Create options for dropdown list
options = [{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()]

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # Dropdown list for Launch Site selection
    dcc.Dropdown(id='site-dropdown',
                 options=options,
                 value='ALL',
                 placeholder='Select a Launch Site here',
                 searchable=True),
    html.Br(),
    
    # Pie chart to show successful launches count
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    
    # Slider for payload range selection
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(id='payload-slider',
                    min=min_payload, max=max_payload, step=1000,
                    marks={min_payload: str(min_payload), max_payload: str(max_payload)},
                    value=[min_payload, max_payload]),
    html.Br(),
    
    # Scatter chart to show correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# Callback function for pie chart
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        data = filtered_df.groupby('Launch Site')['class'].mean()
        # Create pie chart
        fig = px.pie(data, values='class', names=filtered_df['Launch Site'].unique(),
                     title='Success Rate for All Launch Sites')
        return fig
    else:
        # Calculate successful launch count for the selected site
        data = filtered_df[spacex_df['Launch Site'] == entered_site]['class'].value_counts().reset_index()
        data.columns = ['class', 'pie chart values']
        data['pie chart names'] = data['class'].map({1: 'Success', 0: 'Failure'})
        # Create pie chart
        fig = px.pie(data, values='pie chart values', names='pie chart names',
                     title=f'Success Rate for Launch Site {entered_site}')
        return fig

# Callback function for scatter chart
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])

def get_scatter_chart(entered_site, payload_range):
    min_payload, max_payload = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= min_payload) & (spacex_df['Payload Mass (kg)'] <= max_payload)]
    if entered_site == 'ALL':
        # Create scatter chart for all sites
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category', title='Payload vs. Success Rate for All Launch Sites')
        return fig
    else:
        # Create scatter chart for the selected site
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category', title=f'Payload vs. Success Rate for Launch Site {entered_site}')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
