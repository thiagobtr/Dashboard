import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash(__name__)

df = pd.read_csv('/media/sf_FormacaoCientistaDeDados/Portfolio/Dashboard/Data/rank_premier.csv')

df = df[df['Rodada']== 38 ]

app.layout = html.Div([
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
])

if __name__ == '__main__':
    app.run_server(debug=True)
