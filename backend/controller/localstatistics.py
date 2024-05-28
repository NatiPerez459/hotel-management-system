from flask import jsonify
from backend.model.localstatistics import LocalStatisticsDAO
from backend.model.hotel import HotelDAO

class LocalStatisticsController:
    
    def create_dict(self, column_names, row):
        return {col: row[idx] for idx, col in enumerate(column_names)}

    def get_top_handicap_rooms(self, hid, json):
        if len(json) > 1:
            return jsonify("Too many values entered"), 404
        
        dao = LocalStatisticsDAO()
        found_hotel = HotelDAO().getHotelById(hid)

        if not found_hotel: 
            return jsonify('Hotel Not Found'), 404
        
        if json != None:
            dao = LocalStatisticsDAO()
            employee_position = str(dao.getEmployeePosition(json['eid'])).lower()
            dao = LocalStatisticsDAO()
            employee_hotel = dao.getEmployeeHotel(json['eid'])
            if employee_hotel[0] != hid and employee_position == 'regular':
                return jsonify("EMPLOYEE DOES NOT BELONG TO THIS HOTEL"), 404
            dao = LocalStatisticsDAO()
            if employee_position == 'supervisor' and not dao.compareSupervisorChain(json['eid'], hid):
                return jsonify("SUPERVISOR DOES NOT BELONG TO THIS CHAIN"), 404

        dao = LocalStatisticsDAO()
        rows = dao.getTopHandicapRooms(hid)
        column_names = ('rid', 'total_reservations')
        result = [self.create_dict(column_names, row) for row in rows]
        return jsonify(result), 200

    def get_top_rooms_with_least_time_unavailable(self, hid, json):
        if len(json) > 1:
            return jsonify("Too many values entered"), 404
        
        dao = LocalStatisticsDAO()
        found_hotel = HotelDAO().getHotelById(hid)

        if not found_hotel: 
            return jsonify('Hotel Not Found'), 404
        
        if json != None:
            dao = LocalStatisticsDAO()
            employee_position = str(dao.getEmployeePosition(json['eid'])).lower()
            dao = LocalStatisticsDAO()
            employee_hotel = dao.getEmployeeHotel(json['eid'])
            if employee_hotel[0] != hid and employee_position == 'regular':
                return jsonify("EMPLOYEE DOES NOT BELONG TO THIS HOTEL"), 404
            dao = LocalStatisticsDAO()
            if employee_position == 'supervisor' and not dao.compareSupervisorChain(json['eid'], hid):
                return jsonify("SUPERVISOR DOES NOT BELONG TO THIS CHAIN"), 404

        dao = LocalStatisticsDAO()
        rows = dao.getTopRoomsWithLeastTimeUnavailable(hid)
        column_names = ('rid', 'total_days')
        result = [self.create_dict(column_names, row) for row in rows]
        return jsonify(result), 200

    def get_top_clients_under30_most_reservations_with_credit_card(self, hid, json):
        if len(json) > 1:
            return jsonify("Too many values entered"), 404
        
        dao = LocalStatisticsDAO()
        found_hotel = HotelDAO().getHotelById(hid)

        if not found_hotel: 
            return jsonify('Hotel Not Found'), 404
        
        if json != None:
            dao = LocalStatisticsDAO()
            employee_position = str(dao.getEmployeePosition(json['eid'])).lower()
            dao = LocalStatisticsDAO()
            employee_hotel = dao.getEmployeeHotel(json['eid'])
            if employee_hotel[0] != hid and employee_position == 'regular':
                return jsonify("EMPLOYEE DOES NOT BELONG TO THIS HOTEL"), 404
            dao = LocalStatisticsDAO()
            if employee_position == 'supervisor' and not dao.compareSupervisorChain(json['eid'], hid):
                return jsonify("SUPERVISOR DOES NOT BELONG TO THIS CHAIN"), 404

        dao = LocalStatisticsDAO()
        rows = dao.getTopClientsUnder30MostReservationsWithCreditCard(hid)
        column_names = ('clid', 'age','reservations')
        result = [self.create_dict(column_names, row) for row in rows]
        return jsonify(result), 200

    def get_top_highest_paid_regular_employees(self, hid, json):
        if len(json) > 1:
            return jsonify("Too many values entered"), 404
        
        dao = LocalStatisticsDAO()
        found_hotel = HotelDAO().getHotelById(hid)

        if not found_hotel: 
            return jsonify('Hotel Not Found'), 404
        
        if json != None:
            dao = LocalStatisticsDAO()
            employee_position = str(dao.getEmployeePosition(json['eid'])).lower()
            dao = LocalStatisticsDAO()
            employee_hotel = dao.getEmployeeHotel(json['eid'])
            if employee_hotel[0] != hid and employee_position == 'regular':
                return jsonify("EMPLOYEE DOES NOT BELONG TO THIS HOTEL"), 404
            dao = LocalStatisticsDAO()
            if employee_position == 'supervisor' and not dao.compareSupervisorChain(json['eid'], hid):
                return jsonify("SUPERVISOR DOES NOT BELONG TO THIS CHAIN"), 404

        dao = LocalStatisticsDAO()
        rows = dao.getTopHighestPaidRegularEmployees(hid)
        column_names = ('eid', 'salary')
        result = [self.create_dict(column_names, row) for row in rows]
        return jsonify(result), 200

    def get_top_clients_with_most_discounts(self, hid, json):
        if len(json) > 1:
            return jsonify("Too many values entered"), 404
        
        dao = LocalStatisticsDAO()
        found_hotel = HotelDAO().getHotelById(hid)

        if not found_hotel: 
            return jsonify('Hotel Not Found'), 404
        
        if json != None:
            dao = LocalStatisticsDAO()
            employee_position = str(dao.getEmployeePosition(json['eid'])).lower()
            dao = LocalStatisticsDAO()
            employee_hotel = dao.getEmployeeHotel(json['eid'])
            if employee_hotel[0] != hid and employee_position == 'regular':
                return jsonify("EMPLOYEE DOES NOT BELONG TO THIS HOTEL"), 404
            dao = LocalStatisticsDAO()
            if employee_position == 'supervisor' and not dao.compareSupervisorChain(json['eid'], hid):
                return jsonify("SUPERVISOR DOES NOT BELONG TO THIS CHAIN"), 404

        dao = LocalStatisticsDAO()
        rows = dao.TopClientsWithMostDiscounts(hid)
        column_names = ('clid', 'fname', 'lname', 'total_discount')
        result = [self.create_dict(column_names, row) for row in rows]
        return jsonify(result), 200

    def get_total_reservations_by_room_type(self, hid, json):
        if len(json) > 1:
            return jsonify("Too many values entered"), 404
        
        dao = LocalStatisticsDAO()
        found_hotel = HotelDAO().getHotelById(hid)

        if not found_hotel: 
            return jsonify('Hotel Not Found'), 404
        
        if json != None:
            dao = LocalStatisticsDAO()
            employee_position = str(dao.getEmployeePosition(json['eid'])).lower()
            str(employee_position).lower()
            dao = LocalStatisticsDAO()
            employee_hotel = dao.getEmployeeHotel(json['eid'])
            if employee_hotel[0] != hid and employee_position == 'regular':
                return jsonify("EMPLOYEE DOES NOT BELONG TO THIS HOTEL"), 404
            dao = LocalStatisticsDAO()
            if employee_position == 'supervisor' and not dao.compareSupervisorChain(json['eid'], hid):
                return jsonify("SUPERVISOR DOES NOT BELONG TO THIS CHAIN"), 404

        dao = LocalStatisticsDAO()
        rows = dao.TotalReservationsByRoomType(hid)
        column_names = ('rtype', 'total_reservations', 'reservation_percentage')
        result = [self.create_dict(column_names, row) for row in rows]
        return jsonify(result), 200

    def get_top_rooms_with_least_guest_to_capacity_ratio(self, hid, json):
        if len(json) > 1:
            return jsonify("Too many values entered"), 404
        
        dao = LocalStatisticsDAO()
        found_hotel = HotelDAO().getHotelById(hid)

        if not found_hotel: 
            return jsonify('Hotel Not Found'), 404
        
        if json != None:
            dao = LocalStatisticsDAO()
            employee_position = str(dao.getEmployeePosition(json['eid'])).lower()
            str(employee_position).lower()
            dao = LocalStatisticsDAO()
            employee_hotel = dao.getEmployeeHotel(json['eid'])
            if employee_hotel[0] != hid and employee_position == 'regular':
                return jsonify("EMPLOYEE DOES NOT BELONG TO THIS HOTEL"), 404
            dao = LocalStatisticsDAO()
            if employee_position == 'supervisor' and not dao.compareSupervisorChain(json['eid'], hid):
                return jsonify("SUPERVISOR DOES NOT BELONG TO THIS CHAIN"), 404

        dao = LocalStatisticsDAO()
        rows = dao.TopRoomsWithLeastGuestToCapacityRatio(hid)
        column_names = ('rid', 'guest_to_capacity_ratio')
        result = [self.create_dict(column_names, row) for row in rows]
        return jsonify(result), 200
