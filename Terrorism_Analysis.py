
import pandas as pd
import webbrowser
import dash
import dash_html_components as html
from dash.dependencies import Input, Output 
import dash_core_components as dcc 
import plotly.graph_objects as go  
import plotly.express as px
from dash.exceptions import PreventUpdate

app = dash.Dash()
project_name = None


 
def load_data():
    dataset_name = "globalterrorism"
  
    
    global df
    df = pd.read_csv(dataset_name)
    
  
    global month_list
    month = {
           "January":1,
           "February": 2,
           "March": 3,
           "April":4,
           "May":5,
           "June":6,
           "July": 7,
           "August":8,
           "September":9,
           "October":10,
           "November":11,
           "December":12
           }
    month_list= [{"label":key, "value":values} for key,values in month.items()]
  
    global date_list
    date_list = [x for x in range(1, 32)]
  
  
    global region_list
    region_list = [{"label": str(i), "value": str(i)}  for i in sorted( df['region_txt'].unique().tolist() ) ]
  
  
    global country_list
    country_list = df.groupby("region_txt")["country_txt"].unique().apply(list).to_dict()
  
  
    global state_list
    state_list = df.groupby("country_txt")["provstate"].unique().apply(list).to_dict()
  
  
    global city_list
    city_list  = df.groupby("provstate")["city"].unique().apply(list).to_dict()
  
  
    global attack_type_list
    attack_type_list = [{"label": str(i), "value": str(i)}  for i in df['attacktype1_txt'].unique().tolist()]
  
  
    global year_list
    year_list = sorted ( df['iyear'].unique().tolist()  )
  
    global year_dict
    year_dict = {str(year): str(year) for year in year_list}
    
    #chart dropdown options
    global chart_dropdown_values
    chart_dropdown_values = {"Terrorist Organisation":'gname', 
                               "Target Nationality":'natlty1_txt', 
                               "Target Type":'targtype1_txt', 
                               "Type of Attack":'attacktype1_txt', 
                               "Weapon Type":'weaptype1_txt', 
                               "Region":'region_txt', 
                               "Country Attacked":'country_txt'
                            }
                                
    chart_dropdown_values = [{"label":keys, "value":value} for keys, value in chart_dropdown_values.items()]
  
  
def open_browser():
    webbrowser.open_new('http://127.0.0.1:8050/')

def create_app_ui():
    main_layout = html.Div([
    html.H1('Terrorism Analysis with Insights', id='Main_title',style={ "color": "white", 'textAlign': 'center'}),
    dcc.Tabs(id="Tabs", value="Map",children=[
        dcc.Tab(label="Map tool" ,id="Map tool",value="Map", children=[
            dcc.Tabs(id = "subtabs", value = "WorldMap",children = [
                dcc.Tab(label="World Map tool", id="World", value="WorldMap"),
                dcc.Tab(label="India Map tool", id="India", value="IndiaMap")
                ]),
            dcc.Dropdown(
                id='month-dropdown', 
                  options=month_list,
                  placeholder='Select Month',
                  style={ "color": "blue", 'font-weight': 'bold'},
                  multi = True
                    ),
            dcc.Dropdown(
                  id='date-dropdown', 
                  placeholder='Select Day',
                  style={ "color": "blue", 'font-weight': 'bold'},
                  multi = True
                    ),
            dcc.Dropdown(
                  id='region-dropdown', 
                  options=region_list,
                  placeholder='Select Region',
                  style={ "color": "blue",'font-weight': 'bold'},
                  multi = True
                    ),
            dcc.Dropdown(
                  id='country-dropdown', 
                  options=[{'label': 'All', 'value': 'All'}],
                  style={ "color": "blue",'font-weight': 'bold'},
                  placeholder='Select Country',
                  multi = True
                    ),
            dcc.Dropdown(
                  id='state-dropdown', 
                  options=[{'label': 'All', 'value': 'All'}],
                  placeholder='Select State or Province',
                  style={ "color": "blue",'font-weight': 'bold'},
                  multi = True
                    ),
            dcc.Dropdown(
                  id='city-dropdown', 
                  options=[{'label': 'All', 'value': 'All'}],
                  placeholder='Select City',
                  style={ "color": "blue",'font-weight': 'bold'},
                  multi = True
                    ),
            dcc.Dropdown(
                  id='attacktype-dropdown', 
                  options=attack_type_list,#[{'label': 'All', 'value': 'All'}],
                  placeholder='Select Attack Type',
                  style={"color": "blue",'font-weight': 'bold'},
                  multi = True
                    ),
  
            html.H5('Select the Year', id='year_title',style={ "color": "white",'font-weight': 'bold'}),
            dcc.RangeSlider(
                      id='year-slider',
                      min=min(year_list),
                      max=max(year_list),
                      value=[min(year_list),max(year_list)],
                      marks=year_dict,
                      step=None
                        ),
            html.Br()
      ]),
        dcc.Tab(label = "Chart Tool", id="chart tool", value="Chart", children=[
            dcc.Tabs(id = "subtabs2", value = "WorldChart",children = [
                dcc.Tab(label="World Chart tool", id="WorldC", value="WorldChart"),          
              dcc.Tab(label="India Chart tool", id="IndiaC", value="IndiaChart")]),
              html.Br(),
              html.Br(),
              dcc.Dropdown(id="Chart_Dropdown", options = chart_dropdown_values, placeholder="Select option", value = "region_txt",style={"color": "blue",'font-weight': 'bold'}), 
              html.Br(),
              html.Br(),
              html.Hr(),
              dcc.Input(id="search", placeholder="Search Filter",style={ "color": "white" , 'font-size':'20px','font-weight': 'bold'}),
              html.Hr(),
              html.Br(),
              dcc.RangeSlider(
                      id='cyear_slider',
                      min=min(year_list),
                      max=max(year_list),
                      value=[min(year_list),max(year_list)],
                      marks=year_dict,
                      step=None
                        ),
                    html.Br()
                ]),
           ]),
    dcc.Loading(dcc.Graph(id='graph-object', figure = go.Figure()))
    ],style= {
            'border': '10px black',
            'backgroundColor':'#92a8d1',
            'font-weight': 'bold',
            'font-family': 'Verdana,sans-serif'
            })
          
    return main_layout
  
  




