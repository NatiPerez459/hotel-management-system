from flask import Flask, request, jsonify
import os
from backend.controller.room import RoomController
from backend.controller.roomdescription import RoomDescriptionController
from backend.controller.roomunavailable import RoomUnavailableController
from backend.controller.login import LoginController
from backend.controller.client import ClientController
from backend.controller.reserve import ReservationController
from backend.controller.chains import ChainController
from backend.controller.hotel import HotelController
from backend.controller.employee import EmployeeController
from backend.controller.globalstatistics import GlobalStatisticsController
from backend.controller.localstatistics import LocalStatisticsController
from flask_cors import CORS
import subprocess
import requests


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    #TESTING ONLY#####################
    #global streamlit_ui
    # DO NOT DELETE FOR NATIS MENTAL SANITY :)
    #streamlit_ui = subprocess.Popen(['streamlit', 'run', 'C:/Users/Natalia Roldan/Documents/GitHub/hotel-analytical-system-datafr3aks/hotel-analytical-system-datafr3aks/frontend/frontend.py'])
    ##################################
    return "Hello Datafr3aks!"

#### Room ROUTES ####

@app.route('/datafr3aks/room', methods = ['GET', 'POST'])
def handleRooms():
    if request.method == 'POST':
        try:
            return RoomController().addNewRoom(request.json)
        except:
            return jsonify("Incomplete data in json."), 404
    elif request.method == 'GET':
        return RoomController().getAllRooms()
    else:
        return jsonify("Method Not Allowed"), 405
    
@app.route('/datafr3aks/room/<rid>', methods = ['GET', 'PUT', 'DELETE'])
def handleRoomsById(rid):
    try:
        rid = int(rid)
    except ValueError:
        return jsonify("Room ID not an integer."), 400

    if request.method == 'GET':
        return RoomController().getRoomById(rid)
    elif request.method == 'PUT':
        try:
            return RoomController().updateRoom(rid, request.json)
        except:
            return jsonify("Incomplete data in json."), 404
    elif request.method == 'DELETE':
        return RoomController().deleteRoom(rid)
    else:
        return jsonify("Method Not Allowed"), 405
    
#### RoomDescription ROUTES ####
    
@app.route('/datafr3aks/roomdescription', methods = ['GET', 'POST'])
def handleRoomDescriptions():
    if request.method == 'POST':
        try:
            return RoomDescriptionController().addNewRoomDescription(request.json)
        except:
            return jsonify("Incomplete data in json."), 404
    elif request.method == 'GET':
        return RoomDescriptionController().getAllRoomDescriptions()
    else:
        return jsonify("Method Not Allowed"), 405
    
@app.route('/datafr3aks/roomdescription/<rdid>', methods = ['GET', 'PUT', 'DELETE'])
def handleRoomDescriptionsById(rdid):
    try:
        rdid = int(rdid)
    except ValueError:
        return jsonify("RoomDescription ID not an integer."), 400

    if request.method == 'GET':
        return RoomDescriptionController().getRoomDescriptionById(rdid)
    elif request.method == 'PUT':
        try:
            return RoomDescriptionController().updateRoomDescription(rdid, request.json)
        except:
            return jsonify("Incomplete data in json."), 404
    elif request.method == 'DELETE':
        return RoomDescriptionController().deleteRoomDescription(rdid)
    else:
        return jsonify("Method Not Allowed"), 405
    
#### RoomUnavailable ROUTES ####
    
@app.route('/datafr3aks/roomunavailable', methods = ['GET', 'POST'])
def handleRoomUnavailable():
    if request.method == 'POST':
        try:
            return RoomUnavailableController().addNewRoomUnavailable(request.json)
        except:
            return jsonify("Incomplete data in json."), 404
    elif request.method == 'GET':
        return RoomUnavailableController().getAllRoomUnavailable()
    else:
        return jsonify("Method Not Allowed"), 405
    
