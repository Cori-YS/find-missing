import requests
import streamlit as st
from st_pages import hide_pages
from streamlit_extras.switch_page_button import switch_page
import datetime


st.set_page_config(
    page_title="Registar Desaparecidos",
    initial_sidebar_state="expanded"
)
hide_pages(['Login', 'Register'])

token = ''
try:
    token = st.session_state['token']
except:
    switch_page('Login')

st.title("Formulario de Registro de Pessoas Desaparecidas")

# Campo de nome
name = st.text_input("Nome")

# Campo de data de nascimento
birthday = st.date_input("Data de Nascimento", min_value=datetime.date(1900,1,1))

# Campo de BI (com checagem de unicidade)
bi = st.text_input("BI", help="Deve ser único")

# Campo de contato familiar
family_contact = st.text_input("Contato Familiar")

# Campo de data (padrão é a data e hora atual)
date = st.date_input("Data")

# Campo de upload de imagem
image = st.file_uploader("Upload de Imagem", type=["png", "jpg", "jpeg"])

# Botão de submissão
if st.button("Registrar", use_container_width=True):
    if not name or not bi or not family_contact or image is None:
        st.error("Por favor, preencha todos os campos obrigatórios e faça o upload de uma imagem.")
    else:
        # Dados do formulário
        data = {
            "name": name,
            "birthday": birthday.strftime("%Y-%m-%d"),
            "bi": bi,
            "family_contact": family_contact,
            "date": date
        }
        
        # Arquivo de imagem
        files = {"image": image.getvalue()}
        try:
            # Enviar dados para o servidor
            response = requests.post("http://127.0.0.1:5000/missing/", data=data, files=files)
            
            if response.status_code == 200:
                result = response.json()
                st.success("Registro realizado com sucesso!")
                st.write("**Nome:**", name)
                st.write("**Data de Nascimento:**", birthday)
                st.write("**BI:**", bi)
                st.write("**Contato Familiar:**", family_contact)
                st.write("**Data de Desaparecimento:**", date)
                st.write("**Caminho da Imagem:**", result['data']['image_path'])
                st.image(image, caption="Imagem do Usuário", use_column_width=True)
            else:
                st.error(f"Erro ao registrar: {response.status_code}")
        except Exception as e:
            st.error(f"Erro ao enviar requisição: {e}")