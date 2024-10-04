#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# List of years 
year_list = [i for i in range(1980, 2024)]

#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    # TASK 2.1 Add title to the dashboard
    html.H1(
        "Automobile Sales Statistics Dashboard", 
        style={'textAlign': 'center', 'color': '#B03D36', 'font-size': '24px'}
    ),
    
    # TASK 2.2: Add 2 dropdown menus
    html.Div([
        html.Label("Select Report Type:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value=None,
            placeholder='Select a report type',
            style={'width': '60%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}
        )
    ]),

    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': str(i), 'value': i} for i in year_list],
            value=None,
            placeholder='Select year',
            style={'width': '60%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'},
            disabled=True
        )
    ], id='year-dropdown-container'),
    
    html.Div(style={'height': '20px'}),

    html.Div(id='output-container', className='chart-grid', style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'center', 'gap': '20px'}),
])

# TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    [Output('year-dropdown-container', 'style'),
     Output('select-year', 'disabled')],
    Input('dropdown-statistics', 'value')
)
def update_year_dropdown_visibility(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return {'display': 'block'}, False
    else:
        return {'display': 'none'}, True

# Callback for plotting
@app.callback(
    Output('output-container', 'children'),
    [
        Input('dropdown-statistics', 'value'),
        Input('select-year', 'value')
    ]
)
def update_output_container(selected_statistics, selected_year):
    # Only update when a report type is selected
    if selected_statistics is None:
        return []
    
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

        # Plot 1: Automobile sales fluctuate over Recession Period (year-wise) using line chart
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        fig1 = px.line(yearly_rec, x='Year', y='Automobile_Sales', title="Average Automobile Sales Over Recession Period")
        fig1.update_layout(width=600, height=300, margin={'l': 30, 'r': 50, 't': 30, 'b': 30})
        R_chart1 = dcc.Graph(figure=fig1)

        # Plot 2: Average number of vehicles sold by vehicle type as a bar chart
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        fig2 = px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales', title="Average Number of Vehicles Sold by Vehicle Type during Recession")
        fig2.update_layout(width=600, height=300, margin={'l': 30, 'r': 50, 't': 30, 'b': 30})
        R_chart2 = dcc.Graph(figure=fig2)

        # Plot 3: Pie chart for total expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        fig3 = px.pie(exp_rec, values='Advertising_Expenditure', names='Vehicle_Type', title="Total Expenditure Share by Vehicle Type during Recession")
        fig3.update_layout(width=600, height=300, margin={'l': 30, 'r': 50, 't': 30, 'b': 30})
        R_chart3 = dcc.Graph(figure=fig3)

        # Plot 4: Bar chart for the effect of unemployment rate on vehicle type and sales
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        fig4 = px.bar(unemp_data, x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type', 
                       labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
                       title='Effect of Unemployment Rate on Vehicle Type and Sales')
        fig4.update_layout(width=600, height=300, margin={'l': 30, 'r': 50, 't': 30, 'b': 30})
        R_chart4 = dcc.Graph(figure=fig4)

        return [
            html.Div(className='chart-item', children=[R_chart1, R_chart2],
                     style={'display': 'flex', 'flex-direction': 'row', 'gap': '20px', 'justify-content': 'center'}),
            html.Div(className='chart-item', children=[R_chart3, R_chart4],
                     style={'display': 'flex', 'flex-direction': 'row', 'gap': '20px', 'justify-content': 'center'})
        ]

    elif selected_statistics == 'Yearly Statistics':
        if selected_year is None:
            return []  # No year selected, return empty list

        yearly_data = data[data['Year'] == selected_year]

        # Plot 1: Yearly Automobile sales using line chart
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        fig1 = px.line(yas, x='Year', y='Automobile_Sales', title="Yearly Average Automobile Sales")
        fig1.update_layout(width=600, height=300, margin={'l': 30, 'r': 50, 't': 30, 'b': 30})
        Y_chart1 = dcc.Graph(figure=fig1)

        # Plot 2: Total Monthly Automobile sales using line chart
        mas = data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        fig2 = px.line(mas, x='Month', y='Automobile_Sales', title='Total Monthly Automobile Sales')
        fig2.update_layout(width=600, height=300, margin={'l': 30, 'r': 50, 't': 30, 'b': 30})
        Y_chart2 = dcc.Graph(figure=fig2)

        # Plot 3: Average vehicles sold by vehicle type during selected year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        fig3 = px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales', title='Average Vehicles Sold by Vehicle Type in {}'.format(selected_year))
        fig3.update_layout(width=600, height=300, margin={'l': 30, 'r': 50, 't': 30, 'b': 30})
        Y_chart3 = dcc.Graph(figure=fig3)

        # Plot 4: Total Advertisement Expenditure for each vehicle using pie chart
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        fig4 = px.pie(exp_data, values='Advertising_Expenditure', names='Vehicle_Type', title='Total Advertisement Expenditure for Each Vehicle')
        fig4.update_layout(width=600, height=300, margin={'l': 30, 'r': 50, 't': 30, 'b': 30})
        Y_chart4 = dcc.Graph(figure=fig4)

        return [
            html.Div(className='chart-item', children=[Y_chart1, Y_chart2], 
                     style={'display': 'flex', 'flex-direction': 'row', 'gap': '20px', 'justify-content': 'center'}),
            html.Div(className='chart-item', children=[Y_chart3, Y_chart4], 
                     style={'display': 'flex', 'flex-direction': 'row', 'gap': '20px', 'justify-content': 'center'})
        ]
    else:
        return []  # Return an empty list if no valid selection is made

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