@app.route('/datafr3aks/roomunavailable/<ruid>', methods = ['GET', 'PUT', 'DELETE'])
def handleRoomUnavailableById(ruid):
    try:
        ruid = int(ruid)
    except ValueError:
        return jsonify("RoomUnavailable ID not an integer."), 400

    if request.method == 'GET':
        return RoomUnavailableController().getRoomUnavailableById(ruid)
    elif request.method == 'PUT':
        try:
            return RoomUnavailableController().updateRoomUnavailable(ruid, request.json)
        except:
            return jsonify("Incomplete data in json."), 404
    elif request.method == 'DELETE':
        return RoomUnavailableController().deleteRoomUnavailable(ruid)
    else:
        return jsonify("Method Not Allowed"), 405
    
#### Login ROUTES ####
    
@app.route('/datafr3aks/login', methods = ['GET', 'POST'])
def handleLogin():
    if request.method == 'POST':
        try:
            return LoginController().addNewLogin(request.json)
        except:
            return jsonify("Incomplete data in json."), 404
    elif request.method == 'GET':
        return LoginController().getAllLogin()
    else:
        return jsonify("Method Not Allowed"), 405
    
@app.route('/datafr3aks/login/<lid>', methods = ['GET', 'PUT', 'DELETE'])
def handleLoginById(lid):
    try:
        lid = int(lid)
    except ValueError:
        return jsonify("Login ID not an integer."), 400

    if request.method == 'GET':
        return LoginController().getLoginById(lid)
    elif request.method == 'PUT':
        try:
            return LoginController().updateLogin(lid, request.json)
        except:
            return jsonify("Incomplete data in json."), 404
    elif request.method == 'DELETE':
        return LoginController().deleteLogin(lid)
    else:
        return jsonify("Method Not Allowed"), 405
    
#### Chains ROUTES ####

@app.route('/datafr3aks/chains', methods = ['GET', 'POST'])
def handleChains():
    if request.method == 'POST':
        try:
            return ChainController().addNewChain(request.json)
        except:
            return jsonify("Incomplete data in json."), 404
    elif request.method == 'GET':
        return ChainController().getAllChains()
    else:
        return jsonify("Method Not Allowed"), 405
    
@app.route('/datafr3aks/chains/<chid>', methods = ['GET', 'PUT', 'DELETE'])
def handleChainsbyId(chid):
    try:
        chid = int(chid)
    except ValueError:
        return jsonify("Chains ID not an integer."), 400
    
    if request.method == 'GET':
        return ChainController().getChainById(chid)
    elif request.method == 'PUT':
        try:
            return ChainController().updateChain(chid, request.json)
        except:
            return jsonify("Incomplete data in json."), 404
    elif request.method == 'DELETE':
        return ChainController().deleteChain(chid)
    else:
        return jsonify("Method Not Allowed"), 405
    
#### Client ROUTES ####

@app.route('/datafr3aks/client', methods = ['GET', 'POST'])
def handleClients():
    if request.method == 'POST':
        try:
            return ClientController().addNewClient(request.json)
        except:
            return jsonify("Incomplete data in json."), 404
    elif request.method == 'GET':
        return ClientController().getAllClients()
    else:
        return jsonify("Method Not Allowed"), 405
    
@app.route('/datafr3aks/client/<clid>', methods = ['GET', 'PUT', 'DELETE'])
def handleClientsById(clid):
    try:
        clid = int(clid)
    except ValueError:
        return jsonify("CLient ID not an integer."), 400

    if request.method == 'GET':
        return ClientController().getClientById(clid)
    elif request.method == 'PUT':
        try:
            return ClientController().updateClient(clid, request.json)
        except:
            return jsonify("Incomplete data in json."), 404
    elif request.method == 'DELETE':
        return ClientController().deleteClient(clid)
    else:
        return jsonify("Method Not Allowed"), 405
    
#### Reservation ROUTES ####

@app.route('/datafr3aks/reserve', methods = ['GET', 'POST'])
def handleReservations():
    if request.method == 'POST':
        #try:
            return ReservationController().addNewReservation(request.json)
        #except:
        #    return jsonify("Incomplete data in json."), 404
    elif request.method == 'GET':
        return ReservationController().getAllReservations()
    else:
        return jsonify("Method Not Allowed"), 405
    
