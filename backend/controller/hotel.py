from flask import jsonify
from backend.model.hotel import HotelDAO
from backend.error_handling.utils import *

class HotelController:
    
    def create_dict(self, row):
        hotel_dict = {
            'hid': row[0],
            'chid': row[1],
            'hname': row[2],
            'hcity': row[3]
        }
        return hotel_dict
    
    def getAllHotels(self):
        dao = HotelDAO()
        hotel_list = dao.getAllHotels()
        result = [self.create_dict(hotel) for hotel in hotel_list]
        return jsonify(result)
    
    def getHotelById(self, hid):
        if hid < 0:
            return jsonify('Invalid hotel ID: Negative number'), 400

        dao = HotelDAO()
        hotel = dao.getHotelById(hid)
        if not hotel:
            return jsonify('Hotel Not Found'), 404
        else:
            hotel_dict = self.create_dict(hotel)
            return jsonify(hotel_dict), 200
    
    def addNewHotel(self, json):
        chid = json['chid']
        hname = json['hname']
        hcity = json['hcity']
        if len(json) > 3:
            return jsonify("Too many values entered"), 404
        error = handleHotelErrors(chid, hname, hcity)
        if error != False:
            return error
        dao = HotelDAO()
        addedHotel = dao.addNewHotel(chid, hname, hcity)
        result = self.create_dict(addedHotel)
        return jsonify(result), 201
    
    def updateHotel(self, hid, json):
        chid = json['chid']
        hname = json['hname']
        hcity = json['hcity']
        if len(json) > 3:
            return jsonify("Too many values entered"), 404
        error = handleHotelErrors(chid, hname, hcity)
        if error != False:
            return error
        dao = HotelDAO()
        updated_hotel = dao.updateHotel(hid, chid, hname, hcity)
        if updated_hotel:
            result = self.create_dict(updated_hotel)
            return jsonify(result), 200
        else:
            return jsonify("Hotel NOT FOUND"), 404
    
    def deleteHotel(self, hid):
        dao = HotelDAO()
        result = dao.deleteHotel(hid)
        if result:
            return jsonify("Hotel DELETED"), 200
        else:
            return jsonify("Hotel NOT FOUND"), 404
