import streamlit as st
import os
from st_pages import hide_pages
from streamlit_extras.switch_page_button import switch_page
from utilities.functions import stop_process, is_process_running, start_script, list_available_cameras


st.set_page_config(
    page_title="Centro de Vigilância",
    initial_sidebar_state="expanded"
)
hide_pages(['Login', 'Register'])

token = ''
try:
    token = st.session_state['token']
except:
    switch_page('Login')

st.title("Centro de Vigilância Morro Bento")


file_path = 'app/resources/files/cameras.txt'

if not os.path.exists(file_path):
    c = list_available_cameras()
    with open(file_path, 'a') as f:
        [f.write(camera) for camera in c]

# Lista de argumentos para os scripts
#cameras = list_available_cameras()
cameras_file = open(file_path, 'r')

for camera in cameras_file:
    container = st.container(border=True)
    show_cam = False
    status = is_process_running(camera)
    if not status:
        status = is_process_running(camera, "show")
        show_cam = True
    col1, col2 = container.columns(2)
    with col1:
        container.write("Camera: " + camera)
    with col2: 
        s = "Online" if status else "Offline"
        container.write("Status: " + s)
    if not status:
        if container.button("Ativar", key=camera, use_container_width=True):
            start_script(camera)
            st.rerun()
        if container.button("Ativar mostrando a camera", key=camera+camera, use_container_width=True):
            start_script(camera, "show")
            st.rerun()
    else:
        if container.button("Desativar", key=camera, use_container_width=True):
            if not show_cam:
                stop_process(camera)
            else:
                stop_process(camera, "show")
            st.rerun()
        
cameras_file.close()