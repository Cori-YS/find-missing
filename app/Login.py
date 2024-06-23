import streamlit as st
import requests
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="Login",
    initial_sidebar_state="collapsed"
)
st.markdown( """ <style> [data-testid="collapsedControl"] { display: none } </style> """, unsafe_allow_html=True, )

st.title("Entrar")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

# Create two columns for the buttons
col1, col2 = st.columns([0.12,1])

with col1:
    if st.button("Entrar"):
        api_url = 'http://localhost:5000/user/login'
        data = {
           'password': password,
           'username': username,
        }
        # Enviar solicitação POST para a API
        response = requests.post(api_url, json=data)
        token = response.json()['token']
        if len(token) == 1:
            st.error("Username ou password errados.")
        else:
            st.session_state["token"] = token
            switch_page('Listar_Encontrados')

with col2:
    if st.button("Cadastrar"):
        switch_page('Register')


    
