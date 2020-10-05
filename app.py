import os
import pathlib

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import plotly.graph_objs as go
import plotly.express as px
import dash_daq as daq

import pandas as pd

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server
app.config["suppress_callback_exceptions"] = True

APP_PATH = str(pathlib.Path(__file__).parent.resolve())

df_EF = pd.read_csv(os.path.join(APP_PATH, os.path.join("data", "EF_Africa.csv")))
df_con=df_EF.sort_values(by='Countries')

df_HS = pd.read_csv(os.path.join(APP_PATH, os.path.join("data", "HS_Africa.csv")))
del df_HS['Region']
df_HS_con=df_HS.sort_values(by='Country')


## Design the header
def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H5("Economic Freedom and Happiness Dashboard"),
                    html.H6("Done for Sub-Saharan Africa"),
                ],
            ),
            html.Div(
                id="banner-logo",
                children=[
                    html.Button(
                        id="learn-more-button", children="Info", n_clicks=0
                    ),
                ],
            ),
        ],
    )

## Design the two separate tabs
def build_tabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab2",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="Specs-tab",
                        label="Economic Freedom",
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="Control-chart-tab",
                        label="Happiness Score",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                ],
            )
        ],
    )

## Designs the content of tab 1

def build_tab_1():
    return [
        html.Div(
            id="settings-menu",
            children=[
                html.Div(
                    id="value-setter-menu",
                    children=[
                    generate_section_banner("Parameter Correlations"),
                        html.Div(
                            id="value-setter-view-output", className="output-datatable"
                        ),
                        html.Label(id="metric-select-title", children="Select parameters"),
                        dcc.Dropdown(
                            id="dp2_1",
                            options=list(
                                {"label": param, "value": param} for param in df_HS.columns[1:-1]
                            ),
                            value=[df_HS.columns[2],df_HS.columns[3]],multi=True,style={'display':'inline-block', 'width':'70%'}
                        ),
                       dcc.Graph(
                           id="graph3",
                       ),
                       html.Br(),
                       html.Label("Size of bubbles: Economy (GDP per Capita)",style={'color':'grey'} ),
                    ],
                ),
                html.Div(
                    id="metric-select-menu",
                    children=[
                    generate_section_banner("Country Comparism"),
                    html.Br(),
                        html.Label(id="metric-select-title", children="Select Countries"),
                        dcc.Dropdown(
                            id="dp2_3",
                            options=list(
                                {"label": param, "value": param} for param in df_HS_con.Country.unique()
                            ),
                            value=[df_HS_con.Country.unique()[1],df_HS_con.Country.unique()[3]],multi=True,style={'display':'inline-block', 'width':'100%'}
                        ),
                        dcc.Graph(
                            id="graph4",
                        ),
                        html.Br(),
                        html.Label("Compares at most 4 countries",style={'color':'grey'} ),
                    ],

                ),
            ],
        ),
    ]


def build_value_setter_line(line_num, label, value, col3):
    return html.Div(
        id=line_num,
        children=[
            html.Label(label, className="four columns"),
            html.Label(value, className="four columns"),
            html.Div(col3, className="four columns"),
        ],
        className="row",
    )


def generate_modal():
    return html.Div(
        id="markdown",
        className="modal",
        children=(
            html.Div(
                id="markdown-container",
                className="markdown-container",
                children=[
                    html.Div(
                        className="close-container",
                        children=html.Button(
                            "Close",
                            id="markdown_close",
                            n_clicks=0,
                            className="closeButton",
                        ),
                    ),
                    html.Div(
                        className="markdown-text",
                        children=dcc.Markdown(
                            children=(
                                """

                        ### Explanation of this dashboard
                        In this dashbord, you can explore the different Sub-Saharan African countries performance in these areas.

                        #### Economic Freedom Tab
                        This is measured with different parameters. This score shows explains the economic potential for business and growth of a country.
                        The data for this study was taken from Economic Freedom by Fraser Institution.

                        To get understanding about the parameters, check https://www.fraserinstitute.org/sites/default/files/economic-freedom-of-the-world-2019-appendix.pdf

                        - Choose parameters to project the comparism of these parameters on first graph
                        - Select year to view top 5 countries of the first parameter chosen
                        - Choose up to 4 countries to compare their yearly values of the first parameter chosen

                        #### Happiness score Tab
                        This is a measure of a country to provide wellness to its citizen based of certain parameters which economic freedom is one.

                        Download the data from Kaggle: https://www.kaggle.com/unsdsn/world-happiness?select=2019.csv

                        - Choose parameters to project the comparism of these parameters on first graph
                        - Choose up to 4 countries to compare their yearly values of the first parameter chosen

                    """
                            )
                        ),
                    ),
                ],
            )
        ),
    )


