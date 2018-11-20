import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

#external=['https://cdn.rawgit.com/xhlulu/0acba79000a3fd1e6f552ed82edb8a64/raw/dash_template.css']

app = dash.Dash(__name__)

df = pd.read_csv('/media/sf_FormacaoCientistaDeDados/Portfolio/Dashboard/Data/tabela_final.csv')

Times = df['Time'].unique()

#df = df[df['Rodada']== 38 ]
#Gera DataFrame para criacao do radio button
df_ano = df[['Temporada','Ano_inicio']].drop_duplicates().sort_values(by='Ano_inicio')

app.layout = html.Div(children=[
        html.Div(
            className="banner",
            children=[html.H2('Plotly Dash')]
        ),
        html.Div([
            html.Div(
            style={'margin-top': '10'},
            children=[
            dcc.Dropdown(
            id='dropdown-rodadas'
            ,options = [{'label':time ,'value':time}for time in Times]
            ,value = 'Everton FC')]
            ,className= 'four columns')
        ,html.Div(html.H1(''),className='three columns')

         ,html.Div(
            children=['Selecione a Temporada:',
                dcc.RadioItems(
                    id='radio-temporada',
                    options=[{'label':ano[0],'value': ano[1] }for ano in  df_ano.itertuples(index=False)],
                    value = 2015,
                    labelStyle={'display':'inline-block'}
                    )
                ]
                ,className='five columns'
            )

        ]
        ,className='row')

        ,html.Div([
                dcc.Graph(
                 id='Tabela-Premier',
                  )],className= 'eight columns')

        ,html.H5('Teste H5 Teste H5 Teste H5 Teste H5 Teste H5  Teste H5 Teste H5 Teste H5 Teste H5'
        ,className='three columns')
],className='container')

@app.callback(
    dash.dependencies.Output('Tabela-Premier','figure'),
    [dash.dependencies.Input('dropdown-rodadas','value'),
    dash.dependencies.Input('radio-temporada','value')]
)
def update_graph(valor_time,ano):
    df_time= df[(df['Time']== valor_time) & (df['Ano_inicio']== ano)]
    temporada = df_time['Temporada'].unique()
    titulo = 'Pontuação por Time Temporada {}'.format(temporada)
    return {
    'data':[go.Scatter(
        x = df_time['Rodada']
        ,y= df_time['Pontos']
        ,text=valor_time
        ,mode='lines+markers'
        )],
        'layout':go.Layout(
                    yaxis={'title':'Pontuação'}
                    ,hovermode='closest'
                    ,title = titulo
                    ,titlefont=dict(size=26,
                     color='#7f7f7f')
                     )

    }
if __name__ == '__main__':
    app.run_server(debug=True)
