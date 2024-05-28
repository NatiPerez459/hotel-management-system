from flask import jsonify
from backend.model.globalstatistics import GlobalStatisticsDAO

class GlobalStatisticsController:
    
    def create_dict(self, column_names, row):
        dict = {}
        for i in range(len(column_names)):
            dict[column_names[i]] = row[i]
        return dict
    
    def getMostReservations(self, json):
        if len(json) > 1:
            return jsonify("Too many values entered"), 404
        dao = GlobalStatisticsDAO()
        employee_position = dao.getEmployeePosition(json['eid'])
        if str(employee_position[0]).lower() != 'administrator':
            return jsonify("POSITION CANNOT ACCESS GLOBAL STATISTICS"), 404
        dao = GlobalStatisticsDAO()
        most_reservations = dao.getMostReservations()
        result = []
        for row in most_reservations:
            result.append(self.create_dict(('hid', 'chid', 'hname', 'hcity', 'reservations'), row))
        return jsonify(result), 200
    
    def getMostProfitMoth(self, json):
        if len(json) > 1:
            return jsonify("Too many values entered"), 404
        dao = GlobalStatisticsDAO()
        employee_position = dao.getEmployeePosition(json['eid'])
        if str(employee_position[0]).lower() != 'administrator':
            return jsonify("POSITION CANNOT ACCESS GLOBAL STATISTICS"), 404
        dao = GlobalStatisticsDAO()
        most_profit_month = dao.getMostProfitMoth()
        result = []
        for row in most_profit_month:
            result.append(self.create_dict(('chid', 'cname', 'month', 'reservations'), row))
        return jsonify(result), 200
    
    def getMostRevenue(self, json):
        if len(json) > 1:
            return jsonify("Too many values entered"), 404
        dao = GlobalStatisticsDAO()
        employee_position = dao.getEmployeePosition(json['eid'])
        if str(employee_position[0]).lower() != 'administrator':
            return jsonify("POSITION CANNOT ACCESS GLOBAL STATISTICS"), 404
        dao = GlobalStatisticsDAO()
        most_revenue = dao.getHighestTotalRevenue()
        result = []
        for row in most_revenue:
            result.append(self.create_dict(('chid', 'cname', 'revenue'), row))
        return jsonify(result), 200
    
    def getPayment(self, json):
        if len(json) > 1:
            return jsonify("Too many values entered"), 404
        dao = GlobalStatisticsDAO()
        employee_position = dao.getEmployeePosition(json['eid'])
        if str(employee_position[0]).lower() != 'administrator':
            return jsonify("POSITION CANNOT ACCESS GLOBAL STATISTICS"), 404
        dao = GlobalStatisticsDAO()
        payment = dao.getTotalRevPercByPayMethod()
        result = []
        for row in payment:
            result.append(self.create_dict(('payment', 'percentage'), row))
        return jsonify(result), 200
    
    def getLeastRooms(self, json):
        if len(json) > 1:
            return jsonify("Too many values entered"), 404
        dao = GlobalStatisticsDAO()
        employee_position = dao.getEmployeePosition(json['eid'])
        if str(employee_position[0]).lower() != 'administrator':
            return jsonify("POSITION CANNOT ACCESS GLOBAL STATISTICS"), 404
        dao = GlobalStatisticsDAO()
        chains = dao.getTop3ChainsLeastRooms()
        result = []
        for row in chains:
            result.append(self.create_dict(('cname', 'total_rooms'), row))
        return jsonify(result), 200
    
    def getMostCapacity(self, json):
        if len(json) > 1:
            return jsonify("Too many values entered"), 404
        dao = GlobalStatisticsDAO()
        employee_position = dao.getEmployeePosition(json['eid'])
        if str(employee_position[0]).lower() != 'administrator':
            return jsonify("POSITION CANNOT ACCESS GLOBAL STATISTICS"), 404
        dao = GlobalStatisticsDAO()
        chains = dao.getTop5HotelsMostCapacity()
        result = []
        for row in chains:
            result.append(self.create_dict(('hname', 'total_capacity'), row))
        return jsonify(result), 200