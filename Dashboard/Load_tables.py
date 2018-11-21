#Biblioteca usada para requisitar uma pagina web
import urllib.request
import pandas as pd
from pymongo import MongoClient
from bs4 import BeautifulSoup




def Carrega_table(url,liga,rodada,temporada):
    # Definimos a url
    # Verifique as permissões em https://worldfootball.net/robots.txt
    with urllib.request.urlopen(url) as url:
        page = url.read()


    # Analise o html na variável 'page' e armazene-o no formato Beautiful Soup
    soup = BeautifulSoup(page, "html.parser")

    ####Seleciona a Rodada
    #rodada = soup.find_all('option',{'class':"wahl"})[1]
    #rodada = rodada.get_text(strip=True).split('.')[0]

    #selecionando tabela com a classe
    Classif = soup.find_all('table',{'class':"standard_tabelle"})[1]

    Cabecalho = Classif.find_all('th')

    #Selecionando cabecalho
    head = []
    for rows in Cabecalho:
        head.append(rows.get_text(strip=True))
        #print(type(rows))

    #Selecionando dados para criacao do dataset
    dados = []
    for linha in Classif.find_all('tr')[1:]:
        dados.append([campo.get_text(strip=True) for campo in linha.find_all('td') ])


    dados_ok=[]
    for d in dados:
        d.pop(1)
        dados_ok.append(d)


    tabela_liga = pd.DataFrame.from_records(dados_ok,columns = head)

    tabela_liga.rename(columns={'#':'rank','M.':'M','Dif.':'Dif','Pt.':'Pt'},inplace=True)

    #Cria coluna 'Rodada'
    tabela_liga['Rodada'] = rodada

    #Cria coluna 'Temporada'
    tabela_liga['Temporada'] = temporada

    #Cria coluna 'Temporada'
    tabela_liga['Liga'] = liga

    #Cria DataFrame
    tabela_liga_dict = tabela_liga.to_dict('records')

    #Conectando ao Mongodb
    conn = MongoClient('localhost',27017)

    #Criacao do Banco 'Ligas_futebol'
    db = conn.Ligas_futebol
    #db = conn[banco]

    #Criacao/Conexao da colecao
    liga_rank = db.Rank

    #Verfica se os items ja existem
    if liga_rank.find_one({'$and':[{'Rodada':rodada},{'Temporada':temporada},{'Liga':liga}]}):
        #remove todos os documentos
        liga_rank.delete_many({'$and':[{'Rodada':rodada},{'Temporada':temporada},{'Liga':liga}]})

    #inserindo dados na colecao
    resultado = liga_rank.insert_many(tabela_liga_dict)

    return (resultado)


def Carrega_placar(url,liga,rodada,temporada):
    with urllib.request.urlopen(url) as url:
        page = url.read()

    # Analise o html na variável 'page' e armazene-o no formato Beautiful Soup
    soup = BeautifulSoup(page, "html.parser")

    #selecionando tabela com a classe
    Tabela_jogos = soup.find_all('table',{'class':"standard_tabelle"})[0]
    Tabela_jogos_linha = Tabela_jogos.find_all('tr')
    header = ['Data','Hora','Home','campo1','Away','Placar','campo2','campo3']

    jogos=[]
    #pos = [0,1,2,4,5]
    for jogo in Tabela_jogos_linha:
        jogos.append([partida.get_text(strip=True) for partida in jogo.find_all('td')])


    #Cria DataFrame
    Partidas = pd.DataFrame.from_records(jogos,columns = header)
    #Exclui campos desnecessarios
    Partidas.drop(['campo1','campo2','campo3'] ,axis = 1,inplace = True)
    #Formata o variavel 'placar' e cria variavel 'Rodada'
    placar = [placar[0] for placar in Partidas['Placar'].str.split('(').tolist()]
    Partidas['Placar'] = placar

    #Cria variavel 'Rodada'
    Partidas['Rodada'] = rodada

    #Cria variavel 'Temporada'
    Partidas['Temporada'] = temporada

    #Cria variavel 'Liga'
    Partidas['Liga'] = liga

    #Conectando ao Mongodb
    conn = MongoClient('localhost',27017)

    #Criacao/Conexao do Banco
    db = conn.Ligas_futebol

    #Criacao da colecao
    Placar_collection = db.Rodadas
    Placar_dict = Partidas.to_dict('records')


    #Verfica se os items ja existem
    if Placar_collection.find_one({'$and':[{'Rodada':rodada},{'Temporada':temporada},{'Liga':liga}]}):
        #remove todos os documentos
        Placar_collection.delete_many({'$and':[{'Rodada':rodada},{'Temporada':temporada},{'Liga':liga}]})

    #inserindo dados na colecao
    Dados_placar = Placar_collection.insert_many(Placar_dict)

