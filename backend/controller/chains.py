from flask import jsonify
from backend.model.chains import ChainsDAO
from backend.error_handling.utils import *

class ChainController:
    
    def create_dict(self, row):
        chain_dict = {
            'chid': row[0],
            'cname': row[1],
            'springmkup': row[2],
            'summermkup': row[3],
            'fallmkup': row[4],
            'wintermkup': row[5]
        }
        return chain_dict
    
    def getAllChains(self):
        dao = ChainsDAO()
        chain_list = dao.getAllChains()
        result = [self.create_dict(chain) for chain in chain_list]
        return jsonify(result)
    
    def getChainById(self, chid):
        if chid < 0:
            return jsonify('Invalid Chain ID: Negative number'), 400

        dao = ChainsDAO()
        chain = dao.getChainById(chid)
        if not chain:
            return jsonify('Chain Not Found'), 404
        else:
            chain_dict = self.create_dict(chain)
            return jsonify(chain_dict), 200
    
    def addNewChain(self, json):
        cname = json['cname']
        springmkup = json['springmkup']
        summermkup = json['summermkup']
        fallmkup = json['fallmkup']
        wintermkup = json['wintermkup']
        if len(json) > 5:
            return jsonify("Too many values entered"), 404
        error = handleChainErrors(cname, springmkup, summermkup, fallmkup, wintermkup)
        if error != False:
            return error
        dao = ChainsDAO()
        new_chain = dao.addNewChain(cname, springmkup, summermkup, fallmkup, wintermkup)
        result = self.create_dict(new_chain)
        return jsonify(result), 201
    
    def updateChain(self, chid, json):
        cname = json['cname']
        springmkup = json['springmkup']
        summermkup = json['summermkup']
        fallmkup = json['fallmkup']
        wintermkup = json['wintermkup']
        if len(json) > 5:
            return jsonify("Too many values entered"), 404
        error = handleChainErrors(cname, springmkup, summermkup, fallmkup, wintermkup)
        if error != False:
            return error
        dao = ChainsDAO()
        updated_chain = dao.updateChain(chid, cname, springmkup, summermkup, fallmkup, wintermkup)
        if updated_chain:
            result = self.create_dict(updated_chain)
            return jsonify(result), 200
        else:
            return jsonify('Chain Not Found'), 404
    
    def deleteChain(self, chid):
        dao = ChainsDAO()
        result = dao.deleteChain(chid)
        if result:
            return jsonify("Chain DELETED"), 200
        else:
            return jsonify("Chain NOT FOUND"), 404
