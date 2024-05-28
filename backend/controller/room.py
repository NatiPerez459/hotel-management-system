from flask import jsonify
from backend.model.room import RoomDAO
from backend.error_handling.utils import *

class RoomController:
    
    def create_dict(self, row):
        room_dict = {
            'rid': row[0],
            'hid': row[1],
            'rdid': row[2],
            'rprice': row[3]
        }
        return room_dict
    
    def getAllRooms(self):
        dao = RoomDAO()
        room_list = dao.getAllRooms()
        result = []
        for room in room_list:
            result.append(self.create_dict(room))
        return jsonify(result)
    
    def getRoomById(self, rid):
        dao = RoomDAO()
        room = dao.getRoomById(rid)
        if not room:
            return jsonify('Room Not Found'), 404
        else:
            room_dict = self.create_dict(room)
            return jsonify(room_dict), 200
    
    def addNewRoom(self, json):
        hid = json['hid']
        rdid = json['rdid']
        rprice = json['rprice']
        if len(json) > 3:
            return jsonify("Too many values entered"), 404
        error = handleRoomErrors(hid, rdid, rprice)
        if error != False:
            return error
        dao = RoomDAO()
        added_room = dao.addNewRoom(hid, rdid, rprice)
        result = self.create_dict(added_room)
        return jsonify(result), 201
    
    def updateRoom(self, rid, json):
        hid = json['hid']
        rdid = json['rdid']
        rprice = json['rprice']
        if len(json) > 3:
            return jsonify("Too many values entered"), 404
        error = handleRoomErrors(hid, rdid, rprice)
        if error != False:
            return error
        dao = RoomDAO()
        updated_room = dao.updateRoom(rid, hid, rdid, rprice)
        if updated_room:
            result = self.create_dict(updated_room)
            return jsonify(result), 200
        else:
            return jsonify("Room NOT FOUND"), 404
    
    def deleteRoom(self, rid):
        dao = RoomDAO()
        result = dao.deleteRoom(rid)
        if result:
            return jsonify("Room DELETED"), 200
        else:
            return jsonify("Room NOT FOUND"), 404