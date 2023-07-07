#%%
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP,dbc.icons.BOOTSTRAP])

df1 = pd.read_csv('https://raw.githubusercontent.com/christianalvarezbaez/GlobalWarming/main/df_total_new_countries.csv')
df = df1.copy()
df.set_index('Countries',inplace=True)


#%% TITLES 

Header1 = html.H1('Global Warming on the Last Millennium', style ={'color':'#FFFFFF'})
Header2 = html.H4(' Choose a country', style = {'color': '#60d7f7'})
Header3 = html.H4(' Choose first year and last year for comparison within the range of 850 to 2005',  style = {'color': '#60d7f7'})
sub1 = html.P('The result will be how warmer or colder is the second year compared to the first year',  style = {'color': '#60d7f7'})

#STYLES

table_styles = {'marginLeft': '10%','marginRight': '10%', 'width' : '80%'}
map_styles = {'width' : '100%', 'marginLeft': 'auto', 'marginRight':'auto'}

#%% 
app.layout = html.Div(children = [

    dbc.Row([
        Header1
    ],style={'background-color': '#f0f79e',
            'background-image': 'url(https://images.pexels.com/photos/87009/earth-soil-creep-moon-lunar-surface-87009.jpeg)', 
            'height':'150px',
            'background-position': '50' + '%' +' 50'+'%', #x, y
            'background-size': '100' + '%' +' 1000'+'%'}), 
    dbc.Row([
        dbc.Col([
            Header2,
            dcc.Dropdown(id="select_country",
                 options= [{'label': i, 'value': i} for i in df.index],
                 multi=False,
                 value='World',
                 style={'width': "150px",'marginLeft': '1%', 'background-color':'#FFFFFF'}
                 ),
            html.Br(),
            dcc.Graph(id='time_series', 
                      figure={},
                      style = {'width' : '100%','marginLeft': 'auto', 'marginRight': 'auto'}   #Right now is empty
                ),
    ], style={'background-color': '#000000', 'width' : '50%'}), 
        dbc.Col([
            Header3,
            dcc.Input(id="year1", type="number", value=1900),
            dcc.Input(id="year2", type="number", value=2000),
            sub1,
            dcc.Graph(id='map1', 
                      figure={},
                      style = map_styles   #Right now is empty
                      ),
    ], style={'background-color': '#000000'})]),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id = 'map2',
                        figure = {},
                        style = map_styles)
                ), 
        dbc.Col(
            dcc.Graph(id = 'map3',
                       figure = {},
                       style = map_styles)
                )
            ], style={'background-color': '#000000'}),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id = 'table1',
                       figure = {},
                       style = table_styles)
                ), 
        dbc.Col(
            dcc.Graph(id = 'table2',
                       figure = {},
                       style = table_styles)
                )
            ], style={'background-color': '#000000'}),
    dbc.Row([
        dbc.Col(
            dcc.Graph(id = 'table3',
                       figure = {},
                       style = table_styles)
                ), 
        dbc.Col(
            dcc.Graph(id = 'table4',
                       figure = {},
                       style = table_styles)
                )
            ], style={'background-color': '#000000'}),
    

])

#%%
@app.callback(
    [Output(component_id='time_series', component_property='figure'),
    Output(component_id='map1', component_property='figure'),
    Output(component_id='map2', component_property='figure'),
    Output(component_id='map3', component_property='figure'),
    Output(component_id='table1', component_property='figure'),
    Output(component_id='table2', component_property='figure'),
    Output(component_id='table3', component_property='figure'),
    Output(component_id='table4', component_property='figure')],
    [Input(component_id='select_country', component_property='value'), 
    Input(component_id='year1', component_property='value'),
    Input(component_id='year2', component_property='value')]
)

