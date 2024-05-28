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

st.set_page_config(page_title="Login")
displayLoginNavBar()
st.session_state.eid = None

st.title(":green[DataFr3aks Database] :fire:")
st.caption("Members: Natalia, Nicole, Jeremy, Diego")
st.subheader("Sign Up")

with st.form("sign up"):
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    age = st.text_input("Age")
    position = st.selectbox(
        'Select position:',
        options = ['Regular', 'Administrator', 'Supervisor'],
        index = None,
        placeholder = "Select position...")
    salary = st.text_input("Salary")
    hotels = requests.get(f"{st.session_state.URL}/datafr3aks/hotel").json()
    hotels = [hotel['hid'] for hotel in hotels]
    hotel = st.selectbox(
        'Select hotel:',
        options = hotels,
        index = None,
        placeholder = "Hotel Id"
    )
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button('Sign Up')
    
if submit:
    try:
        hotel = int(hotel)
    except:
        pass
        
    try:
        age = int(age)
    except:
        pass
        
    try:
        salary = float(salary)
    except:
        pass
    
    employee = {
        'hid': hotel,
        'fname': first_name,
        'lname': last_name,
        'age': age,
        'position': position,
        'salary': salary
    }
    response = requests.post(f"{st.session_state.URL}/datafr3aks/employee", json=employee)
    
    if 'eid' in response.json():
        eid = response.json()['eid']
        
    if response.ok:
        login = {
            'eid': int(eid),
            'username': username,
            'password': password
        }
        response = requests.post(f"{st.session_state.URL}/datafr3aks/login", json=login)
        if response.ok:
            st.session_state.eid = response.json()['eid']
            st.success("Sign Up Successful.")
            st.session_state.username = username
            st.session_state.position = position

            st.session_state.logged_in = True
            st.switch_page("pages/data_tables.py")
        else:
            st.session_state.eid = None
            st.error(response.json())
    else:
        st.error(response.json())