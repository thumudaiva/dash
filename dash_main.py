import dash
from dash import html, dcc
#from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from datetime import datetime
import plotly.express as px
from dash.dependencies import Input, Output, State, MATCH, ALL
import dash_ag_grid as dag
import numpy as np
import pandas as pd
import pandas_datareader.data as web
from datetime import timedelta
import geopandas as gpd
shapefile_path = r"C:\Users\lenovo\Downloads\ne_110m_populated_places\ne_110m_populated_places.shp"
geo_df = gpd.read_file(shapefile_path)
fig = px.scatter_mapbox(
    geo_df,
    lat=geo_df.geometry.y,
    lon=geo_df.geometry.x,
    hover_name="NAME",  # Adjust column name if needed
    zoom=1,
    mapbox_style="open-street-map"  # Use OpenStreetMap as the map style
)

now = datetime.now()

current_year = datetime.now().year
current_month = datetime.now().month




three_months_back = now - timedelta(days=90)
from_year = three_months_back.year
from_month = three_months_back.month

current_date = f"{current_year}{current_month:02}"
from_date = f"{from_year}{from_month:02}"

external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css',
                        'https://use.fontawesome.com/releases/v5.9.0/css/all.css',
                        'assets/style.css',dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP]  # Add custom CSS file here


month_options = [{'label': f'{current_year}{i:02}', 'value': f'{current_year}{i:02}'} for i in range(1, current_month + 1)]

def fetch_stock_data(symbol, start_date, end_date):
    df = web.DataReader('AAPL', 'av-daily', start='2022-01-01', end='2023-12-31', api_key='your_api_key')
    return df

symbol = 'AAPL'  # Example stock symbol (Apple)
start_date = '2022-01-01'
end_date = '2023-12-31'
stock_df = px.data.iris()
#fetch_stock_data(symbol, start_date, end_date)
stock_df.to_csv(r"C:\Users\lenovo\Downloads\stock.csv")
# Define the app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,suppress_callback_exceptions=True)

# Sample data for the graphs
# data = px.data.iris()  # Sample dataset

# df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv")
column_defs = [
    {'field': 'Date', 'sortable': True},
    {'field': 'Open', 'sortable': True},
    {'field': 'High', 'sortable': True},
    {'field': 'Low', 'sortable': True},
    {'field': 'Close', 'sortable': True},
    {'field': 'Volume', 'sortable': True},
]

ag_grid_table= dag.AgGrid(
    rowData=stock_df.to_dict("records"),
    columnDefs=[{"field": i} for i in stock_df.columns],
    defaultColDef={"filter": True},
    dashGridOptions={"enableAdvancedFilter": True,"pagination": True,"paginationPageSize": 20},
    enableEnterpriseModules=True,
    style={"height": 300, "width": "100%"},
    
   # licenseKey= enter your license key here
)
card_10_content = html.Div([
    html.H5("Card 10 Title", className="card-title"),
    html.Div(ag_grid_table, style={'height': '300px'})  # Adjust height as needed
])

# Define the card creation function with custom styles
# def create_card():
#     return dbc.Card(
#         dbc.CardBody([
#             html.H4("Card Title", className="card-title"),
#             html.P("This is some card content", className="card-text"),
#         ]),
#         className="card l-bg-cherry",
#         style={'borderRadius': '10px', 'border': 'none', 'position': 'relative', 'marginBottom': '30px', 'boxShadow': '0 0.46875rem 2.1875rem rgba(90,97,105,0.1), 0 0.9375rem 1.40625rem rgba(90,97,105,0.1), 0 0.25rem 0.53125rem rgba(90,97,105,0.12), 0 0.125rem 0.1875rem rgba(90,97,105,0.1)'}
#     )

# # Create a row of cards with only three cards
# cards_row = dbc.Row(
#     [dbc.Col(create_card(), width=4) for _ in range(3)],  # Create 3 columns containing cards
#     className="mb-4 no-gutters",  # Margin bottom for spacing between rows, no gutters
#     style={'marginLeft': '10rem', 'marginRight': '5rem'}  # Add margin on both sides
# )

# Define the card creation function with custom styles

