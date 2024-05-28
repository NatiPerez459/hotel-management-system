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

st.set_page_config(page_title="Global Statistics")
check_illegal_url_jump()
displayHomeNavBar()
    
st.title(":blue[Global Statistics] :earth_americas:")

statistic = st.selectbox('Select statistic to view:',
        options = ['Most Revenue', 'Payment Method', 'Least Rooms', 'Most Capacity', 'Most Reservations', 'Most Profit Month'],
        index = 0,
        placeholder = "Select global statistic...")

if 'eid' not in st.session_state:
    st.session_state.eid = None


data = {
    'eid':st.session_state.eid
}

if st.session_state.eid: 
    if statistic == 'Most Revenue':
        st.subheader("Most Revenue Statistics")
        st.write(getDescription('most revenue'))
        response = requests.post(f"{st.session_state.URL}/datafr3aks/most/revenue", json=data)
        x='chid'
        y='revenue'
        title='Top 3 Chain Highest Total Revenue'
        x_axis = 'Chain Id'
        y_axis = 'Total Revenue'
            
    elif statistic == 'Payment Method':
        st.subheader("Payment Method Statistics")
        st.write(getDescription('payment method'))
        response = requests.post(f"{st.session_state.URL}/datafr3aks/paymentmethod", json=data)
        x='payment'
        y='percentage'
        title='Total Reservation Percentage by Payment Method'
            
    elif statistic == 'Least Rooms':
        st.subheader("Least Rooms Statistics")
        st.write(getDescription('least rooms'))
        response = requests.post(f"{st.session_state.URL}/datafr3aks/least/rooms", json=data)
        x='cname'
        y='total_rooms'
        title='Top 3 Hotel Chains With Least Rooms'
        x_axis = 'Chain Name'
        y_axis = 'Total Rooms'
            
    elif statistic == 'Most Capacity':
        st.subheader("Most Capacity Statistics")
        st.write(getDescription('most capacity'))
        response = requests.post(f"{st.session_state.URL}/datafr3aks/most/capacity", json=data)
        x='hname'
        y='total_capacity'
        title='Top 5 Hotels With Most Client Capacity'
        x_axis = 'Hotel Name'
        y_axis = 'Total Capacity'
            
    elif statistic == 'Most Reservations':
        st.subheader("Most Reservations Statistics")
        st.write(getDescription('most reservations'))
        response = requests.post(f"{st.session_state.URL}/datafr3aks/most/reservation", json=data)
        x='hid'
        y='reservations'
        title='Top 10% Hotels With Most Reservations'
        x_axis = 'Hotel Id'
        y_axis = 'Reservations'
            
    elif statistic == 'Most Profit Month':
        st.subheader("Most Profit Month Statistics")
        st.write(getDescription('most profit month'))
        response = requests.post(f"{st.session_state.URL}/datafr3aks/most/profitmonth", json=data)
        title='Top 3 Month With Most Reservation By Chain'
    
    if response.ok:
        data = response.json()
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.subheader(title + " Graph")
        if statistic == 'Payment Method':
            fig = px.pie(response.json(), names=x, values=y, title=None)
            st.plotly_chart(fig)
        elif statistic == 'Most Profit Month':
            chain_data = { }
            reservations = []
            months = []
            chid = None
            for data_row in data:
                if chid == None:
                    chid = data_row['chid']
                elif chid != data_row['chid']:
                    chain_data[chid].append(months)
                    chain_data[chid].append(reservations)
                    reservations = []
                    months = []
                    chid = data_row['chid']
                if data_row['chid'] not in chain_data.keys():
                    reservations = []
                    months = []
                    chain_data[data_row['chid']] = []
                    months.append(data_row['month'])
                    reservations.append(data_row['reservations'])
                else:
                    months.append(data_row['month'])
                    reservations.append(data_row['reservations'])
            chain_data[chid].append(months)
            chain_data[chid].append(reservations)
            
            for graph_data in chain_data:
                chain_pd = pd.DataFrame(chain_data[graph_data]).transpose()
                chain_pd.columns = ['months', 'reservations']
                fig = px.histogram(chain_pd, x='months', y='reservations', title=("Chain Id: " + str(graph_data)), orientation='v', color='months')
                fig.update_xaxes(type='category', title="Months")
                fig.update_yaxes(title="Reservations")
                fig.update_layout(margin=dict(l=10, r=10, t=40, b=10), showlegend=False)
                st.plotly_chart(fig)
        else:
            fig = px.histogram(response.json(), x=x, y=y, title=None, orientation='v', color=x)
            fig.update_xaxes(type='category', title=x_axis)
            fig.update_yaxes(title=y_axis)
            fig.update_layout(margin=dict(l=10, r=10, t=0, b=10), showlegend=False)
            st.plotly_chart(fig)
    else:
        st.error(response.json())      
else:
    st.switch_page('pages/signup.py')