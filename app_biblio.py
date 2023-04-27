# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 10:46:45 2023

@author: loro
"""

# Importez les bibliothèques nécessaires
import json
import dash
from dash import Dash, html, dcc, Input, Output, dash_table
import pandas as pd
import dash_bootstrap_components as dbc
from pyzotero import zotero
from assets.credentials import library_id, library_type, api_key

zot = zotero.Zotero(library_id, library_type, api_key)

# retrieve the items from your library and specify the fields to include
items = zot.everything(zot.top())
        
# create a list of dictionaries representing the items
item_list = [{'Title': item['data']['title'],
              'Author': item['data']['creators'][0].get('name', '') or \
                        item['data']['creators'][0].get('firstName', '') + ' ' + \
                        item['data']['creators'][0].get('lastName', ''),
              'Date': item['data'].get('date', ''),
              'Link': item['data'].get('url', '')} for item in items]
    
for item in items: 
    print(item['data']['tags']).get('tag')
    
# create a Pandas DataFrame from the list of dictionaries
biblio = pd.DataFrame(item_list)    

# Convert the Date column to datetime and fill missing values
biblio["Date"] = pd.to_datetime(biblio["Date"], infer_datetime_format= True, dayfirst=True).dt.date

# Sort the DataFrame by date
biblio_to_display = biblio.sort_values('Date', ascending = False, na_position = 'first')
biblio_to_display.fillna("", inplace=True)

# Create a link column with markdown formatting
biblio_to_display.Link = biblio_to_display.Link.astype(str).apply(lambda x : '[Download]('+ x + ')' if len(x) > 0 else "" )

app_biblio = Dash(__name__, external_stylesheets=[dbc.themes.LITERA])
app = app_biblio.server
app_biblio.config.suppress_callback_exceptions = False

app_biblio.layout = dash_table.DataTable(
    data=biblio_to_display.to_dict('records'),
    columns=[{'id': x, 'name': x, 'presentation': 'markdown'} if x == 'Link' else {'id': x, 'name': x} for x in biblio_to_display.columns],
    filter_action='native',
    sort_action='native',
    sort_mode='multi',
    filter_options={'placeholder_text': 'Filter column...'},
    page_size=15,
    style_table={
        'overflowX': 'auto',
        'padding': '10px', # Add padding to table cells
        # 'border': '1px solid black', # Add a border to the table
        'backgroundColor': 'white', # Set background color to white
        'textAlign': 'center' # Center table content
    },
    style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
        'border': '1px solid black', # Add border to table rows
    },
    style_cell={
        'font-family': 'Calibri',
        'font_size': '15px',
        'textAlign': 'center', # Center cell text
        'padding': '5px', # Add cell padding
        'backgroundColor': '#FFFFFF', # Set cell background color
    },
    style_cell_conditional=[
        {
            'if': {'column_id': 'Title'},
            'textAlign': 'left'
        }, 
        {
            'if': {'column_id': 'Author'},
            'textAlign': 'left'
        }
    ],
    style_header={
        'backgroundColor': '#c7c7c7', # Set header background color
        'color': 'white', # Set header font color to white
        'fontWeight': 'bold', # Set header font weight to bold
        'border': '1px solid black', # Add border to header cells
        'padding': '5px', # Add header cell padding
    },
    page_action='native', # Enable pagination
    page_current=0, # Set current page to 0

)


# Exécutez l'application
if __name__ == '__main__':
    app_biblio.run_server(debug=True)
