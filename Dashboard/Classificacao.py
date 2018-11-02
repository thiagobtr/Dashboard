#Biblioteca usada para requisitar uma pagina web
import urllib.request
import pandas as pd
from pymongo import MongoClient
from bs4 import BeautifulSoup

def Carrega_table(url):
    # Definimos a url
    # Verifique as permissões em https://www.python.org/robots.txt
    with urllib.request.urlopen(url) as url:
        page = url.read()


    # Analise o html na variável 'page' e armazene-o no formato Beautiful Soup
    soup = BeautifulSoup(page, "html.parser")

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


    Tabela_PremierLeague = pd.DataFrame.from_records(dados_ok,columns = head)

    Tabela_PremierLeague.rename(columns={'#':'rank','M.':'M','Dif.':'Dif','Pt.':'Pt'},inplace=True)

    #Conectando ao Mongodb

    conn = MongoClient('localhost',27017)

    #Criacao do Banco
    db = conn.RankGeral

    #Cricao da colecao
    Premier_collection = db.PremierLeague_Table

    PremierLeagueDict = Tabela_PremierLeague.to_dict('records')


    #inserindo dados na colecao
    resultado = Premier_collection.insert_many(PremierLeagueDict)
    print (resultado)
