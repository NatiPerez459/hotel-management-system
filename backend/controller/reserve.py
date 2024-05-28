from flask import jsonify
from backend.model.reserve import ReservationDAO
from backend.error_handling.utils import *

class ReservationController:
    
    def create_dict(self, row):
        reservation_dict = {
            'reid': row[0],
            'ruid': row[1],
            'clid': row[2],
            'total_cost': row[3],
            'payment': row[4],
            'guests': row[5]
        }
        return reservation_dict
    
    def getAllReservations(self):
        dao = ReservationDAO()
        reservation_list = dao.getAllReservations()
        result = []
        for reservation in reservation_list:
            result.append(self.create_dict(reservation))
        return jsonify(result)
    
    def getReservationById(self, reid):
        dao = ReservationDAO()
        reservation = dao.getReservationById(reid)
        if not reservation:
            return jsonify('Reservation Not Found'), 404
        else:
            reservation_dict = self.create_dict(reservation)
            return jsonify(reservation_dict), 200
    
    def addNewReservation(self, json):
        #error handling the payment method
        ruid = json['ruid']
        clid = json['clid']
        total_cost = json['total_cost']
        payment = json['payment']
        guests = json['guests']
        if len(json) > 5:
            return jsonify("Too many values entered"), 404
        error = handleReserveErrors(ruid, clid, total_cost, payment, guests)
        if error != False:
            return error
        dao = ReservationDAO()
        added_reservation = dao.addNewReservation(ruid,clid,total_cost,payment,guests)
        result = self.create_dict(added_reservation)
        return jsonify(result), 201
    
    def updateReservation(self, reid, json):
        #error handling the payment method
        ruid = json['ruid']
        clid = json['clid']
        total_cost = json['total_cost']
        payment = json['payment']
        guests = json['guests']
        if len(json) > 5:
            return jsonify("Too many values entered"), 404
        error = handleReserveErrors(ruid, clid, total_cost, payment, guests, reid)
        if error != False:
            return error
        dao = ReservationDAO()
        updated_reservation = dao.updateReservation(reid,ruid,clid,total_cost,payment,guests)
        if updated_reservation:
            result = self.create_dict(updated_reservation)
            return jsonify(result), 200
        else:
            return jsonify("Reservation NOT FOUND"), 404
    
    def deleteReservation(self, reid):
        dao = ReservationDAO()
        result = dao.deleteReservation(reid)
        if result:
            return jsonify("Reservation DELETED"), 200
        else:
            return jsonify("Reservation NOT FOUND"), 404