def format_total_records(total_records_value):
    if total_records_value >= 10000000:  # If total_records is 1 crore or more
        return f"{total_records_value // 10000000} CR"
    elif total_records_value >= 100000:  # If total_records is 1 lakh or more
        return f"{total_records_value // 100000} L"
    elif total_records_value >= 1000:  # If total_records is 1 thousand or more
        return f"{total_records_value // 1000} K"
    else:
        return str(total_records_value)
    
def calculate_percentage_difference(current_records, previous_records):
    if previous_records == 0:
        return 100 if current_records > 0 else 0
    return ((current_records - previous_records) / previous_records) * 100

def get_ring_color(percentage):
    if percentage == 100:
        return 'green'
    elif 70 < percentage < 100:
        return 'warning'
    elif 30 < percentage <= 70:
        return 'light-warning'
    else:
        return 'red'

def create_card(card_id, perkey, total_records, prev_total_records):
    arrow_icon_class = "bi bi-arrow-up-right text-success" if total_records > prev_total_records else "bi bi-arrow-down-right text-danger"
    percentage_diff = calculate_percentage_difference(total_records, prev_total_records)
    ring_color = get_ring_color(percentage_diff)
    
    progress_value = min(percentage_diff, 100)  # Ensure progress_value does not exceed 100
    
    return dbc.Card(
        dbc.CardBody([
            html.Div(html.I(className=arrow_icon_class), style={'position': 'absolute', 'top': '10px', 'right': '10px'}),
            
            html.Div(f"Perkey {perkey}", style={"color": "#878A99", "font-size": "22px", "font-family": "Saira, sans-serif", "text-transform": "uppercase", "font-weight": "bold"}, className="perkey-text"),
            html.Br(),
            
            html.Div("Total Records", style={"color": "#495057", "font-size": "13px", "font-family": "Saira, sans-serif", "font-weight": "bold",'margin-left': '9rem', "text-transform": "uppercase"}, className="total-records-label"),
            
            html.Div(
                className="card-content",
                children=[
                    html.Div(
                        f"{format_total_records(total_records)}",
                        className="counter-value",
                        style={"color": "#495057", "font-size": "22px", "font-family": "Saira, sans-serif", "font-weight": "bold", 'margin-left': '7rem'}
                    ),
                    html.Div(
                        className=f"ring-progress ring-progress-{ring_color}",
                        children=[
                            html.Div(
                                className="ring-progress-circle",
                                style={"--value": f"{progress_value}%"},
                                **{'data-progress': int(progress_value)}
                            ),
                            html.Div(
                                className="ring-progress-label",
                                children=f"{int(progress_value)}%"
                            )
                        ]
                    )
                ]
            )
        ]),
        className="card l-bg-cherry",
        style={'position': 'relative'}
    )


# Create cards dynamically
  # Sample total records data
data = {
    'perkey': [202401, 202402, 202403, 202404],
    'total_records': [2272939309, 2234333, 4477828828, 123456789]
}
df = pd.DataFrame(data)
num_cards = df.shape[0]



cards_row = dbc.Row(
    [dbc.Col(create_card(i, df.loc[i, 'perkey'], df.loc[i, 'total_records'], df.loc[i-1, 'total_records'] if i > 0 else df.loc[i, 'total_records']), width=3) for i in range(num_cards)],
    className="mb-4 no-gutters justify-content-center",
    style={'marginTop': '50px'}
)


card_5 = dbc.Card(
    dbc.CardBody([
        html.H5("Geographic Scatter Plot", className="card-title"),
        dcc.Graph(figure=fig)  # Embed the Plotly graph here
    ]),
    className="card card-5",  # Add specific class for card_5
    id='card-5',
    style={'width': '98%', 'height': '400px'}  # Adjust width and height
)

card_6 = dbc.Card(
    dbc.CardBody([
        html.H5("Card 6 Title", className="card-title"),
        html.P("This is card 6 content", className="card-text"),
    ]),
    className="card card-6",  # Add specific class for card_6
    id='card-6',
    style={'width': '97%', 'height': '250px'}  # Adjust width and height
)
card_7 = dbc.Card(
    dbc.CardBody([
        html.H5("Card 7 Title", className="card-title"),
        html.P("This is card 5 content", className="card-text"),
    ]),
    className="card card-5",  # Add specific class for card_5
    id='card-7',
    style={'width': '98%', 'height': '250px'}  # Adjust width and height
)

