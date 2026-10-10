
# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read SpaceX launch data into a Pandas DataFrame
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Find minimum and maximum payload
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a Dash application
app = dash.Dash(__name__)

# Create the application layout
app.layout = html.Div(children=[
    html.H1(
        'SpaceX Launch Records Dashboard',
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'font-size': 40
        }
    ),

    # TASK 1: Launch Site Dropdown
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'}
        ] + [
            {'label': site, 'value': site}
            for site in spacex_df['Launch Site'].unique()
        ],
        value='ALL',
        placeholder='Select a Launch Site here',
        searchable=True
    ),

    html.Br(),

    # TASK 2: Success Pie Chart
    html.Div(
        dcc.Graph(id='success-pie-chart')
    ),

    html.Br(),

    # TASK 3: Payload Range Slider
    html.P("Payload range (Kg):"),

    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={
            0: '0',
            1000: '1000',
            2000: '2000',
            3000: '3000',
            4000: '4000',
            5000: '5000',
            6000: '6000',
            7000: '7000',
            8000: '8000',
            9000: '9000',
            10000: '10000'
        },
        value=[min_payload, max_payload]
    ),

    html.Br(),

    # TASK 4: Payload vs Landing Success Scatter Chart
    html.Div(
        dcc.Graph(id='success-payload-scatter-chart')
    )
])


# TASK 2: Callback for Success Pie Chart
@app.callback(
    Output(
        component_id='success-pie-chart',
        component_property='figure'
    ),
    Input(
        component_id='site-dropdown',
        component_property='value'
    )
)
def get_pie_chart(entered_site):

    if entered_site == 'ALL':
        # Show successful launch counts for all sites
        success_df = spacex_df[spacex_df['class'] == 1]

        fig = px.pie(
            success_df,
            names='Launch Site',
            title='Total Successful Launches for All Sites'
        )

    else:
        # Filter data for the selected launch site
        filtered_df = spacex_df[
            spacex_df['Launch Site'] == entered_site
        ]

        # Show successful and failed launch counts
        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Success vs Failed Launches for {entered_site}'
        )

    return fig


# TASK 4: Callback for Payload Scatter Chart
@app.callback(
    Output(
        component_id='success-payload-scatter-chart',
        component_property='figure'
    ),
    [
        Input(
            component_id='site-dropdown',
            component_property='value'
        ),
        Input(
            component_id='payload-slider',
            component_property='value'
        )
    ]
)
def get_scatter_chart(entered_site, payload_range):

    # Get selected payload range
    low, high = payload_range

    # Filter records by payload range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    # If a specific site is selected, filter by site too
    if entered_site != 'ALL':
        filtered_df = filtered_df[
            filtered_df['Launch Site'] == entered_site
        ]

    # Create scatter plot
    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Payload Mass vs. Landing Success',
        labels={
            'Payload Mass (kg)': 'Payload Mass (kg)',
            'class': 'Landing Success (0 = Failure, 1 = Success)',
            'Booster Version Category': 'Booster Version'
        }
    )

    return fig


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
