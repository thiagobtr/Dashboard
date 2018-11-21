import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

#external=['https://cdn.rawgit.com/xhlulu/0acba79000a3fd1e6f552ed82edb8a64/raw/dash_template.css']

app = dash.Dash(__name__)
#Carrega arquivo de classificacao
df_tabela = pd.read_csv('/media/sf_FormacaoCientistaDeDados/Portfolio/Dashboard/Data/tabela_final.csv')
#filtra pela Rodada 38
df_tabela = df_tabela[df_tabela['Rodada'] == 38]
#Carrega arquivo de artilheiros e assistencias
df_art_ass = pd.read_csv('/media/sf_FormacaoCientistaDeDados/Portfolio/Dashboard/Data/artilheiros_final.csv')
#Carrega arquivo de Publico
df_publico = pd.read_csv('/media/sf_FormacaoCientistaDeDados/Portfolio/Dashboard/Data/publico_final.csv')

Times = df_tabela['Time'].unique()
Temporada = df_tabela['Temporada'].unique()
ligas = df_tabela['Liga'].unique()

#df = df[df['Rodada']== 38 ]
#Gera DataFrame para criacao do radio button
df_ano = df_tabela[['Temporada','Ano_inicio']].drop_duplicates().sort_values(by='Ano_inicio')

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
            ,options = [{'label':ano[0],'value': ano[1] }for ano in df_ano.itertuples(index=False)]
            ,value = 2015)]
            ,className= 'four columns')
        ,html.Div(html.H1(''),className='three columns')

         ,html.Div(
            children=['Selecione a Liga:',
                dcc.RadioItems(
                    id='radio-liga',
                    options=[{'label':liga,'value': liga }for liga in ligas],
                    value = 'Premier_league',
                    labelStyle={'display':'inline-block'}
                    )
                ]
                ,className='five columns'
            )

        ]
        ,className='row')

        ,html.Div([
                dcc.Graph(
                 id='Tabela-rank',
                  )],className= 'eight columns')

        ,html.Div([
                update_table_publico(2015,'Premier_league')

            ],className='three columns')

        ,html.Div([
            dcc.Graph(
                id='Tabela-art')],className='six columns')
        ,html.Div([
            dcc.Graph(
                id='Tabela-assist')],className='six columns')

],className='container')

@app.callback(
    dash.dependencies.Output('Tabela-rank','figure'),
    [dash.dependencies.Input('dropdown-rodadas','value'),
    dash.dependencies.Input('radio-liga','value')]
)
def update_graph_rank(temp,liga):
    df_temp = df_tabela[(df_tabela['Ano_inicio'] == temp) & (df_tabela['Liga']== liga)]
    temporada = df_temp['Temporada'].unique()
    titulo = 'Pontuação por Time Temporada {}'.format(temporada)
    return {
    'data':[go.Bar(
        x = df_temp['Time']
        ,y= df_temp['Pontos']
        ,text=''
        #,mode='lines+markers'
        )],
        'layout':go.Layout(
                    yaxis={'title':'Pontuação'}
                    ,hovermode='closest'
                    ,title = titulo
                    ,titlefont=dict(size=26,
                     color='#7f7f7f')
                     )

    }

@app.callback(
    dash.dependencies.Output('Tabela-art','figure'),
    [dash.dependencies.Input('dropdown-rodadas','value'),
    dash.dependencies.Input('radio-liga','value')]
)
def update_graph_art(temp,liga):
    df_art = df_art_ass[(df_art_ass['Ano_inicio'] == temp) & (df_art_ass['Liga']== liga)]
    #lista os 10 maiores artilheiros
    df_art = df_art.sort_values(by='gols',ascending = True).tail(10)

    temporada = df_art['Temporada'].unique()
    titulo = 'Lista de Artilheiros Temporada {}'.format(temporada)
    return {
    'data':[go.Bar(
        x = df_art['gols']
        ,y= df_art['Jogador']
        ,orientation = 'h'
        ,text=''
        #,mode='lines+markers'
        )],
        'layout':go.Layout(
                    # hovermode='closest',
                    title = titulo
                    ,titlefont=dict(size=16,
                     color='#7f7f7f')
                     )

    }

@app.callback(
    dash.dependencies.Output('Tabela-assist','figure'),
    [dash.dependencies.Input('dropdown-rodadas','value'),
    dash.dependencies.Input('radio-liga','value')]
)
def update_graph_ass(temp,liga):
    df_ass = df_art_ass[(df_art_ass['Ano_inicio'] == temp) & (df_art_ass['Liga']== liga)]
    #lista os 10 jogadores que realizaram mais assistencias
    df_ass = df_ass.sort_values(by='ass',ascending = True).tail(10)

    temporada = df_ass['Temporada'].unique()
    titulo = 'Lideres em Assistencias Temporada {}'.format(temporada)
    return {
    'data':[go.Bar(
        x = df_ass['ass']
        ,y= df_ass['Jogador']
        ,orientation = 'h'
        #,text= df_ass['ass'] +' Assistencias'
        #,hoverinfo=text
        #,mode='lines+markers'
        )],
        'layout':go.Layout(
                    #hovermode='closest',
                    title = titulo
                    ,titlefont=dict(size=16,
                     color='#7f7f7f')
                     )

    }
@app.callback(
    dash.dependencies.Output('Tabela-publico','figure'),
    [dash.dependencies.Input('dropdown-rodadas','value'),
    dash.dependencies.Input('radio-liga','value')]
)
def update_table_publico(temp,liga):
    df_pop = df_publico[(df_publico['Ano_inicio'] == temp) & (df_publico['Liga']== liga)]
    #lista os 10 jogadores que realizaram mais assistencias
    df_pop = df_pop.sort_values(by='ass',ascending = True).tail(10)
    max_rows =10
    temporada = df_pop['Temporada'].unique()
    titulo = 'Lideres em Assistencias Temporada {}'.format(temporada)
    return html.Table(
        [html.Tr([html.Th(col) for col in df_pop.columns])]+
        [html.Tr([html.Td(df_pop.iloc[i][col])for col in df_pop.columns
        ]) for i in range(min(len(df_pop),max_rows))]


    )


if __name__ == '__main__':
    app.run_server(debug=True)
