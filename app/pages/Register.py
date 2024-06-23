import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import requests

st.set_page_config(
    page_title="Cadastro",
    initial_sidebar_state="collapsed"
)
st.markdown( """ <style> [data-testid="collapsedControl"] { display: none } </style> """, unsafe_allow_html=True, )

st.title("Cadastro")

# Create input fields for registration
email = st.text_input("Email")
username = st.text_input("Username")
password = st.text_input("Password", type="password")
confirm_password = st.text_input("Confirmar Password", type="password")

# Create two columns for the buttons
col1, col2 = st.columns([0.19,1])

with col1:
    # Create a register button
    if st.button("Cadastrar"):
        if password == confirm_password:
            api_url = 'http://localhost:5000/user/register'
            data = {
                'email': email,
                'password': password,
                'username': username,
            }
            # Enviar solicitação POST para a API
            response = requests.post(api_url, json=data)
            st.write(response)
            switch_page('Login')
        else:
            st.error("Passwords não combinam.")
with col2:
    # Create a register button
    if st.button("Entrar"):
        switch_page('Login')
