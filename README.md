# MACADAO Blockchain Dev

This project is a tutorial on blockchain technology, aiming to provide a better understanding of the mechanics behind a blockchain. It demonstrates the implementation of a blockchain from scratch, showcasing the concepts of proof of work and decentralization.

## Tutorial Video
Before diving into the code and details of the project, we recommend watching the following introductory video that provides an overview of blockchain technology and its fundamental concepts:

<iframe width="560" height="315" src="https://www.youtube.com/embed/qgREVIAzHI0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>


## Code Overview

The provided code implements a basic blockchain and exposes an API for interacting with it. Here is a summary of the main components and functionalities:

1. **Blockchain Class**: This class represents the blockchain itself and contains methods for block creation, proof of work, hashing, validation, transaction management, node management, and chain replacement.

2. **API Requests**: The code includes several API endpoints implemented using Flask, allowing you to interact with the blockchain. Here are the available endpoints:

   - `/mine_block`: This endpoint triggers the mining process to create a new block. It calculates the proof of work, adds transactions, and creates a new block in the blockchain.

   - `/get_chain`: This endpoint retrieves the full chain of the blockchain.

   - `/is_valid`: This endpoint checks if the entire blockchain is valid.

   - `/add_transaction`: This endpoint adds a new transaction to the transaction list, which will later be included in a mined block.

   - `/connect_node`: This endpoint connects a new node to the blockchain network.

   - `/replace_chain`: This endpoint replaces the current chain with the longest chain in the network, ensuring consensus.

## Getting Started

To run this project, follow these steps:

1. Make sure you have Python installed on your machine.

2. Install the necessary dependencies. You can use the following command:
   ```
   pip install flask requests
   ```

3. Copy the provided code into a file named `blockchain.py` or any other preferred filename.

4. Open a terminal or command prompt and navigate to the directory where the file is located.

5. Run the following command to start the blockchain:
   ```
   python blockchain.py
   ```

## API Usage

Once the blockchain is running, you can use the following API endpoints to interact with it:

- To mine a new block, make a GET request to `/mine_block`.

- To retrieve the full chain, make a GET request to `/get_chain`.

- To check the validity of the blockchain, make a GET request to `/is_valid`.

- To add a transaction, make a POST request to `/add_transaction` with the following JSON payload:
  ```
  {
    "sender": "SENDER_ADDRESS",
    "receiver": "RECEIVER_ADDRESS",
    "amount": AMOUNT
  }
  ```
  Replace `SENDER_ADDRESS`, `RECEIVER_ADDRESS`, and `AMOUNT` with appropriate values.

- To connect a new node to the network, make a POST request to `/connect_node` with the following JSON payload:
  ```
  {
    "nodes": ["NODE1_URL", "NODE2_URL", ...]
  }
  ```
  Replace `"NODE1_URL"`, `"NODE2_URL"`, etc., with the URLs of the nodes you want to connect.

- To replace the current chain with the longest chain in the network, make a GET request to `/replace_chain`.

**Note:** Replace `NODE1_URL`, `NODE2_URL`, etc., with the actual URLs of the nodes you want to connect.

## Conclusion

This project provides an educational implementation of a blockchain from scratch, emphasizing the concepts of proof of work and decentralization. By running the code and interacting with the provided API endpoints, you can gain a better understanding of how a blockchain functions. Feel free to explore and experiment with the code to enhance your understanding of blockchain technology.
