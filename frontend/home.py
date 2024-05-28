import streamlit as st
import os
import requests
import pandas as pd

st.session_state.URL = None
st.session_state.testing = False

if not st.session_state.testing:
    from frontend.utils import *
else:
    from utils import *

updateURL()
    
st.set_page_config(page_title="Login")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    displayHomeNavBar()
else:
    displayLoginNavBar()
    
st.title(":green[DataFr3aks CIIC4060 Final Phase] 🤖")
st.caption("Members: Natalia, Nicole, Jeremy, Diego")

st.subheader("Role: Regular")
st.write(getDescription('reg info'))

st.subheader("Role: Supervisor")
st.write(getDescription('super info'))

st.subheader("Role: Administrator")
st.write(getDescription('admin info'))




    
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8501))