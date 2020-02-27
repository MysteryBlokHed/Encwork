# Created by MysteryBlokHed on 21/02/2020.
import socket
from datetime import datetime
from math import ceil
from threading import Thread
from time import sleep

from .encryption import *
from .exceptions import *
from .status import *

HEADERSIZE = 16

class Server(object):
    """
    `port: int` - The port to host Encwork on.
    """
    def __init__(self, port: int=2006):
        self._peer_public_keys = {}
        self._sockets = {}
        self._latest_statuses = []

        self.port = port
        # Generate private key
        self._latest_statuses.append(Status(1))
        self._private_key = gen_private_key()
        self._latest_statuses.append(Status(2))
        # Set up socket
        self._latest_statuses.append(Status(3, "server"))
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.bind(("0.0.0.0", port))
        self._s.listen(4)
        self._latest_statuses.append(Status(4, "server"))
    
    def headerify(self, message: bytes):
        """Add the 16-byte header (specifies msg length) to the message"""
        return bytes(f"{len(message):<{HEADERSIZE}}", "utf-8") + message
    
    def statuses(self):
        """Streams statuses, such as messages and encryption status."""
        while True:
            if len(self._latest_statuses) > 0:
                for status in self._latest_statuses:
                    yield status
                self._latest_statuses = []

    def _connection(self):
        """Internal function to accept connections to receive and then start a new thread of itself."""
        self._latest_statuses.append(Status(5))
        # Accept connections
        while True:
            cs, addr = self._s.accept()
            self._sockets[addr] = cs
            self._latest_statuses.append(Status(9, addr))
            # Start new thread
            Thread(target=self._connection).start()
            # Send public key
            self._latest_statuses.append(Status(10, addr))
            cs.send(self.headerify(get_public_key_text(get_public_key(self._private_key))))
            self._latest_statuses.append(Status(15, addr))

            # Receive public key
            self._latest_statuses.append(Status(18, addr))
            try:
                full_msg = b""
                new_msg = True

                while True:
                    msg = cs.recv(16)

                    if new_msg:
                        msg_len = int(msg[:HEADERSIZE])
                        new_msg = False
                    
                    full_msg += msg

                    if(len(full_msg) - HEADERSIZE == msg_len):
                        # Save the public key
                        self._peer_public_keys[addr] = full_msg[HEADERSIZE:]
                        self._latest_statuses.append(Status(11, addr))
                        cont = True
                        break
            except Exception as e:
                self._latest_statuses.append(Status(19, addr))
                cont = False
            
            # Message receive loop
            while cont:
                full_msg = b""
                try:
                    new_msg = True

                    while True:
                        msg = cs.recv(16)

                        if new_msg:
                            msg_len = int(msg[:HEADERSIZE])
                            new_msg = False
                        
                        full_msg += msg

                        if(len(full_msg) - HEADERSIZE == msg_len):
                            self._latest_statuses.append(Status(7, addr))
                            # Decrypt length and convert to int
                            full_msg_len = int(decrypt(full_msg[HEADERSIZE:], self._private_key))
                            actual_full_message = []
                            # Get all parts of message
                            for i in range(full_msg_len):
                                full_msg = b""
                                try:
                                    new_msg = True

                                    while True:
                                        msg = cs.recv(16)

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
                                    self._latest_statuses.append(Status(21, addr))
                                    cont = False

                            # Assemble message
                            full_message_dec = b""
                            for i in actual_full_message:
                                full_message_dec += decrypt(i, self._private_key)
                            if self._utf8:
                                self._latest_statuses.append(Status(8, (full_message_dec.decode("utf-8"), addr)))
                            else:
                                self._latest_statuses.append(Status(8, (full_message_dec, addr)))
                            raise ExitTryExcept
                except ExitTryExcept:
                    pass

    def start(self, utf8: bool=True):
        """
        Start the Encwork server.

        `utf8: bool` Whether or not to send/receive encoded as UTF-8. Must be `False` for receiving/sending files such as executables or media.
        """
        self._utf8 = utf8
        Thread(target=self._connection).start()
    
    def send_msg(self, message: str, target: tuple):
        """
        Send a message to a target.

        `message: str or bytes` The message to send. Should be str if utf8=True, and bytes if utf8=False.

        `target: tuple` The IP & port to send the message to. They must have already connected to the server and have sent their public key.
        """
        # Check if the target is real
        if target not in self._sockets:
            raise NoTargetError("An invalid target was provided.")
        # Check if there is a public key for the target
        if target not in self._peer_public_keys:
            raise NoEncryptionKeyError("There is no public key from the target specified to encrypt with.")

        # Tell the peer many messages that come in are a part of this one
        # (Done due to the size limit of RSA keys)
        split_size = ceil(len(message)/446)
        split_size_enc = self.headerify(encrypt(bytes(str(split_size), "utf-8"), self._peer_public_keys[target]))
        self._sockets[target].send(split_size_enc)
        # Send the message in as many parts as needed
        self._latest_statuses.append(Status(16, target))
        for i in range(split_size):
            if self._utf8:
                self._sockets[target].send(self.headerify(encrypt(bytes(message[446*i:446*(i+1)], "utf-8"), self._peer_public_keys[target])))
            else:
                self._sockets[target].send(self.headerify(encrypt(message[446*i:446*(i+1)], self._peer_public_keys[target])))
        self._latest_statuses.append(Status(17, target))