"""
Created on Sat Dec 18 14:39:15 2022
@author: michaelrubin
Project: MACADAO Blockchain Dev
Part: This script creates a boilerplate Cryptocurrency called MacaCo (MACA Coin)
"""


# Importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse


## 1. INITIALIZING THE BLOCKCHAIN CLASS

class Blockchain:
    # initializes Blockchain: chain, transations, nodes + creates genesis Block
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof = 1, previous_hash = '0')
        self.nodes = set()
    
    # creates a Block by adding metadata+transactions
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions}
        self.transactions = []
        self.chain.append(block)
        return block

    # gets the last block
    def get_previous_block(self):
        return self.chain[-1]
    
    # is the PoW algorithm itself
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
    
    # method hashes an entire Block
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    # Method checks if a Chain is valid (if hashes fit and of prooves are ok)
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
    
    # appends one transaction to the transaction list
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender': sender,
                                  'receiver': receiver,
                                  'amount': amount})
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1
   
    # adds a Node from url
    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
    
    # checks the longest chain and replaces it if finds a longer
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False


## API REQUESTS TO RUN IT

# 2. Mining a Block // adding Transactions + Mining a Block

# Creating a Flask Web app ( can be substituted by ODAPES??)
app = Flask(__name__)

# Creating an address for the node on Port 5000
node_address = str(uuid4()).replace('-', '')

# initiating Macaco, an instance of Blockchain class
MacaCo = Blockchain()

# API request to mine a Block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = MacaCo.get_previous_block()
    previous_proof = previous_block['proof']
    proof = MacaCo.proof_of_work(previous_proof)
    previous_hash = MacaCo.hash(previous_block)
    MacaCo.add_transaction(sender = 'NEWLY ISSUED MACACO', receiver = 'PAUL', amount = 1)
    block = MacaCo.create_block(proof, previous_hash)
    response = {'message': 'CONGRATS PAUL, you just mined a block! You get 1 Monkey ;)',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']}
    return jsonify(response), 200

# API request to get the full chain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': MacaCo.chain,
                'length': len(MacaCo.chain)}
    return jsonify(response), 200

# This is just the Api request to check if the entire Blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = MacaCo.is_chain_valid(MacaCo.chain)
    if is_valid:
        response = {'message': 'OK. The Blockchain is valid.'}
    else:
        response = {'message': 'NOT OK, The Blockchain is not valid.'}
    return jsonify(response), 200

# This is the API call to add a transaction to the transactions list, which will later be mined.
@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all(key in json for key in transaction_keys):
        return 'Some elements of the transaction are missing', 400
    index = MacaCo.add_transaction(json['sender'], json['receiver'], json['amount'])
    response = {'message': f'This transaction will be added to Block {index}'}
    return jsonify(response), 201


 # 3. Decentralize the Blockchain

# This creates the actual network by adding new nodes to the nodes variable
@app.route('/connect_node', methods = ['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No node", 400
    for node in nodes:
        MacaCo.add_node(node)
    response = {'message': 'All the nodes are now connected. The MACACO CHAIN contains the following nodes:',
                'total_nodes': list(MacaCo.nodes)}
    return jsonify(response), 201

# This replaces the chain by the longest chain if needed
@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    is_chain_replaced = MacaCo.replace_chain()
    if is_chain_replaced:
        response = {'message': 'The nodes had different chains -> chain was replaced by the longest one.',
                    'new_chain': MacaCo.chain}
    else:
        response = {'message': 'OK. The chain is the largest one.',
                    'actual_chain': MacaCo.chain}
    return jsonify(response), 200

# Running the Flask App
app.run(host = '0.0.0.0', port = 5003)
