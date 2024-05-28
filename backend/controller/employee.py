from flask import jsonify, request
from backend.model.employee import EmployeeDAO
from backend.error_handling.utils import *

class EmployeeController:
    
    def create_dict(self, row):
        employee_dict = {
            'eid': row[0],
            'hid': row[1],
            'fname': row[2],
            'lname': row[3],
            'age': row[4],
            'position': row[5],
            'salary': row[6]
        }
        return employee_dict
    
    def getAllEmployees(self):
        dao = EmployeeDAO()
        employee_list = dao.getAllEmployees()
        result = [self.create_dict(employee) for employee in employee_list]
        return jsonify(result)
    
    def getEmployeeById(self, eid):
        dao = EmployeeDAO()
        employee = dao.getEmployeeById(eid)
        if not employee:
            return jsonify('Employee Not Found'), 404
        else:
            employee_dict = self.create_dict(employee)
            return jsonify(employee_dict), 200
    
    def addNewEmployee(self, json):
        hid = json['hid']
        fname = json['fname']
        lname = json['lname']
        age = json['age']
        position = json['position']
        salary = json['salary']
        if len(json) > 6:
            return jsonify("Too many values entered"), 404
        error = handleEmployeeErrors(hid, fname, lname, age, position, salary)
        if error != False:
            return error
        dao = EmployeeDAO()
        employee = dao.addNewEmployee(hid, fname, lname, age, position, salary)
        result = self.create_dict(employee)
        return jsonify(result), 201
    
    def updateEmployee(self, eid, json):
        hid = json['hid']
        fname = json['fname']
        lname = json['lname']
        age = json['age']
        position = json['position']
        salary = json['salary']
        if len(json) > 6:
            return jsonify("Too many values entered"), 404
        error = handleEmployeeErrors(hid, fname, lname, age, position, salary)
        if error != False:
            return error
        dao = EmployeeDAO()
        updated_employee = dao.updateEmployee(eid, hid, fname, lname, age, position, salary)
        if updated_employee:
            result = self.create_dict(updated_employee)
            return jsonify(result), 200
        else:
            return jsonify("Employee NOT FOUND"), 404
    
    def deleteEmployee(self, eid):
        dao = EmployeeDAO()
        result = dao.deleteEmployee(eid)
        if result:
            return jsonify("Employee DELETED"), 200
        else:
            return jsonify("Employee NOT FOUND"), 404