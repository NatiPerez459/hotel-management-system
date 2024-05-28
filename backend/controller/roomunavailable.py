from flask import jsonify
from backend.model.roomunavailable import RoomUnavailableDAO
from backend.error_handling.utils import *

class RoomUnavailableController:
    
    def create_dict(self, row):
        room_unavailable_dict = {
            'ruid': row[0],
            'rid': row[1],
            'startdate': row[2],
            'enddate': row[3]
        }
        return room_unavailable_dict
    
    def getAllRoomUnavailable(self):
        dao = RoomUnavailableDAO()
        room_unavailable_list = dao.getAllRoomUnavailable()
        result = []
        for room_unavailable in room_unavailable_list:
            result.append(self.create_dict(room_unavailable))
        return jsonify(result)
    
    def getRoomUnavailableById(self, rdid):
        dao = RoomUnavailableDAO()
        room_unavailable = dao.getRoomUnavailableById(rdid)
        if not room_unavailable:
            return jsonify('Room Unavailable Not Found'), 404
        else:
            room_unavailable_dict = self.create_dict(room_unavailable)
            return jsonify(room_unavailable_dict), 200
    
    def addNewRoomUnavailable(self, json):
        rid = json['rid']
        startdate = json['startdate']
        enddate = json['enddate']
        if len(json) > 3:
            return jsonify("Too many values entered"), 404
        error =handleRoomUnavailableErrors(rid, startdate, enddate)
        if error != False:
            return error
        dao = RoomUnavailableDAO()
        added_room_unavailable = dao.addNewRoomUnavailable(rid, startdate, enddate)
        result = self.create_dict(added_room_unavailable)
        return jsonify(result), 201

    def updateRoomUnavailable(self, ruid, json):
        rid = json['rid']
        startdate = json['startdate']
        enddate = json['enddate']
        if len(json) > 3:
            return jsonify("Too many values entered"), 404
        error = handleRoomUnavailableErrors(rid, startdate, enddate)
        if error != False:
            return error
        dao = RoomUnavailableDAO()
        updated_room_unavailable = dao.updateRoomUnavailable(ruid, rid, startdate, enddate)
        if updated_room_unavailable:
            result = self.create_dict(updated_room_unavailable)
            return jsonify(result), 200
        else:
            return jsonify("Room Unavailable NOT FOUND"), 404
    
    def deleteRoomUnavailable(self, ruid):
        dao = RoomUnavailableDAO()
        result = dao.deleteRoomUnavailable(ruid)
        if result:
            return jsonify("Room Unavailable DELETED"), 200
        else:
            return jsonify("Room Unavailable NOT FOUND"), 404