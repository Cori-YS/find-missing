import requests
import streamlit as st
from st_pages import hide_pages
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="Listar Desaparecidos",
    initial_sidebar_state="expanded"
)
hide_pages(['Login', 'Register'])

token = ''
try:
    token = st.session_state['token']
except:
    switch_page('Login')

st.title("Lista de Pessoas Desaparecidas")

items_per_page = 5

api_url = 'http://localhost:5000/missing/'
body = {
   'token': token,
}


search = st.text_input("Procure por bilhete de identidade")
if st.button("Procurar"):
    body["search"] = search

page = st.number_input('Page', min_value=1, value=1)
body["page"] = page

response = requests.get(api_url, json=body)
persons = response.json()['persons']
count = response.json()['count']

total_pages = count // items_per_page + (1 if count % items_per_page > 0 else 0)

for person in persons:
    with st.expander(person['Nome']):
        url = "http://127.0.0.1:5000"+person['image_path']
        del person["image_path"]
        col1, col2 = st.columns([0.7,0.3])
        with col1:
            st.write(person)
        with col2:
            st.image(url, caption=person["Nome"], use_column_width=True)
        if st.button("Marcar como resolvido", key=person['ID'], use_container_width=True):
            response = requests.post(api_url+"solved", json={"token": token, "person_id": person['ID']})
            st.rerun()

st.write(f"Page {page} of {total_pages}")