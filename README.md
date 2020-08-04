# Encwork
<!-- Shields.io Badges -->
[![Release](https://img.shields.io/github/v/release/MysteryBlokHed/Encwork?style=flat-square)](https://github.com/MysteryBlokHed/Encwork/releases)
[![License](https://img.shields.io/github/license/MysteryBlokHed/Encwork?style=flat-square)](https://github.com/MysteryBlokHed/Encwork/blob/master/LICENSE)
[![Wheel](https://img.shields.io/pypi/wheel/encwork?style=flat-square)](https://pypi.org/project/encwork/)
[![Python](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-blue?style=flat-square)](https://www.python.org/downloads/)
<!-- End of Badges -->
RSA-encrypted networking library.

## What is it for?
Encwork is designed to be a safe networking system that will generate new keys for each session. It can be used for CLI's or command line tools, general networking that should be encrypted, or throwaway chats.

## How is it secured?
Encwork uses 2048-bit RSA keys to encrypt a separate private key using the `cryptography` library's high-end Fernet encryption.

## How does it work?
### P2P
Each machine will set up a server socket, and a client socket. The client will try to connect to a specified target, while the server accepts connections and checks if the origin is the target. If it's not, it'll kill the connection and wait for the target to connect. Once both peers have confirmed the targets, they will exchange public keys, then private keys. They will then be ready to communicate.

### Server-Based
There will be one machine running a server, and multiple clients can connect to it. The server talks to each client individually, but Encwork provides enough freedom that you could set up a system that allows users to talk to each other. The server will store all client's public/private keys & sockets in a dictionary, so all clients still have different keys that don't cross paths.

## Requirements
**Python v3.6+**  
If you don't already have it, download it [here](https://www.python.org/downloads/).  
**cryptography>=2.8**  
Download it using `pip install "cryptography>=2.8"`, or download the wheel [here](https://pypi.org/project/cryptography/2.8/#files) and use `pip install (.whl file)`.

## Installation
### PyPI
To get the module through PyPi: `pip install encwork`.  
### GitHub (Pulled Repo)
To install the module after pulling the repo: `python setup.py install`.

# Documentation
To see how to use the Encwork module yourself, check out the [Documentation](https://github.com/MysteryBlokHed/Encwork/wiki).
