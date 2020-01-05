# TTChat
Peer-to-peer chat software written in Python.

## What is it for?
TTChat is designed to be a safe chat system that will generate new keys for each session.
It's not intended to be used as WhatsApp or a similar chat program, it's for throwaway chats that don't need to/shouldn't be kept.

## How is it secured?
TTChat uses 4096-bit long RSA keys for every message, other than for the public key exchange, which cannot be encrypted.  
This should not be a problem, as no computer can get the private key from the public key, and the keys are recreated for every new chat session.

### How does it work?
Each machine will set up a server socket, and a client socket. The client will try to connect to a specified target, while the server accepts connections and checks if the origin is the target. If it's not, it'll kill the connection and wait for the target to connect. Once both peers have confirmed the targets, they will exchange public keys and be ready to chat.

## Requirements
**Python v3.6+**  
If you don't already have it, download it [here](https://www.python.org/downloads/).  
**cryptography>=2.8**  
Download it using `pip install "cryptography>=2.8"`, or download the wheel [here](https://pypi.org/project/cryptography/2.8/#files) and use `pip install (.whl file)`.

## Usage
To get the module through PyPi: `pip install ttchat`.  
While TTChat comes with a fully functional `__main__.py` file, it is mainly meant to demonstrate how TTChat works. You can get the module to build your own UI that will work with any other program that uses TTChat, including the example one.

### The `__main__.py` file
Run it as any other python script, using `python` or `python3 __main__.py`. It's a very short piece of code, as it just uses functions from `ttchat.p2p`. Simply give it a target machine and it'll start trying to connect.  
Once you see `Ready to receive messages.` and/or `Ready to send messages.`, the connection has been completed and messaging is ready.

# Documentation
To see how to use the TTChat module yourself, check out the [Documentation](https://github.com/MysteryBlokHed/ttchat/wiki).