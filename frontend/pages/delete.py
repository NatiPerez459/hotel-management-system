import streamlit as st
import requests
import time

st.session_state.testing = False

if not st.session_state.testing:
    from frontend.utils import *
else:
    from utils import *
    
updateURL()

st.set_page_config(page_title="Delete Record")
check_illegal_url_jump()
displayHomeNavBar()
    
st.title(":red[Delete Record] 🗑️")

entity = st.selectbox('Select entity to delete:',
            options = ['Login', 'Employee', 'Hotel', 'Chains', 'Room Description', 'Client', 'Room', 'Room Unavailable', 'Reserve'],
            index = None,
            placeholder = "Select entity...")

st.session_state.delete_record = None

if entity:
    table_name = entity.lower().replace(' ', '')
    
    if entity == 'Login':
        id_name = 'lid'
        
    elif entity == 'Employee':
        id_name = 'eid'
        
    elif entity == 'Hotel':
        id_name = 'hid'
        
    elif entity == 'Chains':
        id_name = 'chid'
        
    elif entity == 'Room Description':
        id_name = 'rdid'
        
    elif entity == 'Client':
        id_name = 'clid'
        
    elif entity == 'Room':
        id_name = 'rid'
        
    elif entity == 'Room Unavailable':
        id_name = 'ruid'
        
    elif entity == 'Reserve':
        id_name = 'reid'
    
    ids = showReferences(id_name)
    id = st.selectbox(id_name, index = None, options=ids, placeholder=f'Select linked ' + id_name + '...')
    
    del_button = st.button('Delete')
    
    curr_account = False
    
    if del_button:
        if id:
            data = { id_name : id }
            
            if id_name == 'lid':
                response = requests.get(f"{st.session_state.URL}/datafr3aks/" + table_name + "/" + str(id), json=data).json()
                if response['username'] == st.session_state.username:
                    curr_account = True
            elif id_name == 'eid' and id == st.session_state.eid['eid']:
                curr_account = True
                
            response = requests.delete(f"{st.session_state.URL}/datafr3aks/" + table_name + "/" + str(id), json=data)
            
            if response.ok:
                if curr_account:
                    st.success(response.json())
                    time.sleep(0.5)
                    st.session_state.logged_in = False
                    st.session_state.eid = None
                    st.switch_page("pages/login.py")
                else:
                    st.success(response.json())
                    time.sleep(0.5)
                    st.switch_page("pages/delete.py")
            else:
                st.error(response.json())
        else:
            st.error("Select an entity id to delete.")