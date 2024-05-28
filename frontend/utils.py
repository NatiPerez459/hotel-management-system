import streamlit as st
import requests

LOCAL_API_URL = "http://127.0.0.1:5000"
HEROKU_API_URL = "https://hotel-analytical-system-e6a256acfaf3.herokuapp.com/"

def updateURL():
    if st.session_state.testing:
        st.session_state.URL = LOCAL_API_URL
    else:
        st.session_state.URL = HEROKU_API_URL

def displayLoginNavBar():
    st.markdown("<style>[data-testid='stSidebarNav'] {display: none;} </style>", unsafe_allow_html=True)

    st.sidebar.page_link("home.py", label="Home", icon="🏠")
    st.sidebar.page_link("pages/login.py", label="Login", icon="🔑")
    st.sidebar.page_link("pages/signup.py", label="Sign Up", icon="📝")

def displayHomeNavBar():
    st.markdown("<style>[data-testid='stSidebarNav'] {display: none;} </style>", unsafe_allow_html=True)
    st.markdown("<style>.modebar {display: none;} </style>", unsafe_allow_html=True)
    st.markdown("<style>[data-testid='StyledFullScreenButton'] {display: none;} </style>", unsafe_allow_html=True)

    st.sidebar.markdown(f"**👤User:** {st.session_state.username}")
    st.sidebar.markdown(f"**🛠 Role:** {st.session_state.position}")
    
    st.sidebar.markdown("---")

    role = st.session_state.position

    st.sidebar.page_link("home.py", label="Home", icon="🏠")
    st.sidebar.page_link("pages/data_tables.py", label="Data Tables", icon="🗂️")
    st.sidebar.page_link("pages/local-statistics.py", label="Local Statistics", icon="🗺")
        
    if role == 'Regular':
        st.sidebar.page_link("pages/reserve_room.py", label="Reserve Room", icon="🛏️")  

    elif role == 'Supervisor':
        st.sidebar.page_link("pages/restrict_room.py", label="Restrict Room", icon="🔒")  
        st.sidebar.page_link("pages/reserve_room.py", label="Reserve Room", icon="🛏️") 

    elif role == 'Administrator':
        st.sidebar.page_link("pages/global-statistics.py", label="Global Statistics", icon="🌍")
        st.sidebar.page_link("pages/create_record.py", label="Create Record", icon="➕")  
        st.sidebar.page_link("pages/update.py", label="Update Record", icon="🔧")  
        st.sidebar.page_link("pages/delete.py", label="Delete Record", icon="🗑️")  

    else:
        st.error('User Role not Valid', icon="🚨")
        st.switch_page("pages/login.py")

    st.sidebar.page_link("pages/login.py", label="Logout", icon="❌")

def check_illegal_url_jump():
    if 'logged_in' not in st.session_state:
        st.switch_page('home.py')
    if not st.session_state.logged_in:
        st.switch_page('home.py')

def showReferences(reference):
    ref_to_primary = {
        'eid': 'employee', 
        'hid': 'hotel', 
        'chid': 'chains', 
        'rdid': 'roomdescription', 
        'rid': 'room', 
        'ruid': 'roomunavailable', 
        'clid': 'client', 
        'reid': 'reserve',
        'lid': 'login'
    }

    response = requests.get(f"{st.session_state.URL}/datafr3aks/{ref_to_primary[reference]}")

    if response.ok:
        ids = [data[reference] for data in response.json()]

    return ids

valid_types = {
    'Standard': ['Basic', 'Premium'],
    'Standard Queen': ['Basic', 'Premium', 'Deluxe'],
    'Standard King': ['Basic', 'Premium', 'Deluxe'],
    'Double Queen': ['Basic', 'Premium', 'Deluxe'],
    'Double King': ['Premium', 'Deluxe', 'Suite'],
    'Triple King': ['Deluxe', 'Suite'],
    'Executive Family': ['Deluxe', 'Suite'],
    'Presidential': ['Suite']
}

valid_capacity = {
    'Standard': [1],
    'Standard Queen': [1, 2],
    'Standard King': [2],
    'Double Queen': [4],
    'Double King': [4, 6],
    'Triple King': [6],
    'Executive Family': [4, 6, 8],
    'Presidential': [4, 6, 8]
}

def getAllValidRoomNames():
    return ['Standard', 'Standard Queen', 'Standard King', 'Double Queen', 'Double King', 'Triple King', 'Executive Family', 'Presidential']

def changeValidRoomSpecs():
    st.session_state.rname_types = valid_types[st.session_state.new_record['rname']]
    st.session_state.rname_caps = valid_capacity[st.session_state.new_record['rname']]

def getDescription(title):
    descriptions = {
        'reg info': "Regular employees have access to make reservations for clients and can view local statistics specific to their hotel. They do not have access to modify records or view global statistics.",
        'super info': "Supervisors can make a room unavailable when it is not reserved and view local statistics across all hotels within the same chain. They can also create records for room unavailability.",
        'admin info': "Administrators have the capability to create, update, and delete any records in the database. They have access to all local and global statistics and can perform any administrative tasks.",
        'data tables': "This section includes the infromation of entities such as Chains, Hotels, Rooms, Employees, Reservations, etc..",
        'handicap room': "Tracks the top 5 handicap-accessible rooms that are reserved the most frequently.",
        'least reserved': "Identifies the top 3 rooms that are least often unavailable.",
        'most credit card': "Lists the top 5 clients under 30 who made the most reservations using a credit card.",
        'highest paid': "Shows the top 3 highest-paid regular employees.",
        'most discount': "Displays the top 5 clients who received the most discounts.",
        'room type': "Summarizes total reservations by room type.",
        'least guests': "Reports on the top 3 rooms that have the least guest-to-capacity ratio.",
        'most revenue': "Details the top 3 chains with the highest total revenue.",
        'payment method': "Breaks down total reservation percentages by payment method.",
        'least rooms': "Identifies the top 3 hotel chains with the least rooms.",
        'most capacity': "Highlights the top 5 hotels with the most client capacity.",
        'most reservations': "Focuses on the top 10% of hotels with the most reservations.",
        'most profit month': "Shows the top 3 months with the most reservations by chain."
    }

    return descriptions.get(title, None)



