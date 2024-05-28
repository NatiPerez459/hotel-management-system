from flask import jsonify
from backend.model.client import ClientDAO
from backend.error_handling.utils import *

class ClientController:
    
    def create_dict(self, row):
        client_dict = {
            'clid': row[0],
            'fname': row[1],
            'lname': row[2],
            'age': row[3],
            'memberyear': row[4]
        }
        return client_dict
    
    def getAllClients(self):
        dao = ClientDAO()
        client_list = dao.getAllClients()
        result = []
        for client in client_list:
            result.append(self.create_dict(client))
        return jsonify(result)
    
    def getClientById(self, clid):
        dao = ClientDAO()
        client = dao.getClientById(clid)
        if not client:
            return jsonify('Client Not Found'), 404
        else:
            client_dict = self.create_dict(client)
            return jsonify(client_dict), 200
    
    def addNewClient(self, json):
        fname = json['fname']
        lname = json['lname']
        age = json['age']
        memberyear = json['memberyear']
        if len(json) > 4:
            return jsonify("Too many values entered"), 404
        error = handleClientErrors(fname, lname, age, memberyear)
        if error != False:
            return error
        dao = ClientDAO()
        added_client = dao.addNewClient(fname,lname,age,memberyear)
        result = self.create_dict(added_client)
        return jsonify(result), 201
    
    def updateClient(self, clid, json):
        fname = json['fname']
        lname = json['lname']
        age = json['age']
        memberyear = json['memberyear']
        if len(json) > 4:
            return jsonify("Too many values entered"), 404
        error = handleClientErrors(fname, lname, age, memberyear)
        if error != False:
            return error
        dao = ClientDAO()
        updated_client = dao.updateClient(clid,fname,lname,age,memberyear)
        if updated_client:
            result = self.create_dict(updated_client)
            return jsonify(result), 200
        else:
            return jsonify("Client NOT FOUND"), 404
    
    def deleteClient(self, clid):
        dao = ClientDAO()
        result = dao.deleteClient(clid)
        if result:
            return jsonify("Client DELETED"), 200
        else:
            return jsonify("Client NOT FOUND"), 404