card_8 = dbc.Card(
    dbc.CardBody([
        html.H5("Card 8 Title", className="card-title"),
        html.P("This is card 5 content", className="card-text"),
    ]),
    className="card card-5",  # Add specific class for card_5
    id='card-8',
    style={'width': '98%', 'height': '250px'}  # Adjust width and height
)

card_9 = dbc.Card(
    dbc.CardBody([
        html.H5("Card 9 Title", className="card-title"),
        html.P("This is card 5 content", className="card-text"),
    ]),
    className="card card-5",  # Add specific class for card_5
    id='card-9',
    style={'width': '98%', 'height': '250px'}  # Adjust width and height
)

card_10 = dbc.Card(
    dbc.CardBody(card_10_content),
    className="card card-5",
    id='card-10',
    style={'width': '98%', 'height': '400px'}  # Adjust width and height
)


# Callback to update the content of each card
@app.callback(
    [Output(f'card-content-{i}', 'children') for i in range(num_cards)],
    [Input('url', 'pathname')]
)
def update_card_content(pathname):
    # You can add your logic here to update the content based on the pathname
    # For demonstration purposes, I'll just return some sample content
    content = [
        html.P(f"This is card {i+1} content") for i in range(num_cards)
    ]
    return content

# Define the sidebar layout with collapsible sub-menus
sidebar = html.Div([
    html.H2("Bedimcode", className="display-4"),
    html.Hr(),
    dbc.Nav([
        dbc.NavLink([html.I(className="bi bi-bar-chart-line-fill"), html.Span("Dashboard")], href="/", active="exact", className="nav-link"),
        dbc.NavLink([html.I(className="bi bi-bar-chart-line-fill"), html.Span("Messenger")], href="/messenger", active="exact", className="nav-link"),
        dbc.NavLink("Analytics", href="/analytics", active="exact", className="nav-link"),
        dbc.NavLink("Settings", href="/settings", active="exact", className="nav-link"),
        dbc.NavItem([
            dbc.NavLink("Projects", href="#", className="nav-link", id="toggle-projects"),
            dbc.Collapse(
                dbc.Nav([
                    dbc.NavLink("Data", href="/projects/data", className="nav-link"),
                    dbc.NavLink("Group", href="/projects/group", className="nav-link"),
                    dbc.NavLink("Members", href="/projects/members", className="nav-link"),
                ], vertical=True, pills=True),
                id="collapse-projects",
            ),
        ]),
        dbc.NavItem([
            dbc.NavLink("Team", href="#", className="nav-link", id="toggle-team"),
            dbc.Collapse(
                dbc.Nav([
                    dbc.NavLink("Data", href="/team/data", className="nav-link"),
                    dbc.NavLink("Group", href="/team/group", className="nav-link"),
                    dbc.NavLink("Members", href="/team/members", className="nav-link"),
                ], vertical=True, pills=True),
                id="collapse-team",
            ),
        ]),
        dbc.NavLink("Log Out", href="/logout", active="exact", className="nav-link"),
    ], vertical=True, pills=True, className="flex-column"),
], className="sidebar")

