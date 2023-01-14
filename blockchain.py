
import datetime
import hashlib
from flask import Flask,jsonify
import json

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1,prev_hash = '0')
        
    def create_block(self,proof,prev_hash):
        block = {'index':len(self.chain)+1 ,'timestamp':str(datetime.datetime.now()),
                 'proof': proof,'previous_hash':prev_hash}
        self.chain.append(block)
        return block
    
    def prev_block(self):
        return self.chain[-1]
    
    def proof_of_work(self,prevProof):
        newProof = 1
        checkProof = False
        while checkProof is False:
            hashOperation = hashlib.sha256(str(newProof**2-prevProof).encode()).hexdigest()
            if hashOperation[:4] == "0000":
                checkProof = True
            else:
                newProof+=1 
        return newProof
    
    def hash(self,block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def check_if_blockchain_is_valid(self,chain):
        previousBlock = chain[0]
        block_index = 1
        while block_index < len(chain):
            current_block = chain[block_index]
            #if current_block['previous_hash']!=previousBlock['previous_hash']:
            #    return False
            current_proof = current_block['proof']
            prev_proof = previousBlock['proof']
            hashOperation = hashlib.sha256(str(current_proof**2-prev_proof).encode()).hexdigest()
            if hashOperation[:4] !='0000':
                return False
            previousBlock = current_block
            block_index+=1
        return True 
    
# part - 2: Mining blockchain

# creating a web app
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# creating blockchain
tradeCoin = Blockchain()

# mine blockchain
@app.route('/mineBlock', methods = ['GET'])

def mine_block():
    previous_block = tradeCoin.prev_block()
    previous_proof = previous_block['proof']
    proof = tradeCoin.proof_of_work(previous_proof)
    previous_hash = tradeCoin.hash(previous_block)
    created_block = tradeCoin.create_block(proof, previous_hash)
    
    display = {'message':'!!congratulations, you just mined a block!!','index':created_block['index']
               ,'timestamp':created_block['timestamp'],'proof':created_block['proof'],
               'previous_hash':created_block['previous_hash']}
    return jsonify(display),200


# getting full blockchain

@app.route('/getChain', methods = ['GET'])

def getChain():
    display = {'Chain':tradeCoin.chain,'length':len(tradeCoin.chain)}
    return jsonify(display),200


###
@app.route('/check_chain',methods = ['GET'])

def check_chain():
    if tradeCoin.check_if_blockchain_is_valid(tradeCoin.chain) is True:
        text = "chain is valid"
        return jsonify(text),200
    else:
        text = "chain is not valid"
        return jsonify(text),200

# running the app
app.run(host='0.0.0.0',port = 5000)
    

