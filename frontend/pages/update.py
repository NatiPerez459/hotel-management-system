import streamlit as st
import requests
import pandas as pd

st.session_state.testing = False

if not st.session_state.testing:
    from frontend.utils import *
else:
    from utils import *
    
updateURL()

st.set_page_config(page_title="Update Record")
check_illegal_url_jump()
displayHomeNavBar()
    
st.title(":orange[Update Record] 🔧")

entity = st.selectbox('Select entity to update:',
            options = ['Login', 'Employee', 'Hotel', 'Chains', 'Room Description', 'Client', 'Room', 'Room Unavailable', 'Reserve'],
            index = None,
            placeholder = "Select entity...")

update_format = {
    'Login': ['lid', 'eid', 'username', 'password'], 
    'Employee': ['eid', 'hid', 'fname', 'lname', 'age', 'position', 'salary'],
    'Hotel': ['hid', 'chid', 'hname', 'hcity'], 
    'Chains': ['chid', 'cname', 'springmkup', 'summermkup', 'fallmkup', 'wintermkup'],
    'Room Description': ['rdid', 'rname', 'rtype', 'capacity', 'ishandicap'],
    'Room': ['rid', 'hid', 'rdid', 'rprice'],
    'Room Unavailable': ['ruid', 'rid', 'startdate', 'enddate'],
    'Client': ['clid', 'fname', 'lname', 'age', 'memberyear'],
    'Reserve': ['reid', 'ruid', 'clid', 'total_cost', 'payment', 'guests']
}

int_fields = {'age', 'memberyear', 'guests'}
float_fields = {'springmkup', 'summermkup', 'fallmkup', 'wintermkup', 'salary', 'rprice', 'total_cost'}
date_fields = {'startdate', 'enddate'}
reference_fields = {'eid', 'hid', 'chid', 'rdid', 'rid', 'ruid', 'clid', 'reid'}


if entity:
    table_name = entity.lower().replace(' ', '')

    st.session_state.new_record = {}

    response = requests.get(f"{st.session_state.URL}/datafr3aks/{table_name}")

    if response.ok:
        ids = [data[update_format[entity][0]] for data in response.json()]

    id = st.selectbox(f'{entity} id to update:',
        options = ids,
        index = None,
        placeholder = "Select id...")
    
    if entity == 'Room Description':
        st.session_state.new_record['rname'] = st.selectbox('rname', options=getAllValidRoomNames(), placeholder='Select room name...')
        changeValidRoomSpecs()

    with st.form('Data Form', border=False):
        for section in update_format[entity][1:]:
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

        submit = st.form_submit_button('Update')

    if submit:
        st.write('id to update:', id)
        st.write('data:', st.session_state.new_record)
        response = requests.put(f'{st.session_state.URL}/datafr3aks/{table_name}/{id}', json=st.session_state.new_record)

        if response.ok:
            updated_record = response.json()
            df = pd.DataFrame([updated_record])

            st.write(f"Updated Record for {table_name} table | {update_format[entity]} = {id}:")
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.error(response.json())

    