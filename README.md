# TTChat
Peer-to-peer chat software written in Python.

## How does it work?
TTChat uses 4096-byte long RSA keys to encrypt/decrypt messages. Each machine will set up a server socket, and a client socket. The client will try to connect to a specified target, while the server accepts connections and checks if the origin is the target. If it's not, it'll kill the connection and wait for the target to connect. Once both servers have confirmed the targets, they will exchange public keys and be ready to chat.

## Requirements
**Python v3.6+**  
If you don't already have it, download it [here](https://www.python.org/downloads/).  
**cryptography>=2.8**  
Download it using `pip install "cryptography>=2.8"`, or download the wheel [here](https://pypi.org/project/cryptography/2.8/#files) and use `pip install (.whl file)`.

## Usage
To get the module through PyPi: `pip install ttchat`.  
While TTChat comes with a `__main__.py` file that you can easily use, you can also get the module to build your own UI that will work with any other TTChat program.  

### The `__main__.py` file
Run it as any other python script, using `python` or `python3 __main__.py`. It's a very short piece of code, as it just uses functions from `ttchat.p2p`. Simply give it a target machine and it'll start trying to connect.  
Once you see `Ready to receive messages.` and/or `Ready to send messages.`, the connection has been completed and messaging is ready.

# Documentation
To see how to use the TTChat module yourself, check out the [Documentation](https://github.com/MysteryBlokHed/ttchat/wiki).