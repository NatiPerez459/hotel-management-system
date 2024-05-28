from flask import jsonify
from backend.model.roomdescription import RoomDescriptionDAO
from backend.error_handling.utils import *

class RoomDescriptionController:

    def create_dict(self, row):
        room__description_dict = {
            'rdid': row[0],
            'rname': row[1],
            'rtype': row[2],
            'capacity': row[3],
            'ishandicap': row[4]
        }
        return room__description_dict
    
    def getAllRoomDescriptions(self):
        dao = RoomDescriptionDAO()
        room_description_list = dao.getAllRoomDescriptions()
        result = []
        for room_description in room_description_list:
            result.append(self.create_dict(room_description))
        return jsonify(result)
    
    def getRoomDescriptionById(self, rdid):
        dao = RoomDescriptionDAO()
        room_description = dao.getRoomDescriptionById(rdid)
        if not room_description:
            return jsonify('Room Description Not Found'), 404
        else:
            room_description_dict = self.create_dict(room_description)
            return jsonify(room_description_dict), 200
    
    def addNewRoomDescription(self, json):
        rname = json['rname']
        rtype = json['rtype']
        capacity = json['capacity']
        ishandicap = json['ishandicap']
        if len(json) > 4:
            return jsonify("Too many values entered"), 404
        error = handleRoomDescriptionErrors(rname, rtype, capacity, ishandicap)
        if error != False:
            return error
        dao = RoomDescriptionDAO()
        added_room_description = dao.addNewRoomDescription(rname, rtype, capacity, ishandicap)
        result = self.create_dict(added_room_description)
        return jsonify(result), 201

    def updateRoomDescription(self, rdid, json):
        rname = json['rname']
        rtype = json['rtype']
        capacity = json['capacity']
        ishandicap = json['ishandicap']
        if len(json) > 4:
            return jsonify("Too many values entered"), 404
        error = handleRoomDescriptionErrors(rname, rtype, capacity, ishandicap)
        if error != False:
            return error
        dao = RoomDescriptionDAO()
        updated_room_description = dao.updateRoomDescription(rdid, rname, rtype, capacity, ishandicap)
        if updated_room_description:
            result = self.create_dict(updated_room_description)
            return jsonify(result), 200
        else:
            return jsonify("Room Description NOT FOUND"), 404
    
    def deleteRoomDescription(self, rdid):
        dao = RoomDescriptionDAO()
        result = dao.deleteRoomDescription(rdid)
        if result:
            return jsonify("Room Description DELETED"), 200
        else:
            return jsonify("Room Description NOT FOUND"), 404