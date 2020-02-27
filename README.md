# Encwork
RSA-encrypted networking library.

## What is it for?
Encwork is designed to be a safe networking system that will generate new keys for each session. It can be used for CLI's or command line tools, general networking that should be encrypted, or throwaway chats.

## How is it secured?
Encwork uses 4096-bit RSA keys (size changable, 4096 recommended) for every message other than for the public key exchange, which cannot be encrypted and does not need to be.  
This should not be a problem, as no computer can get the private key from the public key, and the keys are recreated for every new session.

## How does it work?
### P2P
Each machine will set up a server socket, and a client socket. The client will try to connect to a specified target, while the server accepts connections and checks if the origin is the target. If it's not, it'll kill the connection and wait for the target to connect. Once both peers have confirmed the targets, they will exchange public keys and be ready to communicate.

### Server-Based
There will be one machine running a server, and multiple clients can connect to it. The server talks to each client individually, but Encwork provides enough freedom that you could set up a system that allows users to talk to each other. The server will store all client's public keys & sockets in a dictionary, so all clients still have different keys that don't cross paths.

## Requirements
**Python v3.6+**  
If you don't already have it, download it [here](https://www.python.org/downloads/).  
**cryptography>=2.8**  
Download it using `pip install "cryptography>=2.8"`, or download the wheel [here](https://pypi.org/project/cryptography/2.8/#files) and use `pip install (.whl file)`.

## Installation
### PyPI
To get the module through PyPi: `pip install encwork`.  
### GitHub (Pulled Repo)
To install the module by pulling the repo: `python setup.py install`.

## Usage
While Encwork comes with demonstration files such as `p2p_example.py`, `client_example.py` and `server_example.py`, they are only meant to demonstrate how Encwork works. You can get the module to build your own UI that will work with any other program that uses Encwork, including the example one.

### The `p2p_example.py` file
Run it as any other python script, using `python` or `python3 p2p_example.py`. It's a very short piece of code, as it just uses functions from `encwork.p2p`. Simply give it a target machine and it'll start trying to connect.  
Once you see the prompt "`Enter a message to send`," the connection and key exchange have completed and you are ready to communicate.

### The `client_example.py` and `server_example.py` files
As explained above, one machine will run the server (`server_example.py`) and allow clients to connect to it (`client_example.py`). The example files are for a server that returns ping, for one- and two-way, including encryption/decryption in the time.

# Documentation
To see how to use the Encwork module yourself, check out the [Documentation](https://github.com/MysteryBlokHed/Encwork/wiki).