def build_quick_stats_panel():
    return html.Div(
        id="quick-stats",
        className="row",
        children=[
            html.Div(
                id="card-1",
                children=[
                    html.P("Choose parameters"),
                    dcc.Dropdown(
                        id="dp1",
                        options=list(
                            {"label": param, "value": param} for param in df_EF.columns[4:]
                        ),
                        value=[df_EF.columns[4],df_EF.columns[5]],multi=True,style={'width':'100%','height':'30%'}
                    ),
                    html.Label('Compares at most 2 parameters',style={'color':'grey'} ),
                    html.Div(
                        id="card-1",
                        children=[
                            html.P("Top 5 Countries each year"),
                            dcc.Dropdown(
                                id="dp3",
                                options=list(
                                    {"label": param, "value": param} for param in df_EF.Year.unique()
                                ),
                                value=df_EF.Year.unique()[0],style={'display':'inline-block', 'width':'100%'}
                            ),
                            generate_table(),
                            html.P("Result of Rank from World Comparism",style={'color':'grey'} )
                        ],
                    ),

                    html.P("Choose Countries"),
                    dcc.Dropdown(
                        id="dp4",
                        options=list(
                            {"label": param, "value": param} for param in df_con.Countries.unique()
                        ),
                        value=[df_con.Countries.unique()[0],df_con.Countries.unique()[1]],multi=True,style={'display':'inline-block', 'width':'100%'}
                    ),
                    html.Label('Compares at most 4 countries',style={'color':'grey'} )
                ],
            ),

        ],
    )


def generate_section_banner(title):
    return html.Div(className="section-banner", children=title)


