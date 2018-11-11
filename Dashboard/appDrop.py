import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

external=['https://cdn.rawgit.com/xhlulu/0acba79000a3fd1e6f552ed82edb8a64/raw/dash_template.css']

app = dash.Dash(__name__)

df = pd.read_csv('/media/sf_FormacaoCientistaDeDados/Portfolio/Dashboard/Data/rank_premier.csv')

Times = df['Time'].unique()

#df = df[df['Rodada']== 38 ]


app.layout = html.Div(children=[
html.Div([
    html.Div(
        className="banner",
        children=[html.H2('Plotly Dash')]
    )],className='row'
    ),
    html.Div([
        html.Div(className='three columns',
        style={'margin-top': '10'},
        children=[
        dcc.Dropdown(
        id='dropdown-rodadas'
        ,options = [{'label':time ,'value':time}for time in Times]
        ,value = 'Everton')])
        ],className= 'row')

    ,html.Div([
    dcc.Graph(
    id='Tabela-Premier',
    )
    ]
    ,className='eight columns'),
    html.H5('Teste H5 Teste H5 Teste H5 Teste H5 Teste H5  Teste H5 Teste H5 Teste H5 Teste H5'
    ,className='three columns')

],className='container')

@app.callback(
    dash.dependencies.Output('Tabela-Premier','figure'),
    [dash.dependencies.Input('dropdown-rodadas','value')]
)
def update_graph(valor_time):
    df_time= df[df['Time']== valor_time]
    return {
    'data':[go.Scatter(
        x = df_time['Rodada']
        ,y= df_time['Pontos']
        ,text=valor_time
        ,mode='lines+markers'
        )],
        'layout':go.Layout(
                    yaxis={'title':'Pontuação'},
                    hovermode='closest'
                    )

    }
if __name__ == '__main__':
    app.run_server(debug=True)
