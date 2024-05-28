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

def getEmployeePosition(eid):
    data = {
        'eid': eid
    }
    response = requests.post(f"{st.session_state.URL}/datafr3aks/employee/position", json=data)
    if response.ok:
        st.session_state.position = response.json()['position']
    else:
        st.session_state.position = None


st.set_page_config(page_title="Login")
displayLoginNavBar()
st.session_state.logged_in = False
st.session_state.eid = None
    
st.title(":green[DataFr3aks Database] :fire:")
st.caption("Members: Natalia, Nicole, Jeremy, Diego")
st.subheader("Login")

with st.form("login"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button('Login')
    
if submit:
    data = {
    'username': username,
    'password': password
    }

    response = requests.post(f"{st.session_state.URL}/datafr3aks/employee/id", json=data)
    if response.ok:
        st.session_state.eid = response.json()['eid']
        st.success("Login Successful.")
        st.session_state.username = username

        getEmployeePosition(st.session_state.eid)

        st.session_state.logged_in = True
        st.switch_page("pages/data_tables.py")

    else:
        st.session_state.eid = None
        st.error("Credentials do not exist.")