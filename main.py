from fastapi import FastAPI
from api.v1.schemas.api_producao import scrape, save
from api.v1.schemas.api_processamento import scrape, save 
from api.v1.schemas.api_comercializacao import scrape, save
from api.v1.schemas.api_importacao import scrape, save 
from api.v1.schemas.api_exportacao import scrape, save

app = FastAPI(
    title="Documentação API || Curso Machine Learning Engineering || Grupo 2",
    version="0.0.1",
    description="Esta API foi desenvolvida com o objetivo de guiar o grupo na criação de um projeto para o Tech Challenge."
)

@app.get("/producao",
        description='Produção de vinhos, sucos e derivados',
        summary='Retorna todos os dados desde de 1970 a 2023',
        tags=['Produção de Vinhos']
        )
def read_producao(base_url: str = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02"):
    result = scrape(base_url)
    save(result) 
    return {"data": result}

@app.get("/processamento/{categoria}",
        description='Dados de processamento de vinhos, sucos e derivados',
        summary='Retorna todos os dados desde de 1970 a 2023',
        tags=['Processamento de Vinhos']
        )
def read_processamento(categoria: str):
    categorias = {
        "viniferas": {
            "url": "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_01&opcao=opt_03",
            "xpath": "/html/body/table[4]/tbody/tr/td[2]/div/div/table[1]"
        },
        "americanas_e_hibridas": {
            "url": "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_02&opcao=opt_03",
            "xpath": "/html/body/table[4]/tbody/tr/td[2]/div/div/table[1]"
        },
        "uvas_de_mesa": {
            "url": "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_03&opcao=opt_03",
            "xpath": "/html/body/table[4]/tbody/tr/td[2]/div/div/table[1]"
        },
        "sem_classificacao": {
            "url": "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_04&opcao=opt_03",
            "xpath": "/html/body/table[4]/tbody/tr/td[2]/div/div/table[1]"
        }
    }

@app.get("/comercializacao",
        description='Dados de processamento de vinhos, sucos e derivados',
        summary='Retorna todos os dados desde de 1970 a 2023',
        tags=['Comercialização de Vinhos']
        )
def read_comercializacao(base_url: str = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04"):
    result = scrape(base_url)
    save(result) 
    return {"data": result}

@app.get("/importacao/{categoria}",
        description='Dados de processamento de vinhos, sucos e derivados',
        summary='Retorna todos os dados desde de 1970 a 2023',
        tags=['Importação de Vinhos']
        )
def read_importacao(categoria: str ):
    categorias = {
        "vinhos_de_mesa": {
            "url": "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_01&opcao=opt_05",
            "xpath": "/html/body/table[4]/tbody/tr/td[2]/div/div/table[1]"
        },
        "espumantes": {
            "url": "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_02&opcao=opt_05",
            "xpath": "/html/body/table[4]/tbody/tr/td[2]/div/div/table[1]"
        },
        "uvas_frescas": {
            "url": "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_03&opcao=opt_05",
            "xpath": "/html/body/table[4]/tbody/tr/td[2]/div/div/table[1]"
        },
        "uvas_passas": {
            "url": "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_04&opcao=opt_05",
            "xpath": "/html/body/table[4]/tbody/tr/td[2]/div/div/table[1]"
        },
        "suco_de_uvas": {
            "url": "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_05&opcao=opt_05",
            "xpath": "/html/body/table[4]/tbody/tr/td[2]/div/div/table[1]"
        }
    }
    if categoria not in categorias:
        return {"error": "Categoria não encontrada"}

    url = categorias[categoria]["url"]
    xpath = categorias[categoria]["xpath"]
    result = scrape(url, xpath)
    save(result, f"import_{categoria}")  
    return {"data": result}

@app.get("/exportacao/{categoria}",
        description='Exportação de derivados de uva',
        summary='Retorna todos os dados desde de 1970 a 2023',
        tags=['Exportação de Vinhos']
        )
def read_exportacao(categoria: str ):
    categorias = {
        "vinhos_de_mesa": {
            "url": "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_01&opcao=opt_06",
            "xpath": "/html/body/table[4]/tbody/tr/td[2]/div/div/table[1]"
        },
        "espumantes": {
            "url": "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_02&opcao=opt_06",
            "xpath": "/html/body/table[4]/tbody/tr/td[2]/div/div/table[1]"
        },
        "uvas_frescas": {
            "url": "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_03&opcao=opt_06",
            "xpath": "/html/body/table[4]/tbody/tr/td[2]/div/div/table[1]"
        },
        "suco_de_uvas": {
            "url": "http://vitibrasil.cnpuv.embrapa.br/index.php?subopcao=subopt_05&opcao=opt_06",
            "xpath": "/html/body/table[4]/tbody/tr/td[2]/div/div/table[1]"
        }
    }

    if categoria not in categorias:
        return {"error": "Categoria não encontrada"}

    url = categorias[categoria]["url"]
    xpath = categorias[categoria]["xpath"]
    result = scrape(url, xpath)
    save(result, f"export_{categoria}")  
    return {"data": result}
