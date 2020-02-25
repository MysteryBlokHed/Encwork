# Created by MysteryBlokHed on 13/12/2019.
import socket
from datetime import datetime
from math import ceil
from threading import Thread
from time import sleep

from .encryption import *
from. exceptions import *

HEADERSIZE = 16
global peer_public_key
global latest_message
global latest_time
peer_public_key = None
latest_message = ""
latest_time = datetime.now()

class P2P(object):
    """
    `port: int` - The port to host Encwork on.

    `peer_port: int` - The port that the peer is hosting Encwork on.
    """
    def __init__(self, port: int=2006, peer_port: int=2006):
        self.port = port
        self.peer_port = peer_port
        self._private_key = gen_private_key()
        print("Generated private key.")
        print("Setting up client socket...")
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Set up client socket.")

    def headerify(self, message: bytes):
        """Add the 16-byte header (specifies msg length) to the message"""
        return bytes(f"{len(message):<{HEADERSIZE}}", "utf-8") + message
    
    def start(self, target: str):
        GetMessages(target, self._private_key, self.port).start()
        while True:
            try:
                print(f"Trying to connect to target ({target})...")
                self._s.connect((target, self.peer_port))
                print("Connection established to target.")
                print("Sending public RSA key...")
                self._s.send(self.headerify(get_public_key_text(get_public_key(self._private_key))))
                print("Sent public key.")
                break
            except:
                print(f"Connection to {target} failed. Waiting 5 seconds, then trying again...")
                sleep(5)
        print("Ready to send messages.")

    def send_msg(self, message: str):
        """Send an encrypted message to the peer."""
        global peer_public_key
        # Wait until a public key is available
        while peer_public_key == None:
            print("Waiting for public key to encrypt message...")
            sleep(5)
        # Tell the peer many messages that come in are a part of this one
        # (Done due to the size limit of RSA keys)
        split_size = ceil(len(message)/446)
        split_size_enc = self.headerify(encrypt(bytes(str(split_size), "utf-8"), peer_public_key))
        self._s.send(split_size_enc)
        # Send the message in as many parts as needed
        for i in range(split_size):
            enc_message = self.headerify(encrypt(bytes(message[446*i:446*(i+1)], "utf-8"), peer_public_key))
            self._s.send(enc_message)
        print("Sent message.")

    def stream_messages(self):
        """Create a generator that will stream new messages from the peer."""
        # Pull and set globals to communicate with GetMessages Thread
        global latest_message
        global latest_time
        s_latest_message = latest_message
        s_latest_time = latest_time
        while True:
            if s_latest_message != latest_message or latest_time > s_latest_time:
                yield latest_message
                s_latest_message = latest_message
                s_latest_time = latest_time

class GetMessages(Thread):
    def __init__(self, target: str, key, port: int):
        self.port = port
        Thread.__init__(self)
        self._target = target
        print("Setting up server socket...")
        self._sv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Binding...")
        self._sv.bind(("0.0.0.0", self.port))
        self._sv.listen(4)
        print("Set up server socket.")
        self._key = key

    def run(self):
        global peer_public_key
        global latest_message
        print("Run thread started.")

        # Accept connection and make sure it's from the target
        while True:
            self._s, addr = self._sv.accept()
            print("Connection received!")
            print("Checking target...")
            if addr[0] == self._target:
                print("Target verified!")
                cont = True
                break
            else:
                print(f"Connection from unknown source ({addr[0]})")
                self._s.close()

        # Receive public key
        print("Receiving public key...")
        try:
            full_msg = b""
            new_msg = True

            while True:
                msg = self._s.recv(16)

                if new_msg:
                    msg_len = int(msg[:HEADERSIZE])
                    new_msg = False
                
                full_msg += msg

                if(len(full_msg) - HEADERSIZE == msg_len):
                    # Save the public key
                    self._peer_key = full_msg[HEADERSIZE:]
                    peer_public_key = self._peer_key
                    print("Received public key.")
                    break
        except Exception as e:
            print("Failed to get peer's public key.")
            print(e)
            cont = False

        # Message receive loop
        print("Ready to receive messages.")
        while cont:
            # Get message length
            full_msg = b""
            try:
                new_msg = True

                while True:
                    msg = self._s.recv(16)

                    if new_msg:
                        msg_len = int(msg[:HEADERSIZE])
                        new_msg = False
                    
                    full_msg += msg

                    if(len(full_msg) - HEADERSIZE == msg_len):
                        print("Decrypting message...")
                        # Decrypt length and convert to int
                        full_msg_len = int(decrypt(full_msg[HEADERSIZE:], self._key))
                        actual_full_message = []
                        # Get all parts of message
                        for i in range(full_msg_len):
                            full_msg = b""
                            try:
                                new_msg = True

                                while True:
                                    msg = self._s.recv(16)

                                    if new_msg:
                                        msg_len = int(msg[:HEADERSIZE])
                                        new_msg = False
                                    
                                    full_msg += msg

                                    if(len(full_msg) - HEADERSIZE == msg_len):
                                        actual_full_message.append(full_msg[HEADERSIZE:])
                                        raise ExitTryExcept
                            except ExitTryExcept:
                                pass
                            except Exception as e:
                                print("Failed to receive peer's message.")
                                print(e)
                                cont = False

                        # Put the message together
                        full_message_dec = b""
                        for i in actual_full_message:
                            full_message_dec += decrypt(i, self._key)
                        latest_message = full_message_dec
                        latest_time = datetime.now()
                        raise ExitTryExcept
            except ExitTryExcept as e:
                pass
