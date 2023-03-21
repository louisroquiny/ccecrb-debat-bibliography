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
item_list = []
for item in items:
    # get the first author's name if available
    try : 
        if 'name' in  item['data']['creators'][0] :
            author = item['data']['creators'][0]['name']
        if 'firstName' in item['data']['creators'][0]:
            author = item['data']['creators'][0]['firstName'] + ' ' + item['data']['creators'][0]['lastName']
        else:
            author = item['data']['creators'][0]['lastName']
        # create a dictionary for the item
        item_dict = {'Title' : item['data']['title'],
                     'Author': author,
                     'Type': item['data']['itemType'],
                     'Date': item['data']['date'],
                     'Link': item['data']['url']}
        item_list.append(item_dict)
   
    except KeyError :
        if 'name' in  item['data']['creators'][0] :
            author = item['data']['creators'][0]['name']
        if 'firstName' in item['data']['creators'][0]:
            author = item['data']['creators'][0]['firstName']
        # create a dictionary for the item
        item_dict = {'Title' : item['data']['title'],
                     'Author': author,
                     'Type': item['data']['itemType'],
                     'Date': item['data']['date'],
                     'Link': item['data']['url']}
        item_list.append(item_dict)
        
# create a Pandas DataFrame from the list of dictionaries
biblio = pd.DataFrame(item_list)

biblio["Date"] = pd.to_datetime(biblio["Date"], infer_datetime_format= True)
biblio["Date"] = biblio["Date"].dt.date

biblio.fillna("", inplace=True)

biblio.Link = biblio.Link.astype(str).apply(lambda x : '[Link]('+ x + ')' if len(x) > 0 else "" )

# biblio = biblio.astype(str)
biblio_to_display = biblio.sort_values('Date', ascending = False)

app_biblio = Dash(__name__, external_stylesheets=[dbc.themes.LITERA])
app = app_biblio.server
app_biblio.config.suppress_callback_exceptions = False

# Ajoutez un champ de recherche et un tableau à la page HTML
app_biblio.layout = dash_table.DataTable(
    biblio_to_display.to_dict("records"),
    #[{"name": i, "id": i} for i in biblio_to_display.columns],
    [{'id': x, 'name': x, 'presentation': 'markdown'} if x == 'Link' else {'id': x, 'name': x} for x in biblio_to_display.columns],
    filter_action="native",
    sort_action='native',
    sort_mode="multi",
    filter_options={"placeholder_text": "Filter column..."},
    # fixed_rows={'headers': True},
    page_size=15,
    style_table={
        'overflowX': 'auto',
        'height': '100%',
        # 'witdh' : 500
        },
    style_data={
    'whiteSpace': 'normal',
    'height': 'auto',
    },
    style_cell = {'font_size': '14px'},
    style_cell_conditional=[
        {
            'if': {'column_id': 'Title'},
            'textAlign': 'left'
        }, 
        {
            'if': {'column_id': 'Author'},
            'textAlign': 'left'
        }]
)

# Exécutez l'application
if __name__ == '__main__':
    app_biblio.run_server(debug=True)
