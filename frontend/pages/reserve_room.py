import streamlit as st
import requests
import pandas as pd

st.session_state.testing = False

if not st.session_state.testing:
    from frontend.utils import *
else:
    from utils import *
    
updateURL()

st.set_page_config(page_title="Reserve Room")
check_illegal_url_jump()
displayHomeNavBar()
    
st.title(":blue[Reserve Room] 🛏️")

st.session_state.new_record = {}

with st.form('Data Form'):
    st.session_state.new_record['ruid'] = st.selectbox('ruid',
                                            options = showReferences('ruid'),
                                            index = None,
                                            placeholder = "Select room unnavailable id...")
    
    st.session_state.new_record['clid'] = st.selectbox('clid',
                                            options = showReferences('clid'),
                                            index = None,
                                            placeholder = "Select client id...")

    st.session_state.new_record['total_cost'] = st.number_input('total_cost', value=0.0, format='%.2f')
    
    st.session_state.new_record['payment'] = st.selectbox('payment', index = None, options=['cash', 'check', 'credit card', 'debit card','pear pay'], placeholder='Select Payment Method...')

    st.session_state.new_record['guests'] = st.number_input('guests', value=0, format='%d')

    submit = st.form_submit_button('Reserve room')

if submit:
    response = requests.post(f'{st.session_state.URL}/datafr3aks/reserve', json=st.session_state.new_record)

    if response.ok:
        created_record = response.json()
        df = pd.DataFrame([created_record])

        st.write(f"Created reservation:")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.error(response.json())