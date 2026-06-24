import requests
from pymongo import MongoClient

CONN_STRING = "mongodb://admin:admin@localhost:27017/"
client = MongoClient(CONN_STRING)

db = client["dados_camara"]

colecao_deputados = db["deputados"]
colecao_despesas = db["despesas"]

colecao_deputados.delete_many({})
colecao_despesas.delete_many({})

url_deputados = "https://dadosabertos.camara.leg.br/api/v2/deputados"
parametros = {
    "siglaUf": "PB",
    "idLegislatura": 57
}

resposta = requests.get(url_deputados, params=parametros)

if resposta.status_code == 200:
    json_dados = resposta.json() 
    dados = json_dados['dados']
    print(f"Lista de deputados obtida com sucesso!")
else:
    print(f" A API retornou um erro ao buscar deputados: {resposta.status_code}")
    dados = []


for dado in dados:
    id_deputado = dado['id']
    nome_deputado = dado['nome']
    sigla_partido = dado['siglaPartido']
    sigla_uf = dado['siglaUf']
    url_foto = dado['urlFoto']
    email = dado.get('email', '') 

    documento_deputado = {
        "_id": id_deputado,  
        "nome": nome_deputado,
        "siglaPartido": dado['siglaPartido'],
        "siglaUf": dado['siglaUf'],
        "email": dado.get('email', '')
    }
    colecao_deputados.insert_one(documento_deputado)

    print(f"Iniciando a extração de despesas do deputado(a): {nome_deputado} )")

    
    nova_url = f"https://dadosabertos.camara.leg.br/api/v2/deputados/{id_deputado}/despesas"
    contador_paginas = 1

    while nova_url:
        print(f" Acessando página {contador_paginas} de despesas...")
        resposta_despesas = requests.get(nova_url)
        
        if resposta_despesas.status_code != 200:
            print(f" Erro ao buscar despesas na URL:{nova_url}")
            break 
         
        json_despesas = resposta_despesas.json()
        despesas = json_despesas['dados']
        print(f"{len(despesas)} despesas encontradas nesta página.")
        
        
        for despesa in despesas:
            
            documento_despesa = {
                # O id da despesa será gerado automaticamente como ObjectId pelo Mongo
                "ano": despesa.get('ano'),
                "mes": despesa.get('mes'),
                "tipoDespesa": despesa.get('tipoDespesa'),
                "numDocumento": despesa.get('codDocumento'),     
                "urlDocumento": despesa.get('urlDocumento'),
                
                # Referência pura ao ID do deputado (linha de associação 1..*)
                "deputado_id": id_deputado,

                # Agregação: Valores (documento, glosa, liquido)
                "valores": {
                    "documento": despesa.get('valorLiquido', 0) + despesa.get('valorGlosa', 0), 
                    "glosa": despesa.get('valorGlosa', 0),  
                    "liquido": despesa.get('valorLiquido', 0)
                },

                # Agregação: Fornecedor (cnpjCpf, nome)
                "fornecedor": {
                    "cnpjCpf": despesa.get('cnpjCpfFornecedor'),
                    "nome": despesa.get('nomeFornecedor')
                }
            }
            colecao_despesas.insert_one(documento_despesa)

       
        links = json_despesas.get('links', [])
        proxima_pagina = None

        for link in links:
            if link['rel'] == 'next':
                proxima_pagina = link['href']
                   
        
        nova_url = proxima_pagina
        contador_paginas += 1

print("Processo de ETL concluído!")
