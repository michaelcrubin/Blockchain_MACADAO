#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 11:37:45 2022
@author: michaelrubin
Project: MACADAO Blockchain Dev
"""

# Importing the needed libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify


# 1. Intializing the Blockchain Class

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
        
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        self.chain.append(block)
        return(block)
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
      
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            # here I check if the hashs are corresponding
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof =  block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True



# 2. Mining a Block

# Creating a Flask Web app ( can be substituted by ODAPES??)
app = Flask(__name__)

# initiating Blockchain instance
blockchain1 = Blockchain()

# API request to mine a Block
@app.route("/mine_block", methods = ['GET'])
def mine_block():
    previous_block = blockchain1.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain1.proof_of_work(previous_proof)
    previous_hash = blockchain1.hash(previous_block)
    block = blockchain1.create_block(proof, previous_hash)
    response = {'message': 'Great, you just mined a block buddy!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200

# API request to get the full chain
@app.route("/get_chain", methods = ['GET'])
def get_chain():
    response = {'chain': blockchain1.chain,
                'lenght': len(blockchain1.chain)}
    return jsonify(response), 200
    
# Running the Flask App
app.run(host = '0.0.0.0', port = 5000)
























