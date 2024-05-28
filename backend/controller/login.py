from flask import jsonify
from backend.model.login import LoginDAO
from backend.error_handling.utils import *

class LoginController:
    
    def create_dict(self, row):
        login_dict = {
            'lid': row[0],
            'eid': row[1],
            'username': row[2],
            'password': row[3]
        }
        return login_dict
    
    def employee_id_dict(self, row):
        login_dict = {
            'eid': row[0]
        }
        return login_dict
    
    def get_employee_id(self, json):
        username = json['username']
        password = json['password']
        if len(json) > 2:
            return jsonify("Too many values entered"), 404
        error = handleLogOnErrors(username, password)
        if error != False:
            return error
        dao = LoginDAO()
        eid = dao.get_employee_id(username, password)
        if eid:
            result = self.employee_id_dict(eid)
            return jsonify(result), 201
        else:
            return jsonify("No employee found for given credentials."), 404
        
    def get_employee_position(self, json):
        eid = json['eid']
        if len(json) > 1:
            return jsonify("Too many values entered"), 404
        dao = LoginDAO()
        position = dao.get_employee_position(eid)
        if position:
            return jsonify({'position':position}), 201
        else:
            return jsonify("No position found for given employee."), 404
        
    def get_employee_hotels(self, json):
        eid = json['eid']
        if len(json) > 1:
            return jsonify("Too many values entered"), 404
        dao = LoginDAO()
        hotels = dao.get_employee_hotels(eid)
        if hotels:
            return hotels
        else:
            return jsonify("No hotels found for given employee."), 404
    
    def getAllLogin(self):
        dao = LoginDAO()
        login_list = dao.getAllLogin()
        result = []
        for login in login_list:
            result.append(self.create_dict(login))
        return jsonify(result)
    
    def getLoginById(self, lid):
        dao = LoginDAO()
        login = dao.getLoginById(lid)
        if not login:
            return jsonify('Login Not Found'), 404
        else:
            login_dict = self.create_dict(login)
            return jsonify(login_dict), 200
    
    def addNewLogin(self, json):
        eid = json['eid']
        username = json['username']
        password = json['password']
        if len(json) > 3:
            return jsonify("Too many values entered"), 404
        error = handleLoginErrors(eid, username, password)
        if error != False:
            return error
        dao = LoginDAO()
        added_login = dao.addNewLogin(eid, username, password)
        result = self.create_dict(added_login)
        return jsonify(result), 201
    
    def updateLogin(self, lid, json):
        eid = json['eid']
        username = json['username']
        password = json['password']
        if len(json) > 3:
            return jsonify("Too many values entered"), 404
        error = handleLoginErrors(eid, username, password, lid)
        if error != False:
            return error
        dao = LoginDAO()
        updated_login = dao.updateLogin(lid, eid, username, password)
        if updated_login:
            result = self.create_dict(updated_login)
            return jsonify(result), 200
        else:
            return jsonify("Login NOT FOUND"), 404
    
    def deleteLogin(self, lid):
        dao = LoginDAO()
        result = dao.deleteLogin(lid)
        if result:
            return jsonify("Login DELETED"), 200
        else:
            return jsonify("Login NOT FOUND"), 404