@app.route('/datafr3aks/reserve/<reid>', methods = ['GET', 'PUT', 'DELETE'])
def handleReservationsById(reid):
    try:
        reid = int(reid)
    except ValueError:
        return jsonify("Reserve ID not an integer."), 400

    if request.method == 'GET':
        return ReservationController().getReservationById(reid)
    elif request.method == 'PUT':
        try:
            return ReservationController().updateReservation(reid, request.json)
        except:
            return jsonify("Incomplete data in json."), 404
    elif request.method == 'DELETE':
        return ReservationController().deleteReservation(reid)
    else:
        return jsonify("Method Not Allowed"), 405
  
#### Hotel ROUTES ####

@app.route('/datafr3aks/hotel', methods = ['GET', 'POST'])
def handleHotel():
    if request.method == 'POST':
        try:
            return HotelController().addNewHotel(request.json)
        except:
            return jsonify("Incomplete data in json."), 404
    elif request.method == 'GET':
        return HotelController().getAllHotels()
    else:
        return jsonify("Method Not Allowed"), 405
    
@app.route('/datafr3aks/hotel/<hid>', methods = ['GET', 'PUT', 'DELETE'])
def handleHotelById(hid):
    try:
        hid = int(hid)
    except ValueError:
        return jsonify("Hotel ID not an integer."), 400

    if request.method == 'GET':
        return HotelController().getHotelById(hid)
    elif request.method == 'PUT':
        try:
            return HotelController().updateHotel(hid, request.json)
        except:
            return jsonify("Incomplete data in json."), 404
    elif request.method == 'DELETE':
        return HotelController().deleteHotel(hid)
    else:
        return jsonify("Method Not Allowed"), 405
    
#### Employee ROUTES ####

@app.route('/datafr3aks/employee', methods = ['GET', 'POST'])
def handleEmployee():
    if request.method == 'POST':
        try:
            return EmployeeController().addNewEmployee(request.json)
        except:
            return jsonify("Incomplete data in json."), 404
    elif request.method == 'GET':
        return EmployeeController().getAllEmployees()
    else:
        return jsonify("Method Not Allowed"), 405
    
@app.route('/datafr3aks/employee/<eid>', methods = ['GET', 'PUT', 'DELETE'])
def handleEmployeeById(eid):
    try:
        eid = int(eid)
    except ValueError:
        return jsonify("Employee ID not an integer."), 400

    if request.method == 'GET':
        return EmployeeController().getEmployeeById(eid)
    elif request.method == 'PUT':
        try:
            return EmployeeController().updateEmployee(eid, request.json)
        except:
            return jsonify("Incomplete data in json."), 404
    elif request.method == 'DELETE':
        return EmployeeController().deleteEmployee(eid)
    else:
        return jsonify("Method Not Allowed"), 405
  
    
#### Global Statistics ROUTES ####
    
@app.route('/datafr3aks/most/reservation', methods = ['POST'])
def obtainMostReservation():
    if request.method == 'POST':
        try:
            return GlobalStatisticsController().getMostReservations(request.json)
        except:
            return jsonify("Incomplete data in json."), 404
    else:
        return jsonify("Method Not Allowed"), 405
    
@app.route('/datafr3aks/most/profitmonth', methods = ['POST'])
def obtainMostProfitMonth():
    if request.method == 'POST':
        try:
            return GlobalStatisticsController().getMostProfitMoth(request.json)
        except:
            return jsonify("Incomplete data in json."), 404
    else:
        return jsonify("Method Not Allowed"), 405
    
@app.route('/datafr3aks/most/revenue', methods = ['POST'])
def obtainMostRevenue():
    if request.method == 'POST':
        try:
            return GlobalStatisticsController().getMostRevenue(request.json)
        except:
            return jsonify("Incomplete data in json."), 404
    else:
        return jsonify("Method Not Allowed"), 405
    
@app.route('/datafr3aks/paymentmethod', methods = ['POST'])
def obtainPaymentMethod():
    if request.method == 'POST':
        try:
            return GlobalStatisticsController().getPayment(request.json)
        except:
            return jsonify("Incomplete data in json."), 404
    else:
        return jsonify("Method Not Allowed"), 405
    
@app.route('/datafr3aks/least/rooms', methods = ['POST'])
def obtainLeastRooms():
    if request.method == 'POST':
        try:
            return GlobalStatisticsController().getLeastRooms(request.json)
        except:
            return jsonify("Incomplete data in json."), 404
    else:
        return jsonify("Method Not Allowed"), 405

