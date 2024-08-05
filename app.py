import streamlit as st
import pandas as pd
import jwt
import time
import psycopg2
from api.usuario import database

# Chave secreta para codificar e decodificar JWT (Código do Adilson)
SECRET_KEY = 'secret_key'

# Função para autenticar o usuário
def authenticate(username, password):
    if username == 'admin' and password == 'password': # Usuário e senha de exemplo (Podemos deixar isso mais dinamico)
        token = jwt.encode({'user': username, 'exp': time.time() + 3600}, SECRET_KEY, algorithm='HS256')
        return token
    return None

# Função para verificar o token
def verify_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded['user']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Função para mostrar a tela de login
def login_screen():
    st.title('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        token = authenticate(username, password)
        if token:
            st.session_state['token'] = token
            st.success('Login successful')
            #st.experimental_rerun()
        else:
            st.error('Invalid credentials')

# Função para conectar ao banco de dados PostgreSQL e obter os dados
def get_data_from_db():
    conn = psycopg2.connect(
        dbname=database['db_name'],
        user=database['db_user'],
        password=database['db_password'],
        host=database['db_host']
    )
    query = "SELECT expo.ano, expo.chave as pais, expo.valor, pais.latitude, pais.longitude FROM export_espumantes expo JOIN paises as pais ON expo.chave = pais.pais"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Função para mostrar o dashboard
def dashboard():
    st.title('Dashboard Interativo - TechChallange GrupoDois')
    
    try:
        df = get_data_from_db()
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return
    
    # Mostrar os dados
    st.write(df)

    # Gráfico interativo de mapa
    st.map(df)

# Verificar se o usuário está logado
# Ainda não esta rodando
if 'token' in st.session_state:
    user = verify_token(st.session_state['token'])
    if user:
        dashboard()
    else:
        st.error('Sessão expirada. Por favor, faça login novamente.')
        login_screen()
else:
    login_screen()
