import streamlit as st
from auth import tela_login
from dashboard import painel_dashboard
from auth import verificar_token

# Verificar se o usuário está logado
if 'token' in st.session_state:
    usuario = verificar_token(st.session_state['token'])
    if usuario:
        painel_dashboard()
    else:
        st.session_state['logado'] = False
        tela_login()
else:
    tela_login()

