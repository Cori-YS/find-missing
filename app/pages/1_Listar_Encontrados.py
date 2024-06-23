import requests
import streamlit as st
from st_pages import hide_pages
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="Listar Encontrados",
    initial_sidebar_state="expanded"
)
hide_pages(['Login', 'Register'])

token = ''
try:
    token = st.session_state['token']
except:
    switch_page('Login')

st.title("Lista de Aparições")

items_per_page = 5

api_url = 'http://localhost:5000/found/'
body = {
   'token': token,
}


search = st.text_input("Procure por bilhete de identidade")
if st.button("Procurar"):
    body["search"] = search

page = st.number_input('Page', min_value=1, value=1)
body["page"] = page

response = requests.get(api_url, json=body)
founds = response.json()['founds']
count = response.json()['count']

total_pages = count // items_per_page + (1 if count % items_per_page > 0 else 0)

for found in founds:
    with st.expander(found["Desaparecido"]['Nome']):
        url = "http://127.0.0.1:5000"+found['Desaparecido']['image_path']
        del found["Desaparecido"]["image_path"]

        col1, col2 = st.columns([0.7,0.3])
        with col1:
            st.write(found)
        with col2:
            st.image(url, caption=found["Desaparecido"]["Nome"], use_column_width=True)

st.write(f"Page {page} of {total_pages}")