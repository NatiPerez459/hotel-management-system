import streamlit as st
import os
import requests
import pandas as pd

st.session_state.testing = False

if not st.session_state.testing:
    from frontend.utils import *
else:
    from utils import *
    
updateURL()

st.set_page_config(page_title="Data Tables")
check_illegal_url_jump()
displayHomeNavBar()
    
st.title(":green[DataFr3aks Database] 🗂️")
st.caption("Members: Natalia, Nicole, Jeremy, Diego")

st.subheader('Description'.title())
st.write(getDescription('data tables'))

if 'eid' not in st.session_state:
    st.session_state.eid = None

eid = st.session_state.eid

if eid:
    entity = st.selectbox('Select entity to view:',
            options = ['Login', 'Employee', 'Hotel', 'Chains', 'Room Description', 'Client', 'Room', 'Room Unavailable', 'Reserve'],
            index = None,
            placeholder = "Select entity...")

    response = None

    if entity == 'Login':
        st.subheader("Login Data")
        response = requests.get(f"{st.session_state.URL}/datafr3aks/login")
            
    elif entity == 'Employee':
        st.subheader("Employee Data")
        response = requests.get(f"{st.session_state.URL}/datafr3aks/employee")
            
    elif entity == 'Hotel':
        st.subheader("Hotel Data")
        response = requests.get(f"{st.session_state.URL}/datafr3aks/hotel")
            
    elif entity == 'Chains':
        st.subheader("Chains Data")
        response = requests.get(f"{st.session_state.URL}/datafr3aks/chains")
            
    elif entity == 'Room Description':
        st.subheader("Room Description Data")
        response = requests.get(f"{st.session_state.URL}/datafr3aks/roomdescription")
            
    elif entity == 'Client':
        st.subheader("Client Data")
        response = requests.get(f"{st.session_state.URL}/datafr3aks/client")
            
    elif entity == 'Room':
        st.subheader("Room Data")
        response = requests.get(f"{st.session_state.URL}/datafr3aks/room")
            
    elif entity == 'Room Unavailable':
        st.subheader("Room Unavailable Data")
        response = requests.get(f"{st.session_state.URL}/datafr3aks/roomunavailable")
            
    elif entity == 'Reserve':
        st.subheader("Reserve Data")
        response = requests.get(f"{st.session_state.URL}/datafr3aks/reserve")
    
    if response:     
        if response.ok:
                data = response.json()
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.error(response.json())
else:
    st.switch_page('pages/signup.py')