# Horizontal Navbar
# Horizontal Navbar
horizontal_navbar = html.Div(
    className="navbar",
    style={'padding': '20px 0', 'background-color': '#F2F3F8', 'height': '5rem', 'marginBottom': '3rem'},  # Increase padding to increase height and set background color
    children=[
        html.Div(
            className="container",
            children=[
                html.Div(
                    className="row align-items-center",
                    children=[
                        html.Div(
                            className="col",
                            children=[
                                html.Span("From Date", className="font-weight-bold", style={'margin-left': '6rem', 'margin-top': '-2rem'}),
                                dcc.Dropdown(
                                    id='month-dropdown-1',
                                    options=month_options,
                                    value=from_date,  # Default to the first month of the current year
                                    className='dropdown-style',
                                    style={'width': '150px', 'margin-left': '6rem', 'margin-top': '-2rem'}  # Set width of the dropdown
                                ),
                            ]
                        ),
                        html.Div(
                            className="col",
                            children=[
                                html.Span("To Date", className="font-weight-bold", style={'margin-left': '6rem', 'margin-top': '-2rem'}),
                                dcc.Dropdown(
                                    id='month-dropdown-2',
                                    options=month_options,
                                    value=current_date,  # Default to the first month of the current year
                                    className='dropdown-style',
                                    style={'width': '150px', 'margin-left': '5rem', 'margin-top': '-2rem'}  # Set width of the dropdown
                                ),
                            ]
                        ),
                        html.Div(
                            className="col", style={'flex': '1'},  # Set the third column to take up the remaining space
                            children=[
                                html.Div(
                                    className="search",
                                    children=[
                                        dcc.Input(
                                            className="form-control mr-sm-2",
                                            type="search",
                                            placeholder="Search Courses",
                                            name="search",
                                            style={'width': '300px', 'height': '35px', 'border-radius': '25px', 'border': 'none', 'margin-left': '6rem', 'margin-top': '-0.8rem'}
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        html.Div(  # Move this div to the end for profile dropdown
                            className="col",
                            children=[
                                html.Div(
                                    className="dropdown",
                                    children=[
                                        html.A(
                                            className="nav-link dropdown-toggle",
                                            href="#",
                                            id="navbarDropdownMenuLink",
                                            role="button",
                                            **{"data-toggle": "dropdown", "aria-haspopup": "true", "aria-expanded": "false"},
                                            children=[
                                                html.Img(src="https://s3.eu-central-1.amazonaws.com/bootstrapbaymisc/blog/24_days_bootstrap/fox.jpg", className="rounded-circle", style={'width': '40px', 'height': '40px'}),
                                            ]
                                        ),
                                        
            #                             html.Div(
            # id='date-validation-message-container',
            # children=[
            #     html.Div(
            #         id='
           # date-validation-message',
            #         style={'color': 'red', 'font-size': 'small', 'padding-top': '10px'}
            #     ),
            # ],
            # style={'display': 'none'}),
                #                         dbc.Alert(
                #     id='date-validation-alert',
                #     color='danger',
                #     is_open=False,
                #     duration=4000,  # Alert will auto-dismiss after 4000 milliseconds
                # ),
         
                                        dbc.DropdownMenu(
                                        [
                                            dbc.DropdownMenuItem("My Profile", href="/profile"),
                                            dbc.DropdownMenuItem("Settings", href="/settings"),
                                            dbc.DropdownMenuItem("Log Out", href="/logout"),
                                        ],
                                        right=True,
                                        className="dropdown-menu dropdown-menu-right",
                                    ),
                                    ]
                                ),
                            ]
                        ),
                    ]
                )
            ]
        )
    ],id = 'navbar-container',
)
content = html.Div([
    html.Div(
        id='date-validation-alert-container',
        children=[
            dbc.Alert(
                id='date-validation-alert',
                color='danger',
                is_open=False,
                duration=4000,  # Alert will auto-dismiss after 4000 milliseconds
            ),
        ],
        className='top-alert',  # Apply the custom class to the alert container
    ),
    html.Div([
        html.Div([
            cards_row,  # Insert the row of cards at the top of the content
            dbc.Row([
                html.Div(card_5, className="col card-wrapper"),
                html.Div(card_6, className="col card-wrapper")
            ], className="mb-4 no-gutters justify-content-center", style={'marginTop': '50px'}),
            dbc.Row([
                html.Div(card_7, className="col card-wrapper"),
                html.Div(card_8, className="col card-wrapper"),
                html.Div(card_9, className="col card-wrapper"),

            ], className="mb-4 no-gutters justify-content-center", style={'marginTop': '50px'}),
            dbc.Row([
                html.Div(card_10, className="col card-wrapper")

            ], className="mb-4 no-gutters justify-content-center", style={'marginTop': '50px'})  # Add margin on top
        ], style={'overflowY': 'auto', 'height': 'calc(100vh - 60px)', 'marginLeft': '80px'})  
    ], id="page-content")
], id="content-wrapper")
# Landing page layout
landing_page_layout = html.Div(
    [
        html.H1("Welcome to My Dashboard"),
        html.P("This is a simple landing page for the dashboard."),
        html.P("Please use the sidebar navigation to explore the dashboard features."),
        html.Div([
            dcc.Dropdown(['NYC', 'MTL', 'SF'], 'NYC', id='demo-dropdown'),
            html.Div(id='dd-output-container')
        ],className="test_drop")
    ],
    style={'textAlign': 'center', 'padding': '50px'}
)

# App layout
app.layout = html.Div([
    dcc.Location(id="url"),  # Add the URL component
    sidebar,
    html.Div(horizontal_navbar),
    html.Div(content),
#    html.Div(id='date-validation-message-container', children=[
#     html.Div(id='date-validation-message', style={'color': 'red', 'font-size': 'small', 'padding-top': '10px'}),
# ], style={'padding-left': '80px'})

])

# @app.callback(
#     Output('date-validation-message-container', 'style'),
#     [Input('month-dropdown-1', 'value'), Input('month-dropdown-2', 'value')]
# )
# def show_date_validation_message(from_date, to_date):
#     if from_date is not None and to_date is not None:
#         from_year, from_month = divmod(int(from_date), 100)
#         to_year, to_month = divmod(int(to_date), 100)
#         if from_year > to_year or (from_year == to_year and from_month > to_month):
#             return {'display': 'block'}
#     return {'display': 'none'}

@app.callback(
    Output('month-dropdown-1', 'className'),
    Output('month-dropdown-2', 'className'),
    [Input('month-dropdown-1', 'value'), Input('month-dropdown-2', 'value')]
)
def update_dropdown_classes(from_date, to_date):
    from_year, from_month = divmod(int(from_date), 100) if from_date else (0, 0)
    to_year, to_month = divmod(int(to_date), 100) if to_date else (current_year, current_month)
    if from_year > to_year or (from_year == to_year and from_month > to_month):
        return 'is-invalid', 'is-invalid'
    return '', ''

# @app.callback(
#     Output('date-validation-message', 'children'),
#     [Input('month-dropdown-1', 'value'), Input('month-dropdown-2', 'value')]
# )
# def validate_date_range(from_date, to_date):
#     if from_date is not None and to_date is not None:
#         from_year, from_month = divmod(int(from_date), 100)
#         to_year, to_month = divmod(int(to_date), 100)
#         if from_year > to_year or (from_year == to_year and from_month > to_month):
#             return "Invalid date range. Please select a valid date range."
#     return ""


@app.callback(
    [Output('date-validation-alert', 'is_open'),
     Output('date-validation-alert', 'children')],
    [Input('month-dropdown-1', 'value'),
     Input('month-dropdown-2', 'value')]
)
def validate_dates(from_date, to_date):
    if from_date and to_date:
        from_date_int = int(from_date)
        to_date_int = int(to_date)
        if from_date_int > to_date_int:
            return True, "Invalid date range: 'From Date' cannot be after 'To Date'."
    return False, ""



# Callback to toggle collapse on sub-menu items
@app.callback(
    [Output("collapse-projects", "is_open"), Output("collapse-team", "is_open")],
    [Input("toggle-projects", "n_clicks"), Input("toggle-team", "n_clicks")],
    [State("collapse-projects", "is_open"), State("collapse-team", "is_open")],
)
def toggle_collapse(n1, n2, is_open1, is_open2):
    if not n1 and not n2:
        return False, False  # Neither button has ever been clicked
    ctx = dash.callback_context
    if not ctx.triggered:
        return False, False  # No clicks yet
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if button_id == "toggle-projects":
        return not is_open1, False
    elif button_id == "toggle-team":
        return False, not is_open2
    return False, False

# Define the callback to switch between landing page and dashboard
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def display_page(pathname):
    if pathname == "/":
        return landing_page_layout
    else:
        return content


@app.callback(
    Output("navbar-container", "style"),
    [Input("url", "pathname")]
)
def toggle_navbar_visibility(pathname):
    if pathname == "/":
        return {'display': 'none'}  # Hide the navbar if pathname is '/'
    else:
        return {}  # Show the navbar for other paths
    




from dash.exceptions import PreventUpdate


if __name__ == "__main__":
    app.run_server(debug=True,port=9999)
