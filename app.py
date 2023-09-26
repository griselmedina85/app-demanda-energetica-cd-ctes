# Importa las bibliotecas necesarias
from dash import Dash, dash_table, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# Carga tus datos
df = pd.read_csv('demanda_energia_mwh - demanda_energia_mwh.csv')

# Renombra las columnas del DataFrame
# df = df.rename(columns={'periodo': 'Período', 
#                         'demanda_comercial': 'Demanda Comercial', 
#                         'demanda_industrial/comercial_grande': 'Demanda Industrial/Comercial Grande',
#                         'demanda_residencial':'Demanda Residencial',})

# Inicializa la aplicación con un tema de Bootstrap
app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])

server = app.server

#css tabs
tabs_style = {
    'height' : '44 px'
}
tab_style = {
    'borderBottom' : '1px solid #d6d6d6',
    'padding' : '6px',
    'fontWeight' : 'bold'
}
tab_selected_style = {
    'borderTop' : '1px solid #d6d6d6',
    'borderBottom' : '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color' : 'white',
    'padding' : '6px'
}



# Define el diseño de las pestañas anidadas
app.layout = dbc.Container([
    html.Link(rel='stylesheet', href='/assets/styles.css'),
    dbc.Row([
        html.Div([
            html.Img(src='https://www.cumbrededatos.ar/assets/img/logo/logo-CD.png', height='auto',width='200px', style={'float': 'left', 'margin-top': '1%'}),  # Reemplaza 'URL_DE_TU_LOGO.png' con la URL o la ruta de tu imagen
            html.H1('Dashboard Demanda de Energía Eléctrica', className="app-title", style={'float': 'right'}),
        ]),
    ]),
    
     dbc.Row(children=[
        html.Hr(),
        html.Div('Demanda de Energía Eléctrica, en MWh (Megavatio por hora) para la Provincia de Corrientes desde enero de 2017', className="text-primary text-center fs-4")
    ]),
    
    html.Br(),
    
    dcc.Tabs(id='pestanas-radio-buttons-final', value='tab_tabla', children=[
        dcc.Tab(label='Tabla de Datos Completa', value='tab_tabla', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Demanda Comercial', value='demanda_comercial', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Demanda Industrial/Comercial Grande', value='demanda_industrial/comercial_grande', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Demanda Residencial', value='demanda_residencial', style=tab_style, selected_style=tab_selected_style),
        
    ], style=tabs_style),
    
    dcc.Loading(id="loading", type="default", children=[
        dcc.Graph(figure={}, id="my-first-graph-final", style={'display': 'block'})
    ]),
    
    dbc.Row([
        html.Div('Tabla de Datos', className="text-primary text-center fs-3")
    ]),
    
    html.Br(),

    dbc.Row([
        html.Div(
        dash_table.DataTable(
            id="tabla-datos",
            page_size=12, 
            style_table={'overflowX': 'auto'}, 
            style_cell={'width':'auto'},
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248,248,248)'
                }
                ],
            style_header={
                'backgroundColor' : 'rgb(230,230,230)',
                'fontWeight': 'bold'
            },
        ),
        )
    ]),
    
    html.Footer([
        html.Div("Datathon 2023 © Griselda Medina", style={'textAlign': 'center', 'padding': '10px', 'backgroundColor': '#f0f0f0'}),
    ], style={'bottom': '0', 'width': '100%'})
    
    
], fluid=True)



# Define el contenido de cada pestaña anidada
@app.callback(
    Output(component_id='my-first-graph-final', component_property='figure'),
    Output(component_id='tabla-datos', component_property='data'),    
    Input(component_id='pestanas-radio-buttons-final', component_property='value')
)
def update_content(selected_tab):
     
    print(selected_tab)
    
   #agrego tab tabla completa
    if selected_tab == 'tab_tabla':
        #print('tablaaaaaaaaaaaaa')
                
        #Actualiza el gráfico
        #fig = empty_figure
        #fig = px.scatter(df, x='periodo', y=selected_tab, labels={'periodo': 'Fecha', selected_tab: 'Valor'})
        fig = go.Figure()
        for col in df.columns:
            if col != 'periodo':
                fig.add_trace(go.Scatter(x=df['periodo'], y=df[col], mode='lines', name=col))
                

        #Actualiza tabla de datos
        data = df.to_dict('records')
        
    else:
        #Filtra el dataframe en función de la pestaña seleccionada
        filtered_df = df[df[selected_tab].notna()]
        
        #Actualiza el gráfico
        fig = px.histogram(filtered_df, x='periodo', y=selected_tab, histfunc='avg')
    
        
        # mapa de selected_tab a columnas correspondientes
        column_mapping = {
            'demanda_comercial' : [ 'demanda_comercial' ],
            'demanda_industrial/comercial_grande' : [ 'demanda_industrial/comercial_grande' ],
            'demanda_residencial' : [ 'demanda_residencial' ]
        }
        
        #obtener columnas 
        selected_columns = column_mapping.get(selected_tab, [])
        
        # filtro dataframe df basado en las columnas seleccionadas
        filtered_df = df[['periodo'] + selected_columns]
        
        #Actualiza tabla de datos
        data = filtered_df.to_dict('records')
    
    #Cambio rótulo en el eje y
    fig.update_yaxes(title_text='MWh')  
    #fig.update_layout(title=f'Gráfico para {selected_tab}')
    
    return fig, data

 
    


# Ejecuta la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