@app.callback(dash.dependencies.Output('graph-object', 'figure'),
    [
    Input("Tabs", "value"),
    Input('month-dropdown', 'value'),
    Input('date-dropdown', 'value'),
    Input('region-dropdown', 'value'),
    Input('country-dropdown', 'value'),
    Input('state-dropdown', 'value'),
    Input('city-dropdown', 'value'),
    Input('attacktype-dropdown', 'value'),
    Input('year-slider', 'value'), 
    Input('cyear_slider', 'value'), 
    
    Input("Chart_Dropdown", "value"),
    Input("search", "value"),
    Input("subtabs2", "value")
    ]
    )

def update_app_ui(Tabs, month, date,region,country,state,city,attack,year,chart_year, chart_dp, search, subtabs2):
    fig = None
     
    if Tabs == "Map":
        print("Data Type of month value = " , str(type(month)))
        print("Data of month value = " , month)
        
        print("Data Type of Day value = " , str(type(date)))
        print("Data of Day value = " , date)
        
        print("Data Type of region value = " , str(type(region)))
        print("Data of region value = " , region)
        
        print("Data Type of country value = " , str(type(country)))
        print("Data of country value = " , country)
        
        print("Data Type of state value = " , str(type(state)))
        print("Data of state value = " , state)
        
        print("Data Type of city value = " , str(type(city)))
        print("Data of city value = " , city)
        
        print("Data Type of Attack value = " , str(type(attack)))
        print("Data of Attack value = " , attack)
        
        print("Data Type of year value = " , str(type(year)))
        print("Data of year value = " , year)
        year_range = range(year[0], year[1]+1)
        new_df = df[df["iyear"].isin(year_range)]
    
        if month==[] or month is None:
            pass
        else:
            if date==[] or date is None:
                new_df = new_df[new_df["imonth"].isin(month)]
            else:
                new_df = new_df[new_df["imonth"].isin(month)
                                & (new_df["iday"].isin(date))]
        # region, country, state, city filter
        if region==[] or region is None:
            pass
        else:
            if country==[] or country is None :
                new_df = new_df[new_df["region_txt"].isin(region)]
            else:
                if state == [] or state is None:
                    new_df = new_df[(new_df["region_txt"].isin(region))&
                                    (new_df["country_txt"].isin(country))]
                else:
                    if city == [] or city is None:
                        new_df = new_df[(new_df["region_txt"].isin(region))&
                        (new_df["country_txt"].isin(country)) &
                        (new_df["provstate"].isin(state))]
                    else:
                        new_df = new_df[(new_df["region_txt"].isin(region))&
                        (new_df["country_txt"].isin(country)) &
                        (new_df["provstate"].isin(state))&
                        (new_df["city"].isin(city))]
                        
        if attack == [] or attack is None:
            pass
        else:
            new_df = new_df[new_df["attacktype1_txt"].isin(attack)] 
    
        mapFigure = go.Figure()
        if new_df.shape[0]:
            pass
        else: 
            new_df = pd.DataFrame(columns = ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
               'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])
            
            new_df.loc[0] = [0, 0 ,0, None, None, None, None, None, None, None, None]
            
        
        mapFigure = px.scatter_mapbox(new_df,
          lat="latitude", 
          lon="longitude",
          color="attacktype1_txt",
          hover_name="city", 
          hover_data=["region_txt", "country_txt", "provstate","city", "attacktype1_txt","nkill","iyear","imonth", "iday"],
          zoom=1
          )                       
        mapFigure.update_layout(mapbox_style="open-street-map",
          autosize=True,
          margin=dict(l=0, r=0, t=25, b=20),
          )
          
        fig = mapFigure

    elif Tabs=="Chart":
        fig = None
        
        year_range_c = range(chart_year[0], chart_year[1]+1)
        chart_df = df[df["iyear"].isin(year_range_c)]
        
        
        if subtabs2 == "WorldChart":
            pass
        elif subtabs2 == "IndiaChart":
            chart_df = chart_df[(chart_df["region_txt"]=="South Asia") &(chart_df["country_txt"]=="India")]
        if chart_dp is not None and chart_df.shape[0]:
            if search is not None:
                chart_df = chart_df.groupby("iyear")[chart_dp].value_counts().reset_index(name = "count")
                chart_df  = chart_df[chart_df[chart_dp].str.contains(search, case=False)]
            else:
                chart_df = chart_df.groupby("iyear")[chart_dp].value_counts().reset_index(name="count")
        
        
        if chart_df.shape[0]:
            pass
        else: 
            chart_df = pd.DataFrame(columns = ['iyear', 'count', chart_dp])
            
            chart_df.loc[0] = [0, 0,"No data"]
        fig = px.area(chart_df, x="iyear", y ="count", color = chart_dp)

    return fig



@app.callback(
    Output("date-dropdown", "options"),
    [Input("month-dropdown", "value")])
def update_date(month):
    option = []
    if month:
        option= [{"label":m, "value":m} for m in date_list]
    return option

@app.callback(
    [Output("region-dropdown", "value"),
    Output("region-dropdown", "disabled"),
    Output("country-dropdown", "value"),
    Output("country-dropdown", "disabled")],
    [Input("subtabs", "value")]
    )
def update_r(tab):
    region = None
    disabled_r = False
    country = None
    disabled_c = False
    if tab == "WorldMap":
        pass
    elif tab=="IndiaMap":
        region = ["South Asia"]
        disabled_r = True
        country = ["India"]
        disabled_c = True
    return region, disabled_r, country, disabled_c



@app.callback(
    Output('country-dropdown', 'options'),
    [Input('region-dropdown', 'value')])
def set_country_options(region_value):
    option = []
    # Making the country Dropdown data
    if region_value is  None:
        raise PreventUpdate
    else:
        for var in region_value:
            if var in country_list.keys():
                option.extend(country_list[var])
    return [{'label':m , 'value':m} for m in option]


@app.callback(
    Output('state-dropdown', 'options'),
    [Input('country-dropdown', 'value')])
def set_state_options(country_value):
    # Making the state Dropdown data
    option = []
    if country_value is None :
        raise PreventUpdate
    else:
        for var in country_value:
            if var in state_list.keys():
                option.extend(state_list[var])
    return [{'label':m , 'value':m} for m in option]

@app.callback(
    Output('city-dropdown', 'options'),
    [Input('state-dropdown', 'value')])
def set_city_options(state_value):
    option = []
    if state_value is None:
        raise PreventUpdate
    else:
        for var in state_value:
            if var in city_list.keys():
                option.extend(city_list[var])
    return [{'label':m , 'value':m} for m in option]


def main():
    load_data()
    
    open_browser()
    
    global project_name
    project_name = "Terrorism Analysis with Insights" 
      
    global app
    app.layout = create_app_ui()
    app.title = project_name
    app.run_server()
  
    print("This would be executed only after the script is closed")
    app = None
    project_name = None


if __name__ == '__main__':
    main()




