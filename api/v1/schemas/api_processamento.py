from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from api.usuario import database, caminho
import time
import psycopg2

def raspar(base_url, xpath, ano_inicial=1970, ano_final=2023):
    opcoes_chrome = Options()
    opcoes_chrome.add_argument("--headless")  
    servico = Service(caminho) # Colocar o caminho do WebDriver ou usar o modo direto

    navegador = webdriver.Chrome(service=servico, options=opcoes_chrome)

    todos_dados = []

    for ano in range(ano_inicial, ano_final + 1):
        url = f"{base_url}&ano={ano}"
        navegador.get(url)
        time.sleep(2)

        try:
            tabela = navegador.find_element(By.XPATH, xpath)
            linhas = tabela.find_elements(By.TAG_NAME, 'tr')
            for linha in linhas:
                colunas = linha.find_elements(By.TAG_NAME, 'td')
                if len(colunas) >= 2:
                    chave = colunas[0].text
                    valor = colunas[1].text
                    todos_dados.append((ano, chave, valor))
        except Exception as e:
            todos_dados.append((ano, "Erro ao raspar a tabela:", str(e)))

    navegador.quit()
    return todos_dados

def salvar(dados, nome_tabela, db_nome=database['db_name'], db_usuario=database['db_user'], db_senha=database['db_password'], db_host=database['db_host'], db_porta=database['db_port']): # Colocar dados do banco de dados Postgres
    try:
        conexao = psycopg2.connect(
            dbname=db_nome,
            user=db_usuario,
            password=db_senha,
            host=db_host,
            port=db_porta
        )
        cursor = conexao.cursor()
        
        # Cria a tabela se não existir
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {nome_tabela} (
            id SERIAL PRIMARY KEY,
            ano INT,
            chave TEXT,
            valor TEXT
        )
        """)
        
        # Insere os dados na tabela
        for ano, chave, valor in dados:
            cursor.execute(f"INSERT INTO {nome_tabela} (ano, chave, valor) VALUES (%s, %s, %s)", (ano, chave, valor))
        
        conexao.commit()
        cursor.close()
        conexao.close()
        print(f"Dados inseridos na tabela {nome_tabela} no banco de dados PostgreSQL com sucesso.")
    except Exception as erro:
        print(f"Erro ao conectar ou inserir na tabela {nome_tabela} no banco de dados PostgreSQL:", erro)
