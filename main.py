from fastapi import FastAPI
from api.v1.schemas.api_producao import raspar, salvar
from api.v1.schemas.api_processamento import raspar, salvar 
from api.v1.schemas.api_comercializacao import raspar, salvar
from api.v1.schemas.api_importacao import raspar, salvar 
from api.v1.schemas.api_exportacao import raspar, salvar

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
def ler_producao(url_base: str = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02"):
    resultado = raspar(url_base)
    salvar(resultado) 
    return {"dados": resultado}

@app.get("/processamento/{categoria}",
        description='Dados de processamento de vinhos, sucos e derivados',
        summary='Retorna todos os dados desde de 1970 a 2023',
        tags=['Processamento de Vinhos']
        )
def ler_processamento(categoria: str):
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

    if categoria not in categorias:
        return {"erro": "Categoria não encontrada"}

    url = categorias[categoria]["url"]
    xpath = categorias[categoria]["xpath"]
    resultado = raspar(url, xpath)
    salvar(resultado, f"processamento_{categoria}")  
    return {"dados": resultado}

@app.get("/comercializacao",
        description='Dados de comercialização de vinhos, sucos e derivados',
        summary='Retorna todos os dados desde de 1970 a 2023',
        tags=['Comercialização de Vinhos']
        )
def ler_comercializacao(url_base: str = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04"):
    resultado = raspar(url_base)
    salvar(resultado) 
    return {"dados": resultado}

@app.get("/importacao/{categoria}",
        description='Dados de importação de vinhos, sucos e derivados',
        summary='Retorna todos os dados desde de 1970 a 2023',
        tags=['Importação de Vinhos']
        )
def ler_importacao(categoria: str ):
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
        return {"erro": "Categoria não encontrada"}

    url = categorias[categoria]["url"]
    xpath = categorias[categoria]["xpath"]
    resultado = raspar(url, xpath)
    salvar(resultado, f"importacao_{categoria}")  
    return {"dados": resultado}

@app.get("/exportacao/{categoria}",
        description='Exportação de derivados de uva',
        summary='Retorna todos os dados desde de 1970 a 2023',
        tags=['Exportação de Vinhos']
        )
def ler_exportacao(categoria: str ):
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
        return {"erro": "Categoria não encontrada"}

    url = categorias[categoria]["url"]
    xpath = categorias[categoria]["xpath"]
    resultado = raspar(url, xpath)
    salvar(resultado, f"exportacao_{categoria}")  
    return {"dados": resultado}
