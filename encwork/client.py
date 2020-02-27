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

class Client(object):
    """
    `port: int` - The port that the server hosts Encwork on.
    """
    def __init__(self, port: int=2006):
        self._peer_public_key = None
        self._target = None
        self._latest_statuses = []

        self.port = port
        # Generate private key
        self._latest_statuses.append(Status(1))
        self._private_key = gen_private_key()
        self._latest_statuses.append(Status(2))
        # Set up socket
        self._latest_statuses.append(Status(3, "client"))
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._latest_statuses.append(Status(4, "client"))
    
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
        """Internal function to connect to server and receive messages."""
        while True:
            try:
                # Try to connect
                self._latest_statuses.append(Status(12, self._target))
                self._s.connect((self._target, self.port))
                self._latest_statuses.append(Status(13, self._target))
                # Send public key
                self._latest_statuses.append(Status(10, self._target))
                self._s.send(self.headerify(get_public_key_text(get_public_key(self._private_key))))
                self._latest_statuses.append(Status(15, self._target))

                # Receive public key
                self._latest_statuses.append(Status(18, self._target))
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
                            self._peer_public_key = full_msg[HEADERSIZE:]
                            self._latest_statuses.append(Status(11, self._target))
                            cont = True
                            break
                except Exception as e:
                    self._latest_statuses.append(Status(19, self._target))
                    cont = False
                
                # Message receive loop
                while cont:
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
                                self._latest_statuses.append(Status(7, self._target))
                                # Decrypt length and convert to int
                                full_msg_len = int(decrypt(full_msg[HEADERSIZE:], self._private_key))
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
                                        self._latest_statuses.append(Status(21, self._target))
                                        cont = False

                                # Assemble message
                                full_message_dec = b""
                                for i in actual_full_message:
                                    full_message_dec += decrypt(i, self._private_key)
                                if self._utf8:
                                    self._latest_statuses.append(Status(8, (full_message_dec.decode("utf-8"), self._target)))
                                else:
                                    self._latest_statuses.append(Status(8, (full_message_dec, self._target)))
                                raise ExitTryExcept
                    except ExitTryExcept:
                        pass
            except:
                # Failed connection
                self._latest_statuses.append(Status(14, self._target))
                sleep(5)

    def start(self, target: str, utf8: bool=True):
        """
        Start the Encwork client.

        `target: str` The server to connect to.

        `utf8: bool` Whether or not to send/receive encoded as UTF-8. Must be `False` for receiving/sending files such as executables or media.
        """
        self._utf8 = utf8
        self._target = target
        Thread(target=self._connection).start()
    
    def send_msg(self, message: str):
        """
        Send a message to the server.

        `message: str` The message to send. Should be str if utf8=True, and bytes if utf8=False.
        """
        # See if there is a target
        if self._target is None:
            raise NoTargetError("No target is available to send messages to.")
        # See if a public key has been received
        if self._peer_public_key is None:
            raise NoEncryptionKeyError("There is no public key to encrypt with.")

        # Tell the peer many messages that come in are a part of this one
        # (Done due to the size limit of RSA keys)
        split_size = ceil(len(message)/446)
        split_size_enc = self.headerify(encrypt(bytes(str(split_size), "utf-8"), self._peer_public_key))
        self._s.send(split_size_enc)
        # Send the message in as many parts as needed
        self._latest_statuses.append(Status(16, self._target))
        for i in range(split_size):
            if self._utf8:
                self._s.send(self.headerify(encrypt(bytes(message[446*i:446*(i+1)], "utf-8"), self._peer_public_key)))
            else:
                self._s.send(self.headerify(encrypt(message[446*i:446*(i+1)], self._peer_public_key)))
        self._latest_statuses.append(Status(17, self._target))