import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.session_state.testing = False

if not st.session_state.testing:
    from frontend.utils import *
else:
    from utils import *
    
updateURL()

st.set_page_config(page_title="Local Statistics")
check_illegal_url_jump()
displayHomeNavBar()
    
st.title(":green[Local Statistics] 🗺")

if 'eid' not in st.session_state:
    st.session_state.eid = None

data = {
    'eid':st.session_state.eid
}

hotels = requests.post(f"{st.session_state.URL}/datafr3aks/employee/hotels", json=data).json()
hotels = [hotel[0] for hotel in hotels]

if st.session_state.eid:
    hotel = st.selectbox(
        'Select hotel:',
        options = hotels,
        index = None,
        placeholder = "Hotel Id"
    )

    statistic = st.selectbox('Select statistic to view:',
        options = ['Handicap Room', 'Least Reserved', 'Most Credit Card', 'Highest Paid', 'Most Discount', 'Room Type', 'Least Guests'],
        index = 0,
        placeholder = "Select local statistic...")
    
    st.write(getDescription(statistic.lower()))
    
    if hotel: 
        if statistic == 'Handicap Room':
            st.subheader("Handicap Room Statistics")
            response = requests.post(f"{st.session_state.URL}/datafr3aks/hotel/" + str(hotel) + "/handicaproom", json=data)
            x='rid'
            y='total_reservations'
            title='Handicap Rooms Reserved Most'
            x_axis = 'Room Id'
            y_axis = 'Total Reservations'
                
        elif statistic == 'Least Reserved':
            st.subheader("Least Reserved Statistics")
            response = requests.post(f"{st.session_state.URL}/datafr3aks/hotel/" + str(hotel) + "/leastreserve", json=data)
            x='rid'
            y='total_days'
            title='Least Reserved Rooms'
            x_axis = 'Room Id'
            y_axis = 'Total Days'
        
        elif statistic == 'Most Credit Card':
            st.subheader("Most Credit Card Statistics")
            response = requests.post(f"{st.session_state.URL}/datafr3aks/hotel/" + str(hotel) + "/mostcreditcard", json=data)
            x='clid'
            y='reservations'
            title='Most Reservations Made with Credit Card'
            x_axis = 'Client Id'
            y_axis = 'Reservations'
                
        elif statistic == 'Highest Paid':
            st.subheader("Highest Paid Statistics")
            response = requests.post(f"{st.session_state.URL}/datafr3aks/hotel/" + str(hotel) + "/highestpaid", json=data)
            x='eid'
            y='salary'
            title='Top 3 Highest Paid Employees'
            x_axis = 'Employee Id'
            y_axis = 'Salary'
                
        elif statistic == 'Most Discount':
            st.subheader("Most Discount Statistics")
            response = requests.post(f"{st.session_state.URL}/datafr3aks/hotel/" + str(hotel) + "/mostdiscount", json=data)
            x='clid'
            y='total_discount'
            title='Top Clients by Discounts Received'
            x_axis = 'Client Id'
            y_axis = 'Total Discount'
                
        elif statistic == 'Room Type':
            st.subheader("Room Type Statistics")
            response = requests.post(f"{st.session_state.URL}/datafr3aks/hotel/" + str(hotel) + "/roomtype", json=data)
            x='rtype'
            y='total_reservations'
            title='Total Reservations by Room Type'
            x_axis = 'Room Type'
            y_axis = 'Reservations'
                
        elif statistic == 'Least Guests':
            st.subheader("Least Guests Statistics")
            response = requests.post(f"{st.session_state.URL}/datafr3aks/hotel/" + str(hotel) + "/leastguests", json=data)
            x='rid'
            y='guest_to_capacity_ratio'
            title='Rooms with Least Guest-to-Capacity Ratio'
            x_axis = 'Room Id'
            y_axis = 'Guest-Capacity Ratio'

        if response.ok:
            data = response.json()
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.subheader(title + " Graph")
            fig = px.histogram(response.json(), x=x, y=y, title=None, orientation='v', color=x)
            fig.update_xaxes(type='category', title=x_axis)
            fig.update_yaxes(title=y_axis)
            fig.update_layout(margin=dict(l=10, r=10, t=0, b=10), showlegend=False)
            st.plotly_chart(fig)
        else:
            st.error(response.json())
else:
    st.switch_page('pages/signup.py')