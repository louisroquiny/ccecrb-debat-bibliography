# ccecrb-debat-bibliography
bib-app on ccecrb-debat.com

This dashboard is used on ccecrb-debat.com to show a list of useful papers and resources for the public finances debate. The dashboard is powered by the Python Dash framework and retrieves data from a Zotero library using the pyzotero library.

## Adding Resources

To add one or more resources to the dashboard, please send an application to join the Zotero group. Once added to the group, you can add new resources to the library which will automatically appear in the dashboard.

## Usage

The dashboard displays a table of resources which can be filtered and sorted using the options at the top of each column. To filter the table, simply click on the filter icon and enter a search term. To sort the table, click on the column header.

## Requirements

* Python 3.7 or higher
* Zotero account
* Zotero API key
* Libraries: `dash`, `dash_bootstrap_components`, `pandas`, `pyzotero`

## Setup

1. Clone or download this repository.
2. Install the required libraries using pip install -r requirements.txt.
3. Rename assets/credentials_example.py to assets/credentials.py and fill in your library ID, library type and API key obtained from Zotero.
4. Run the app using python app.py.
5. Navigate to http://127.0.0.1:8050/ in your web browser to see the dashboard.

## Dependencies

The dashboard requires the following Python packages to be installed:

dash
dash_bootstrap_components
pandas
pyzotero
These packages can be installed using pip:

`pip install dash dash_bootstrap_components pandas pyzotero`

## Credits

This dashboard was created using the Dash framework and the pyzotero library. The design is based on the LITERA theme from Bootstrap.
