# Created by MysteryBlokHed on 15/12/2019.
import socket
from threading import Thread

from .encryption import *

HEADERSIZE = 16

class Client(object):
    def __init__(self, port=2006):
        self.port = port
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def headerify(self, message):
        """Add the 16-byte header (specifies msg length) to the message"""
        return bytes(f"{len(message):<{HEADERSIZE}}", "utf-8") + message
    
    def start(self, target: str, self_username: str, target_username: str):
        # Connect to server
        while True:
            try:
                print(f"Trying to connect to server...")
                self._s.connect((target, self.port))
                print("Connection established to target.")
                print("Sending target username...")
                self._s.send(self.headerify(target_username))
                print("Sending public RSA key...")
                self._s.send(self.headerify(get_public_key_text(get_public_key(self._private_key))))
                print("Sent public key.")
                break
            except:
                print(f"Connection to {target} failed. Waiting 15 seconds then trying again...")
                sleep(15)
        print("Ready to send messages.")

class GetMessages(Thread):
    def __init__(self, target, port):
        Thread.__init__(self)
    
    def run(self):
        pass