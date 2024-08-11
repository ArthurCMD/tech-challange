import streamlit as st
import pandas as pd
import jwt
import time
import psycopg2
from api.usuario import database
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# Definindo anos padrão
ANO_INICIAL = 1970
ANO_FINAL = 2024

# Chave secreta para codificar e decodificar JWT
SECRET_KEY = 'secret_key'

# Função para autenticar o usuário
def authenticate(username, password):
    if username == 'admin' and password == 'password':  # Usuário e senha de exemplo
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
    st.set_page_config(page_title='Login', page_icon='🔒')
    st.title('Login')
    st.subheader('Por favor, entre com suas credenciais')
    
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    
    if st.button('Login'):
        token = authenticate(username, password)
        if token:
            st.session_state['token'] = token
            st.success('Login bem-sucedido!')
            st.experimental_rerun()
        else:
            st.error('Credenciais inválidas. Tente novamente.')

# Função para conectar ao banco de dados PostgreSQL e obter os dados
def get_data_from_db(start_year, end_year):
    try:
        conn = psycopg2.connect(
            dbname=database['db_name'],
            user=database['db_user'],
            password=database['db_password'],
            host=database['db_host']
        )
        
        # Query para obter dados para o gráfico de mapa
        query_map = """
            SELECT expo.ano, expo.chave as pais, expo.valor, pais.latitude, pais.longitude 
            FROM export_espumantes expo 
            JOIN paises as pais ON expo.chave = pais.pais
            WHERE CAST(expo.ano AS INTEGER) BETWEEN %s AND %s
            AND expo.valor > 0
            AND pais.pais <> 'Total'
        """
        df_map = pd.read_sql_query(query_map, conn, params=(start_year, end_year))
        
        # Query para obter os 5 maiores valores
        query_top5 = """
            SELECT expo.chave as pais, expo.valor as total_valor, expo.ano
            FROM export_espumantes expo
            WHERE CAST(expo.ano AS INTEGER) BETWEEN %s AND %s
            AND expo.chave <> 'Total'
            GROUP BY expo.valor,expo.chave, expo.ano
            ORDER BY total_valor desc
            LIMIT 5
        """
        df_top5 = pd.read_sql_query(query_top5, conn, params=(start_year, end_year))
        
        conn.close()
        return df_map, df_top5
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return pd.DataFrame(), pd.DataFrame()  # Retornar DataFrames vazios em caso de erro

# Função para criar o gráfico de barras horizontal
def plot_bar_chart(df):
    if df.empty:
        st.warning('Nenhum dado disponível para o gráfico de barras.')
        return

    # Formatar valores como moeda
    df['formatted_value'] = df['total_valor'].apply(lambda x: f'R${x:,.3f}')

    plt.figure(figsize=(10, 6))
    
    # Configurar o fundo do gráfico para transparente
    plt.style.use('dark_background')  # Usar fundo preto para o gráfico
    
    # Criar o gráfico de barras com Seaborn
    ax = sns.barplot(x='total_valor', y='pais', data=df, palette='viridis')

    # Configurar o fundo dos eixos e outros elementos
    ax.set_facecolor('none')  # Fundo dos eixos transparente
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='both', colors='white')

    plt.xlabel('Valor Total', color='white')
    plt.ylabel('País', color='white')
    plt.title('Top 5 Países com Maiores Valores Exportados', color='white')
    
    # Adicionar rótulos de valor no gráfico
    for index, value in enumerate(df['total_valor']):
        plt.text(value, index, f'R${value:,.3f}', va='center', color='white')

    # Salvar a imagem no buffer com fundo transparente
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=300, transparent=True)
    buf.seek(0)
    return buf

# Função para mostrar o dashboard
def dashboard():
    st.set_page_config(page_title='Dashboard Interativo', page_icon='📊', layout='wide')
    st.title('Dashboard Interativo - TechChallange GrupoDois')
    
    # Adicionar filtros de ano
    st.sidebar.header('Filtros de Ano')
    start_year = st.sidebar.number_input('Ano Inicial', min_value=ANO_INICIAL, max_value=ANO_FINAL, value=2000, step=1)
    end_year = st.sidebar.number_input('Ano Final', min_value=ANO_INICIAL, max_value=ANO_FINAL, value=2024, step=1)
    
    if start_year > end_year:
        st.sidebar.error('O ano inicial deve ser menor ou igual ao ano final.')
        return
    
    df_map, df_top5 = get_data_from_db(start_year, end_year)
    if df_map.empty:
        st.warning('Nenhum dado encontrado para o intervalo de anos selecionado.')
        return
    
    # Exibir tabela e gráfico lado a lado
    col1, col2 = st.columns([3, 5])
    
    with col1:
        st.subheader(f'Exportação de espumantes ({start_year} a {end_year})')
        st.write(df_map)

    with col2:
        st.subheader('Top 5 Países com Maiores Valores Exportados')
        buf = plot_bar_chart(df_top5)
        st.image(buf, use_column_width=True)

    st.subheader('Mapa Interativo')
    if not df_map.empty:
        st.map(df_map[['latitude', 'longitude']])

# Verificar se o usuário está logado
if 'token' in st.session_state:
    user = verify_token(st.session_state['token'])
    if user:
        dashboard()
    else:
        st.error('Sessão expirada. Por favor, faça login novamente.')
        login_screen()
else:
    login_screen()
