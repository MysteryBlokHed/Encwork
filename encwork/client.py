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
        # Server's public RSA key
        self.__peer_public_key = None
        # Server's Fernet key
        self.__peer_key = None
        self.__target = None
        self.__latest_statuses = []

        self.port = port
        # Generate RSA private key
        self.__latest_statuses.append(Status(1))
        self.__private_key = gen_private_key()
        self.__latest_statuses.append(Status(2))
        # Set up socket
        self.__latest_statuses.append(Status(3, "client"))
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__latest_statuses.append(Status(4, "client"))

    def headerify(self, message: bytes):
        """Add the 16-byte header (specifies msg length) to the message"""
        return bytes(f"{len(message):<{HEADERSIZE}}", "utf-8") + message

    def statuses(self):
        """Streams statuses, such as messages and encryption status."""
        while True:
            if len(self.__latest_statuses) > 0:
                for status in self.__latest_statuses:
                    yield status
                self.__latest_statuses = []

    def __connection(self):
        """Internal function to connect to server and receive messages."""
        while True:
            try:
                # Try to connect
                self.__latest_statuses.append(Status(12, self.__target))
                self.__s.connect((self.__target, self.port))
                self.__latest_statuses.append(Status(13, self.__target))
                # Send public key
                self.__latest_statuses.append(Status(10, self.__target))
                self.__s.send(get_public_key_text(get_public_key(self.__private_key)))
                self.__latest_statuses.append(Status(15, self.__target))

                # Receive public key
                self.__latest_statuses.append(Status(18, self.__target))
                # try:
                #     full_msg = b""
                #     new_msg = True

                #     while True:
                #         msg = self.__s.recv(16)

                #         if new_msg:
                #             msg_len = int(msg[:HEADERSIZE])
                #             new_msg = False
                        
                #         full_msg += msg

                #         if(len(full_msg) - HEADERSIZE == msg_len):
                #             # Save the public key
                #             self.__peer_public_key = full_msg[HEADERSIZE:]
                #             self.__latest_statuses.append(Status(11, self.__target))
                #             cont = True
                #             break
                # except Exception as e:
                #     self.__latest_statuses.append(Status(19, self.__target))
                #     cont = False
                try:
                    # Get RSA key and save it
                    msg = self.__s.recv(256)
                    self.__peer_public_key = msg
                    self.__latest_statuses.append(Status(11, self.__target))

                    # Get RSA-encrypted Fernet key
                    msg = self.__s.recv(256)
                    self.__peer_key = decrypt_rsa(msg, self.__private_key)
                
                # Message receive loop
                while cont:

                    full_msg = b""
                    try:
                        new_msg = True

                        while True:
                            msg = self.__s.recv(16)

                            if new_msg:
                                msg_len = int(msg[:HEADERSIZE])
                                new_msg = False
                            
                            full_msg += msg

                            if(len(full_msg) - HEADERSIZE == msg_len):
                                self.__latest_statuses.append(Status(7, self.__target))
                                # Decrypt length and convert to int
                                full_msg_len = int(decrypt(full_msg[HEADERSIZE:], self.__private_key))
                                actual_full_message = []
                                # Get all parts of message
                                for i in range(full_msg_len):
                                    full_msg = b""
                                    try:
                                        new_msg = True

                                        while True:
                                            msg = self.__s.recv(16)

                                            if new_msg:
                                                msg_len = int(msg[:HEADERSIZE])
                                                new_msg = False
                                            
                                            full_msg += msg

                                            if(len(full_msg) - HEADERSIZE == msg_len):
                                                self.__latest_statuses.append(Status(7, self.__target))
                                                raise ExitTryExcept
                                    except ExitTryExcept:
                                        pass
                                    except Exception as e:
                                        self.__latest_statuses.append(Status(21, self.__target))
                                        cont = False

                                # Decrypt message
                                full_msg_dec = self.__private_key[1].decrypt(full_msg)
                                if self._utf8:
                                    self.__latest_statuses.append(Status(8, (full_msg_dec.decode("utf-8"), self.__target)))
                                else:
                                    self.__latest_statuses.append(Status(8, (full_msg_dec, self.__target)))

                                raise ExitTryExcept
                    except ExitTryExcept:
                        pass
            except:
                # Failed connection
                self.__latest_statuses.append(Status(14, self.__target))
                sleep(5)

    def start(self, target: str, utf8: bool=True):
        """
        Start the Encwork client.

        `target: str` The server to connect to.

        `utf8: bool` Whether or not to send/receive encoded as UTF-8. Must be `False` for receiving/sending files such as executables or media.
        """
        self.__utf8 = utf8
        self.__target = target
        Thread(target=self.__connection).start()
    
    def send_msg(self, message: str or bytes):
        """
        Send a message to the server.

        `message: str` The message to send. Should be str if utf8=True, and bytes if utf8=False.
        """
        # See if there is a target
        if self.__target is None:
            raise NoTargetError("No target is available to send messages to.")
        # See if a public key has been received
        if self.__peer_public_key is None:
            raise NoEncryptionKeyError("There is no public key to encrypt with.")

        # Send the message
        self.__latest_statuses.append(Status(16, self.__target))

        if self.__utf8:
            self.__s.send(self.headerify(encrypt_fernet(bytes(message, "utf-8"), self.__peer_key)))
        else:
            self.__s.send(self.headerify(encrypt(message, self.__peer_key)))
