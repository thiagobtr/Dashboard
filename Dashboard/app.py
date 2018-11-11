import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

external=['https://cdn.rawgit.com/xhlulu/0acba79000a3fd1e6f552ed82edb8a64/raw/dash_template.css']

app = dash.Dash(__name__)

df = pd.read_csv('/media/sf_FormacaoCientistaDeDados/Portfolio/Dashboard/Data/rank_premier.csv')

Times = df['Time'].unique()

df = df[df['Rodada']== 38 ]


app.layout = html.Div(children=[
html.Div([
    html.Div(
        className="banner",
        children=[html.H2('Plotly Dash')]
    )],className='row'
    ),html.Div([
    dcc.Graph(
    id='Tabela-Premier',
    figure={
        'data':[
            go.Bar(
                x= df['Time'],
                y= df['Pontos'],
                name = 'Time' #df['Time'].unique()

                )
            ],
            'layout':go.Layout(
                yaxis={'title':'Pontuação'},
                hovermode='closest'
            )
        }
    )
    ]
    ,className='eight columns'),
    html.H5('Teste H5 Teste H5 Teste H5 Teste H5 Teste H5  Teste H5 Teste H5 Teste H5 Teste H5'
    ,className='three columns')

])

if __name__ == '__main__':
    app.run_server(debug=True)
