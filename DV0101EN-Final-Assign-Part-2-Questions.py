#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# Load Dataset
data = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/d51iMGfp_t0QpO30Lym-dw/automobile-sales.csv"
)

# ---------------------------------------------------------
# Create Dash App
app = dash.Dash(__name__)
app.title = "Automobile Sales Statistics Dashboard"

# ---------------------------------------------------------
# Dropdown Options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# Year List
year_list = [i for i in range(1980, 2014)]

# ---------------------------------------------------------
# Layout
app.layout = html.Div([

    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'fontSize': 24
        }
    ),

    html.Br(),

    # Dropdown 1
    html.Div([
        html.Label("Select Report Type:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Yearly Statistics',
            placeholder='Select a report type',
            style={
                'width': '80%',
                'padding': '3px',
                'fontSize': '20px',
                'textAlignLast': 'center'
            }
        )
    ]),

    html.Br(),

    # Dropdown 2
    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value=1980,
            placeholder='Select-year',
            style={
                'width': '80%',
                'padding': '3px',
                'fontSize': '20px',
                'textAlignLast': 'center'
            }
        )
    ]),

    html.Br(),

    # Output Container
    html.Div(
        id='output-container',
        className='chart-grid',
        style={
            'display': 'flex',
            'flexDirection': 'column',
            'width': '100%'
        }
    )

])

# ---------------------------------------------------------
# Callback 1: Enable / Disable Year Dropdown
@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True

# ---------------------------------------------------------
# Callback 2: Update Charts
@app.callback(
    Output('output-container', 'children'),
    [
        Input('dropdown-statistics', 'value'),
        Input('select-year', 'value')
    ]
)
def update_output_container(selected_statistics, input_year):

    # =====================================================
    # Recession Statistics
    if selected_statistics == 'Recession Period Statistics':

        recession_data = data[data['Recession'] == 1]

        # Plot 1
        yearly_rec = recession_data.groupby(
            'Year')['Automobile_Sales'].mean().reset_index()

        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x='Year',
                y='Automobile_Sales',
                title='Average Automobile Sales During Recession'
            )
        )

        # Plot 2
        average_sales = recession_data.groupby(
            'Vehicle_Type')['Automobile_Sales'].mean().reset_index()

        R_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title='Average Vehicles Sold by Vehicle Type'
            )
        )

        # Plot 3
        exp_rec = recession_data.groupby(
            'Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()

        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Advertisement Expenditure Share by Vehicle Type'
            )
        )

        # Plot 4
        unemp_data = recession_data.groupby(
            ['unemployment_rate', 'Vehicle_Type']
        )['Automobile_Sales'].mean().reset_index()

        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data,
                x='unemployment_rate',
                y='Automobile_Sales',
                color='Vehicle_Type',
                labels={
                    'unemployment_rate': 'Unemployment Rate',
                    'Automobile_Sales': 'Average Automobile Sales'
                },
                title='Effect of Unemployment Rate on Vehicle Type and Sales'
            )
        )

        return [

            html.Div(
                children=[R_chart1, R_chart2],
                style={'display': 'flex'}
            ),

            html.Div(
                children=[R_chart3, R_chart4],
                style={'display': 'flex'}
            )
        ]

    # =====================================================
    # Yearly Statistics
    elif selected_statistics == 'Yearly Statistics':

        yearly_data = data[data['Year'] == input_year]

        # Plot 1
        yas = data.groupby(
            'Year')['Automobile_Sales'].mean().reset_index()

        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x='Year',
                y='Automobile_Sales',
                title='Yearly Automobile Sales'
            )
        )

        # Plot 2
        mas = yearly_data.groupby(
            'Month')['Automobile_Sales'].sum().reset_index()

        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas,
                x='Month',
                y='Automobile_Sales',
                title='Total Monthly Automobile Sales'
            )
        )

        # Plot 3
        avr_vdata = yearly_data.groupby(
            'Vehicle_Type')['Automobile_Sales'].mean().reset_index()

        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)
            )
        )

        # Plot 4
        exp_data = yearly_data.groupby(
            'Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()

        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title='Total Advertisement Expenditure for Each Vehicle'
            )
        )

        return [

            html.Div(
                children=[Y_chart1, Y_chart2],
                style={'display': 'flex'}
            ),

            html.Div(
                children=[Y_chart3, Y_chart4],
                style={'display': 'flex'}
            )
        ]

    return None

# ---------------------------------------------------------
# Run App
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8050)