@app.route('/datafr3aks/most/capacity', methods = ['POST'])
def obtainMostCapacity():
    if request.method == 'POST':
        try:
            return GlobalStatisticsController().getMostCapacity(request.json)
        except:
            return jsonify("Incomplete data in json."), 404
    else:
        return jsonify("Method Not Allowed"), 405
    
#### Local Statistics ROUTES ####

@app.route('/datafr3aks/hotel/<int:hid>/handicaproom', methods=['POST'])
def get_top_handicap_rooms(hid):
    if request.method == 'POST':
        try:
            return LocalStatisticsController().get_top_handicap_rooms(hid, request.json)
        except:
            return jsonify("Incomplete data in json."), 404
    else:
        return jsonify("Method Not Allowed"), 405

@app.route('/datafr3aks/hotel/<int:hid>/leastreserve', methods=['POST'])
def get_rooms_least_time_unavailable(hid):
    if request.method == 'POST':
        try:
            return LocalStatisticsController().get_top_rooms_with_least_time_unavailable(hid, request.json)
        except:
            return jsonify("Incomplete data in json."), 404
    else:
        return jsonify("Method Not Allowed"), 405

@app.route('/datafr3aks/hotel/<int:hid>/mostcreditcard', methods=['POST'])
def get_clients_under30_most_reservations(hid):
    if request.method == 'POST':
        try:
            return LocalStatisticsController().get_top_clients_under30_most_reservations_with_credit_card(hid, request.json)
        except:
            return jsonify("Incomplete data in json."), 404
    else:
        return jsonify("Method Not Allowed"), 405

@app.route('/datafr3aks/hotel/<int:hid>/highestpaid', methods=['POST'])
def get_highest_paid_employees(hid):
    if request.method == 'POST':
        try:
            return LocalStatisticsController().get_top_highest_paid_regular_employees(hid, request.json)
        except:
            return jsonify("Incomplete data in json."), 404
    else:
        return jsonify("Method Not Allowed"), 405

@app.route('/datafr3aks/hotel/<int:hid>/mostdiscount', methods=['POST'])
def get_clients_most_discounts(hid):
    if request.method == 'POST':
        try:
            return LocalStatisticsController().get_top_clients_with_most_discounts(hid, request.json)
        except:
            return jsonify("Incomplete data in json."), 404
    else:
        return jsonify("Method Not Allowed"), 405

@app.route('/datafr3aks/hotel/<int:hid>/roomtype', methods=['POST'])
def get_reservations_by_room_type(hid):
    if request.method == 'POST':
        try:
            return LocalStatisticsController().get_total_reservations_by_room_type(hid, request.json)
        except:
            return jsonify("Incomplete data in json."), 404
    else:
        return jsonify("Method Not Allowed"), 405

@app.route('/datafr3aks/hotel/<int:hid>/leastguests', methods=['POST'])
def get_rooms_guest_capacity_ratio(hid):
    if request.method == 'POST':
        try:
            return LocalStatisticsController().get_top_rooms_with_least_guest_to_capacity_ratio(hid, request.json)
        except:
            return jsonify("Incomplete data in json."), 404
    else:
        return jsonify("Method Not Allowed"), 405
    
@app.route('/datafr3aks/employee/id', methods=['POST'])
def get_employee_id():
    if request.method == 'POST':
        try:
            return LoginController().get_employee_id(request.json)
        except:
            return jsonify("Incomplete data in json."), 404
    else:
        return jsonify("Method Not Allowed"), 405
    
@app.route('/datafr3aks/employee/hotels', methods=['POST'])
def get_employee_hotels():
    if request.method == 'POST':
        try:
            return LoginController().get_employee_hotels(request.json)
        except:
            return jsonify("Incomplete data in json."), 404
    else:
        return jsonify("Method Not Allowed"), 405
    
@app.route('/datafr3aks/employee/position', methods=['POST'])
def get_employee_position():
    if request.method == 'POST':
        try:
            return LoginController().get_employee_position(request.json)
        except:
            return jsonify("Incomplete data in json."), 404
    else:
        return jsonify("Method Not Allowed"), 405
    
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)
    
    #TESTING ONLY#####################
    # try:
    #     app.run(debug=False, port=port)
    # finally:
    #     streamlit_ui.terminate()
    ##################################