def update_graph(country,year1,year2):
    print(country)
    print(type(country))

    #Figure 1
    x=df.columns
    y=df.loc[str(country)]
    country = [str(country)] * len(df.loc[str(country)])

    fig1 = px.line(x=x, y=y, 
              color=country, 
              title = f'Mean temperature on {country[0]} <br> over last millenium', template = 'plotly_dark'
              ).update_layout(title_x = 0.50,
        legend_title_text='Country',
    xaxis_title="Year", yaxis_title="Temperature °C", font=dict(
        family="Sans-serif, monospace",
        size=16,
        color="White"), 
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)').update_xaxes(tickangle=60,nticks =20, tickfont_size = 12)
    


 
    #Figure 2
    df_world_r = df[str(year2)] - df[str(year1)]
    df_world_r = df_world_r.reset_index()

    fig2 = px.choropleth(
        data_frame=df_world_r,
        locationmode='country names',
        locations='Countries',
        scope="world",
        title = f'Temperature Difference by Nation <br> between year {year1} and {year2}',
        color=df_world_r[0],
        color_continuous_scale=px.colors.sequential.RdBu_r,
        labels={'0': '°C'},
        template='plotly_dark',
        range_color = [-2, 2], 
    ).update_layout(
    title_x = 0.50,
    font=dict(
        family="Arial",
        size=16,  # Set the font size here
        color="White",),
    margin=dict(l=50, r=50, b=90, t=100),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
    )

    #Figure 3
    df_row2 = df.drop('World').reset_index() 

    fig3 = px.choropleth(
        data_frame=df_row2,
        locationmode='country names',
        locations='Countries',
        scope="world",
        title = f'Mean Temperature by Nation <br> at year {year1}',
        color=str(year1),
        color_continuous_scale=px.colors.sequential.RdBu_r,
        labels={str(year1): '°C'},
        template='plotly_dark',
        range_color = [-30, 30]
    ).update_layout(title_x = 0.50,
    font=dict(
        family="Arial",
        size=16,  # Set the font size here
        color="White"),
    margin=dict(l=60, r=50, b=100, t=100),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
    )

    #Figure 4
    fig4 = px.choropleth(
        data_frame=df_row2,
        locationmode='country names',
        locations='Countries',
        scope="world",
        title = f'Mean Temperature by Nation <br> at year {year2}',
        color=str(year2),
        color_continuous_scale=px.colors.sequential.RdBu_r,
        labels={str(year2): '°C'},
        template='plotly_dark',
        range_color = [-30, 30]
    ).update_layout(title_x = 0.5,
    font=dict(
        family="Arial",
        size=16,  # Set the font size here
        color="White"),
    margin=dict(l=60, r=50, b=100, t=100),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
    )


    #Tables
    df_top_cold_old = df[str(year1)].sort_values().head(10)
    df_top_hot_old = df[str(year1)].sort_values(ascending = False).head(10)
    df_top_cold_new = df[str(year2)].sort_values().head(10)
    df_top_hot_new = df[str(year2)].sort_values(ascending = False).head(10)


    fig5 = go.Figure(data=[go.Table(
    header=dict(values=['Countries', 'Temperature °C'],
                line_color='darkslategray',
                fill_color='lightskyblue',
                align='left'),
    cells=dict(values=[df_top_cold_old.index, # 1st column
                       df_top_cold_old.round(2)], # 2nd column
               line_color='darkslategray',
               fill_color='lightcyan',
               align='left'))
    ],layout = {'title' : f'Top Ten Coldest <br> Countries in {year1}','title_x': 0.5, 'title_y':0.9}).update_layout(paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',margin=dict(l=20, r=20, b=20, t=100),title_font_size = 25,title_font_color = 'white')

    fig6 = go.Figure(data=[go.Table(
    header=dict(values=['Countries', 'Temperature °C'],
                line_color='darkslategray',
                fill_color=' lightcoral',
                align='left'),
    cells=dict(values=[df_top_hot_old.index, # 1st column
                       df_top_hot_old.round(2)], # 2nd column
               line_color='darkslategray',
               fill_color='lightyellow',
               align='left'))
    ],layout = {'title' : f'Top Ten Warmest <br> Countries in {year1}','title_x': 0.5, 'title_y':0.9}).update_layout(paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',margin=dict(l=20, r=20, b=20, t=100),title_font_size = 25,title_font_color = 'white')


    fig7 = go.Figure(data=[go.Table(
    header=dict(values=['Countries', 'Temperature °C'],
                line_color='darkslategray',
                fill_color='lightskyblue',
                align='left'),
    cells=dict(values=[df_top_cold_new.index, # 1st column
                       df_top_cold_new.round(2)], # 2nd column
               line_color='darkslategray',
               fill_color='lightcyan',
               align='left'))
    ], layout = {'title' : f'Top Ten Coldest <br> Countries in {year2}', 'title_x': 0.5, 'title_y':0.9}).update_layout(paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',margin=dict(l=20, r=20, b=20, t=100),title_font_size = 25,title_font_color = 'white')

    fig8 = go.Figure(data=[go.Table(
    header=dict(values=['Countries', 'Temperature °C'],
                line_color='darkslategray',
                fill_color=' lightcoral',
                align='left'),
    cells=dict(values=[df_top_hot_new.index, # 1st column
                       df_top_hot_new.round(2)], # 2nd column
               line_color='darkslategray',
               fill_color='lightyellow',
               align='left'))
    ], layout = {'title' : f'Top Ten Warmest <br> Countries in {year2}', 'title_x': 0.5, 'title_y':0.9}).update_layout(paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',margin=dict(l=20, r=20, b=20, t=100),title_font_size = 25,title_font_color = 'white')


    return [fig1,fig2,fig3,fig4,fig5,fig6,fig7,fig8]


#%%
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=False,host="0.0.0.0",port=8080)




# %%

#html.A(
#        html.Img(src='https://es.m.wikipedia.org/wiki/Archivo:LinkedIn_logo_initials.png', height='32', width='32'),
#        href='https://www.linkedin.com/in/christian-adri%C3%A1n-%C3%A1lvarez-b%C3%A1ez-264a8aa4/')
#Experiment with this 
#https://www.w3schools.com/html/tryit.asp?filename=tryhtml_images_background8
#https://dev.to/omeal/how-to-build-a-curved-ui-header-51dm

#playground for images
#https://www.w3schools.com/cssref/tryit.php?filename=trycss3_background-size

# %%
    
#    dbc.Container(
#            [
#             dbc.Row([
#        dbc.Col(
#            html.P('Author: Christian Álvarez', style = {'color': '#60d7f7'}),
#                    ),   
#            html.A(
#                html.Img(src='https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png', height='32', width='32'),
#                href='https://www.linkedin.com/in/christian-adri%C3%A1n-%C3%A1lvarez-b%C3%A1ez-264a8aa4/')    
#            ], style={'background-color': '#000000', 'display':'inline-block'})
#            ]),