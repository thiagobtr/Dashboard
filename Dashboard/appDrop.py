import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
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
            children=['Temporada:',
            dcc.Dropdown(
            id='dropdown-rodadas'
            ,options = [{'label':ano[0],'value': ano[1] }for ano in df_ano.itertuples(index=False)]
            ,value = 2015)]
            ,className= 'four columns')
        ,html.Div(html.H1(''),className='three columns')

         ,html.Div(
            style={'margin-top': '10'},
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

                 )],className= 'seven columns')
        ,html.Div([
                dcc.Graph(
                 #html.Div(id='Tabela-publico'),
                 id='Tabela-publico' )
                  #dash_table.DataTable(
                  #id = 'Tabela-publico',
                  #columns = [{"name":i , 'id':i} for i in df_publico.columns],
                  #data=df_publico.to_dict('rows'),
                  #)

                #update_table_publico(2015,'Premier_league')

            ],className='five columns')

        ,html.Div([
            dcc.Graph(
                id='Tabela-art')],className='seven columns')
        ,html.Div([
            dcc.Graph(
                id='Dot-Plot-assist')],className='five columns')

],className='container')

@app.callback(
    dash.dependencies.Output('Tabela-rank','figure'),
    [dash.dependencies.Input('dropdown-rodadas','value'),
    dash.dependencies.Input('radio-liga','value')]
)
def update_graph_rank(temp,liga):
    df_temp = df_tabela[(df_tabela['Ano_inicio'] == temp) & (df_tabela['Liga']== liga)]
    temporada = df_temp['Temporada'].unique()
    titulo = 'Pontuação por Time Temporada {}'.format(temporada[0])
    return {
    'data':[go.Bar(
        x = df_temp['Time']
        ,y= df_temp['Pontos']
        ,text=''
        ,marker={'color':'rgb(55, 83, 109)'}
        #,mode='lines+markers'
        )],
        'layout':go.Layout(
                    yaxis={'title':'Pontuação'}
                    ,hovermode='closest'
                    ,title = titulo
                    ,titlefont=dict(size=26,
                     color='#7f7f7f')
                     ,xaxis=dict(tickangle=-45)
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
    titulo = 'Lista de Artilheiros Temporada {}'.format(temporada[0])
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

'''
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
    titulo = 'Lideres em Assistencias Temporada {}'.format(temporada[0])
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
    '''
@app.callback(
    dash.dependencies.Output('Tabela-publico','figure'),
    [dash.dependencies.Input('dropdown-rodadas','value'),
    dash.dependencies.Input('radio-liga','value')]
)
def update_table_publico(temp,liga):
    df_pop = df_publico[(df_publico['Ano_inicio'] == temp) & (df_publico['Liga']== liga)]
    #lista os 10 jogadores que realizaram mais assistencias
    df_pop = df_pop.sort_values(by='Rank',ascending = True)#.head(20)
    max_rows =20
    temporada = df_pop['Temporada'].unique()
    titulo = 'Lideres de Público na Temporada {}'.format(temporada[0])
    return {
    'data':[go.Table(
        columnwidth = [30,30,100],
        header = dict(values=['Rank','Média','Time'],
        fill = dict(color = 'rgb(55, 83, 109)'),
        font = dict(color = 'white')),
        cells = dict(values = [df_pop.Rank,round(df_pop.Media,3),df_pop.Time])
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


    #dash_table.DataTable(
    #id = 'Tabela-publico',
    #columns = [{"name":i , 'id':i} for i in df_pop.columns],
    #data=df.to_dict('rows'),

    #)
    }

@app.callback(
    dash.dependencies.Output('Dot-Plot-assist','figure'),
    [dash.dependencies.Input('dropdown-rodadas','value'),
    dash.dependencies.Input('radio-liga','value')]
)
def update_graph_ass(temp,liga):
    df_saldo = df_tabela[(df_tabela['Ano_inicio'] == temp) & (df_tabela['Liga']== liga)]
    #lista os 10 jogadores que realizaram mais assistencias
    df_saldo = df_saldo.sort_values(by=['Pontos','Gols_pro'],ascending = True).tail(10)

    temporada = df_saldo['Temporada'].unique()
    titulo = 'Diferença de Gols a favor e contra. Temporada {}'.format(temporada[0])
    trace1 = {'x':df_saldo['Gols_pro'],
              'y':df_saldo['Time'],
              'marker':{'color':'blue','size':12},
              'mode':'markers',
              'name': 'Gols a favor',
              'type':'scatter'}

    trace2 = {'x':df_saldo['Gols_con'],
              'y':df_saldo['Time'],
              'marker':{'color':'red','size':12},
              'mode':'markers',
              'name': 'Gols contra',
              'type':'scatter'}
    data =[trace1,trace2]

    return {
        'data':go.Figure(
            data=data,
            layout=go.Layout(
                        #hovermode='closest',
                        title = titulo
                        ,titlefont=dict(size=16,
                         color='#7f7f7f')
                         ))

    }

if __name__ == '__main__':
    app.run_server(debug=True)
