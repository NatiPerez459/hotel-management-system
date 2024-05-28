import streamlit as st
import requests
import pandas as pd

st.session_state.testing = False

if not st.session_state.testing:
    from frontend.utils import *
else:
    from utils import *
    
updateURL()

st.set_page_config(page_title="Create Record")
check_illegal_url_jump()
displayHomeNavBar()
    
st.title(":green[Create Record] ➕")

entity = st.selectbox('Select entity to create:',
            options = ['Login', 'Employee', 'Hotel', 'Chains', 'Room Description', 'Client', 'Room', 'Room Unavailable', 'Reserve'],
            index = None,
            placeholder = "Select entity...")

create_format = {
    'Login': ['eid', 'username', 'password'],
    'Employee': ['hid', 'fname', 'lname', 'age', 'position', 'salary'],
    'Hotel': ['chid', 'hname', 'hcity'],
    'Chains': ['cname', 'springmkup', 'summermkup', 'fallmkup', 'wintermkup'],
    'Room Description': ['rname', 'rtype', 'capacity', 'ishandicap'],
    'Room': ['hid', 'rdid', 'rprice'],
    'Room Unavailable': ['rid', 'startdate', 'enddate'],
    'Client': ['fname', 'lname', 'age', 'memberyear'],
    'Reserve': ['ruid', 'clid', 'total_cost', 'payment', 'guests']
}

int_fields = {'age', 'memberyear', 'guests'}
float_fields = {'springmkup', 'summermkup', 'fallmkup', 'wintermkup', 'salary', 'rprice', 'total_cost'}
date_fields = {'startdate', 'enddate'}
reference_fields = {'eid', 'hid', 'chid', 'rdid', 'rid', 'ruid', 'clid', 'reid'}


if entity:
    table_name = entity.lower().replace(' ', '')

    st.session_state.new_record = {}

    if entity == 'Room Description':
        st.session_state.new_record['rname'] = st.selectbox('rname', options=getAllValidRoomNames(), placeholder='Select room name...')
        changeValidRoomSpecs()

    with st.form('Data Form', border=False):
        for section in create_format[entity]:
            if section == 'rname': continue

            if section in reference_fields:
                ids = showReferences(section)
                st.session_state.new_record[section] = st.selectbox(section, index = None, options=ids, placeholder=f'Select linked {section}...')

            elif section in int_fields:
                st.session_state.new_record[section] = st.number_input(section, value=0, format='%d')

            elif section in float_fields:
                st.session_state.new_record[section] = st.number_input(section, value=0.0, format='%.2f')

            elif section in date_fields:
                st.session_state.new_record[section] = st.date_input(section, format='YYYY-MM-DD').strftime("%Y-%m-%d")

            elif section == 'ishandicap':
                st.session_state.new_record[section] = st.selectbox(section, index = None, options=['true', 'false'], placeholder='true/false')

            elif section == 'position':
                st.session_state.new_record[section] = st.selectbox(section, index = None, options=['Regular', 'Supervisor', 'Administrator'], placeholder='Select Position...')

            elif section == 'rtype':
                st.session_state.new_record[section] = st.selectbox(section, index = None, options=st.session_state.get('rname_types', []), placeholder='Select room type... (Choose rname first)')

            elif section == 'capacity':
                st.session_state.new_record[section] = st.selectbox(section, index = None, options=st.session_state.get('rname_caps', []), placeholder='Select room capacity... (Choose rname first)')

            elif section == 'payment':
                st.session_state.new_record[section] = st.selectbox(section, index = None, options=['cash', 'check', 'credit card', 'debit card','pear pay'], placeholder='Select Payment Method...')
            
            elif section == 'password':
                st.session_state.new_record[section] = st.text_input(section, placeholder='Enter text here', type='password')
            
            else:
                st.session_state.new_record[section] = st.text_input(section, placeholder='Enter text here')

        submit = st.form_submit_button('Create')

    if submit:
        response = requests.post(f'{st.session_state.URL}/datafr3aks/{table_name}', json=st.session_state.new_record)

        if response.ok:
            created_record = response.json()
            df = pd.DataFrame([created_record])

            st.write(f"Created Record for {table_name} table:")
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.error(response.json())

    