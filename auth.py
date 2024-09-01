import streamlit as st
import psycopg2
import hashlib
import jwt
import time
from api.usuario import database

# Chave secreta para codificar e decodificar JWT
CHAVE_SECRETA = 'secret_key'

# Função para gerar o hash da senha
def gerar_hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# Função para autenticar o usuário usando o banco de dados PostgreSQL
def autenticar(usuario, senha):
    try:
        conn = psycopg2.connect(
            dbname=database['db_name'],
            user=database['db_user'],
            password=database['db_password'],
            host=database['db_host']
        )
        cursor = conn.cursor()
        cursor.execute("SELECT senha FROM usuarios WHERE usuario = %s", (usuario,))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            senha_armazenada = resultado[0]
            if gerar_hash_senha(senha) == senha_armazenada:
                token = jwt.encode({'user': usuario, 'exp': time.time() + 3600}, CHAVE_SECRETA, algorithm='HS256')
                return token

        return None
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para registrar novos usuários
def registrar_usuario(usuario, senha):
    hash_senha = gerar_hash_senha(senha)
    try:
        conn = psycopg2.connect(
            dbname=database['db_name'],
            user=database['db_user'],
            password=database['db_password'],
            host=database['db_host']
        )
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (usuario, senha) VALUES (%s, %s)",
            (usuario, hash_senha)
        )
        conn.commit()
        conn.close()
        st.success('Usuário registrado com sucesso!')
    except Exception:
        st.error(f"Usuário já existe.")

# Função para verificar o token
def verificar_token(token):
    try:
        decodificado = jwt.decode(token, CHAVE_SECRETA, algorithms=['HS256'])
        return decodificado['user']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Função para mostrar a tela de login e permitir o registro de novos usuários
def tela_login():
    st.set_page_config(page_title='Login', page_icon='🔒')
    st.title('Login')
    
    # Alternar entre Login e Registro
    acao = st.radio("Escolha uma ação", ["Login", "Registrar"])

    if acao == "Login":
        st.subheader('Por favor, entre com suas credenciais')
        usuario = st.text_input('Usuário')
        senha = st.text_input('Senha', type='password')

        if st.button('Login'):
            token = autenticar(usuario, senha)
            if token:
                st.session_state['token'] = token
                st.session_state['logado'] = True
                st.success('Login bem-sucedido!')
            else:
                st.error('Credenciais inválidas. Tente novamente.')

    elif acao == "Registrar":
        st.subheader('Registrar Novo Usuário')
        novo_usuario = st.text_input('Novo Usuário')
        nova_senha = st.text_input('Nova Senha', type='password')
        
        if st.button('Registrar'):
            if novo_usuario and nova_senha:
                registrar_usuario(novo_usuario, nova_senha)
            else:
                st.warning('Por favor, preencha todos os campos para registrar um novo usuário.')