def build_top_panel(stopped_interval):
    return html.Div(
        id="top-section-container",
        className="row",
        children=[
            # Metrics summary
            html.Div(
                id="metric-summary-session",
                className="eight columns",
                children=[
                    generate_section_banner("Parameter Correlations"),
                    html.Div(
                        id="metric-div",
                        children=[
                            dcc.Graph(
                                id="graph1",
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


def generate_table():
    return dash_table.DataTable(
    id='table',
    columns=[
            {'name': 'Country', 'id': 'country'},
            {'name': 'Value', 'id': 'val'}
        ],
        data=[{'name': i} for i in range(1,6)],
    style_as_list_view=True,
     style_header={
        'backgroundColor': 'rgba(0, 0, 0, 0)',
        'fontWeight': 'bold'
    },
    style_cell={
        'font_family': 'cursive',
        'font_size': '24px',
        'text_align': 'center',
       'backgroundColor': 'rgba(0, 0, 0, 0)',
       'fontWeight': 'bold'
   }
)



def build_chart_panel():
    return html.Div(
        id="control-chart-container",
        className="twelve columns",
        children=[
            generate_section_banner("Country Comparism"),
            dcc.Graph(
                id="graph2",
            ),
        ],
    )




app.layout = html.Div(
    id="big-app-container",
    children=[
        build_banner(),
        dcc.Interval(
            id="interval-component",
            interval=2 * 1000,  # in milliseconds
            n_intervals=50,  # start at batch 50
            disabled=True,
        ),
        html.Div(
            id="app-container",
            children=[
                build_tabs(),
                # Main app
                html.Div(id="app-content"),
            ],
        ),
        dcc.Store(id="n-interval-stage", data=50),
        generate_modal(),
    ],
)


@app.callback(
    [Output("app-content", "children"), Output("interval-component", "n_intervals")],
    [Input("app-tabs", "value")],
    [State("n-interval-stage", "data")],
)
def render_tab_content(tab_switch, stopped_interval):
    if tab_switch == "tab1":
        return build_tab_1(), stopped_interval
    return (
        html.Div(
            id="status-container",
            children=[
                build_quick_stats_panel(),
                html.Div(
                    id="graphs-container",
                    children=[build_top_panel(stopped_interval), build_chart_panel()],
                ),
            ],
        ),
        stopped_interval,
    )


# Update interval
@app.callback(
    Output("n-interval-stage", "data"),
    [Input("app-tabs", "value")],
    [
        State("interval-component", "n_intervals"),
        State("interval-component", "disabled"),
        State("n-interval-stage", "data"),
    ],
)
def update_interval_state(tab_switch, cur_interval, disabled, cur_stage):
    if disabled:
        return cur_interval

    if tab_switch == "tab1":
        return cur_interval
    return cur_stage



# ======= Callbacks for modal popup =======
@app.callback(
    Output("markdown", "style"),
    [Input("learn-more-button", "n_clicks"), Input("markdown_close", "n_clicks")],
)
def update_click_output(button_click, close_click):
    ctx = dash.callback_context

    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if prop_id == "learn-more-button":
            return {"display": "block"}

    return {"display": "none"}



@app.callback(
    output=Output("graph1", "figure"),
    inputs=[Input("dp1", "value")],
)
def Scatter_chart(dp1):
    df=df_EF.fillna(0)
    df=df.sort_values(by='Year')
    r_x=[-1,max(df[dp1[0]])+1]
    r_y=[-1,max(df[dp1[1]])+1]
    fig=px.scatter(df,x=dp1[0],y=dp1[1],color='Countries',size='Quartile', animation_frame="Year", animation_group="Countries",
     size_max=15,height=400,range_x=r_x,range_y=r_y)

    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    fig.update_layout(xaxis_zeroline=False, yaxis_zeroline=False,font=dict(
        family="Courier New, monospace",
        size=14,
        color='white'
    ))
    fig.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    return fig

@app.callback(
    output=Output("graph2", "figure"),
        inputs=[Input("dp1", "value"),
            Input("dp4", "value")],
    )
def comp_con(dp1, dp4):
    df_1=df_EF.fillna(0)
    df1=pd.DataFrame()
    for val in dp4[:4]:
        df1=pd.concat([df1,df_1[(df_1.Countries==val)]])
    fig=px.line(df1,x='Year',y=dp1[0],color='Countries')
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    fig.update_layout(xaxis_zeroline=False, yaxis_zeroline=False,font=dict(
        family="Courier New, monospace",
        size=14,
        color='white'
    ))
    fig.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    return fig

@app.callback(
    output=Output("table", "data"),
    inputs=[Input("dp1", "value"),
        Input("dp3", "value")],
    state=State('table', 'data')
)
def top5_chart(dp1,dp3,rows):
    df=df_EF.fillna(0)
    df=df[df.Year==dp3]
    if dp1[0]=='Rank':
        df=df.sort_values(by=dp1[0],ascending=False)
    else:
        df=df.sort_values(by=dp1[0])
    df=df[['Countries',dp1[0]]]
    df=df.drop_duplicates()
    i=1
    for row in rows:
        row['country']=df['Countries'].iloc[-i]
        row['val']=round(df[dp1[0]].iloc[-i],2)
        i+=1
    return rows

@app.callback(
    output=Output("graph3", "figure"),
    inputs=[Input("dp2_1", "value")],
)
def Scatter_chart_tab2(dp1):
    df=df_HS.fillna(0)
    df=df.sort_values(by='Year')
    r_x=[-0.05,max(df[dp1[0]])+0.05]
    r_y=[-0.05,max(df[dp1[1]])+0.05]

    fig=px.scatter(df,x=dp1[0],y=dp1[1],color='Country',size='Economy (GDP per Capita)', animation_frame="Year", animation_group="Country",
     size_max=45,height=400,range_x=r_x,range_y=r_y)

    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    fig.update_layout(xaxis_zeroline=False, yaxis_zeroline=False,font=dict(
        family="Courier New, monospace",
        size=14,
        color='white'
    ))
    fig.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    return fig

@app.callback(
    output=Output("graph4", "figure"),
        inputs=[Input("dp2_3", "value"),
        Input("dp2_1", "value")],
    )
def comp_con_HS(dp1,dp2):
    df_1=df_HS.fillna(0)
    df1=pd.DataFrame()
    for val in dp1[:4]:
        df1=pd.concat([df1,df_1[(df_1.Country==val)]])
    fig=px.bar(df1,x='Year',y=dp2[0],color='Country',barmode='group')
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    fig.update_layout(xaxis_zeroline=False, yaxis_zeroline=False,font=dict(
        family="Courier New, monospace",
        size=14,
        color='white'
    ))
    fig.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })
    return fig
# Running the server
if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
