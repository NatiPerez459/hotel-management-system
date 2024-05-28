import streamlit as st
import requests
import pandas as pd

st.session_state.testing = False

if not st.session_state.testing:
    from frontend.utils import *
else:
    from utils import *
    
updateURL()

st.set_page_config(page_title="Restrict Rooom")
check_illegal_url_jump()
displayHomeNavBar()
    
st.title(":blue[Restrict Room] 🔒")

st.session_state.new_record = {}

with st.form('Data Form'):
    st.session_state.new_record['rid'] = st.selectbox('rid',
                                            options = showReferences('rid'),
                                            index = None,
                                            placeholder = "Select room id...")

    st.session_state.new_record['startdate'] = st.date_input('startdate', format='YYYY-MM-DD').strftime("%Y-%m-%d")
    st.session_state.new_record['enddate'] = st.date_input('enddate', format='YYYY-MM-DD').strftime("%Y-%m-%d")

    submit = st.form_submit_button('Complete Restriction')

if submit:
    response = requests.post(f'{st.session_state.URL}/datafr3aks/roomunavailable', json=st.session_state.new_record)

    if response.ok:
        created_record = response.json()
        df = pd.DataFrame([created_record])

        st.write(f"Restricted room time slot:")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.error(response.json())