def Carrega_art_ass (url,liga,temporada):

    with urllib.request.urlopen(url) as url:
        page = url.read()

    # Analise o html na variável 'page' e armazene-o no formato Beautiful Soup
    soup = BeautifulSoup(page, "html.parser")
    scorer_table = soup.find_all('table',{'class':"standard_tabelle"})[0]
    header = scorer_table.find_all('th')
    header_scorer = []
    for cab in header:
        header_scorer.append(cab.get_text(strip=True))

    scorer_row = scorer_table.find_all('tr')

    #cria lista coms os valores
    scorer =[]

    for scorers in scorer_row:
        scorer.append([scorer_col.get_text(strip=True) for scorer_col in scorers.find_all('td')])

    #cria DataFrame
    df_scorer = pd.DataFrame.from_records(scorer,columns = header_scorer)
    df_scorer.rename(columns={'#':'rank'},inplace=True)

    #Exclui valores nulos
    df_scorer.dropna(inplace=True)

    df_scorer['points'] = df_scorer['points'].str.split('+')
    #crias variaveis gols e ass
    gols = [valor[0] for valor in df_scorer['points']]
    ass = [valor[1] for valor in df_scorer['points']]
    df_scorer['gols'] = gols
    df_scorer['ass'] = ass


    df_scorer['ass'] = df_scorer['ass'].str.split(')',expand=True)[0]

    df_scorer['gols'] = df_scorer['gols'].str.split('(',expand=True)[1]

    #df_scorer['Rodada'] = rodada

    df_scorer['Liga'] = liga

    df_scorer['Temporada'] = temporada

    #Conectando ao Mongodb
    conn = MongoClient('localhost',27017)

    #Criacao/Conexao do Banco
    db = conn.Ligas_futebol
    #db = conn[banco]

    #Criacao da colecao
    Score_collection = db.score

    Scorer_dict = df_scorer.to_dict('records')

    #Verfica se os items ja existem
    if Score_collection.find_one({'$and':[{'Liga':liga},{'Temporada':temporada}]}):
        #remove todos os documentos
        Score_collection.delete_many({'$and':[{'Liga':liga},{'Temporada':temporada}]})

    #inserindo dados na colecao
    resultado = Score_collection.insert_many(Scorer_dict)
    print(resultado)

def Carrega_publico(url,liga,temporada):
    with urllib.request.urlopen(url) as url:
        page = url.read()

    # Analise o html na variável 'page' e armazene-o no formato Beautiful Soup
    soup = BeautifulSoup(page, "html.parser")
    tabela_publico = soup.find_all('table',{'class':"standard_tabelle"})[0]
    #Cabecalho
    cabecalho = ['Rank','campo_vazio','Time','Total','Jogos','Media']

    #Extrai os dados da tabela
    Tabela_publico_dados = tabela_publico.find_all('tr')[1:]


    #Extrai os dados para criacao do dataframe
    dados=[]
    for linha in Tabela_publico_dados:
        dados.append([campo.get_text(strip=True) for campo in linha.find_all('td')])

    df_publico = pd.DataFrame.from_records(dados,columns = cabecalho)

    #Exclui campo desnecessarios
    df_publico.drop('campo_vazio',axis=1,inplace=True)

    #df_scorer['Rodada'] = rodada

    df_publico['Liga'] = liga

    df_publico['Temporada'] = temporada

    #Conectando ao Mongodb
    conn = MongoClient('localhost',27017)

    #Criacao/Conexao do Banco
    db = conn.Ligas_futebol
    #db = conn[banco]

    #Criacao da colecao
    Colecao_publico = db.Publico

    Publico_dict = df_publico.to_dict('records')

    #Verfica se os items ja existem
    if Colecao_publico.find_one({'$and':[{'Liga':liga},{'Temporada':temporada}]}):
        #remove todos os documentos
        Colecao_publico.delete_many({'$and':[{'Liga':liga},{'Temporada':temporada}]})

    #inserindo dados na colecao
    resultado = Colecao_publico.insert_many(Publico_dict)
    print(resultado)
