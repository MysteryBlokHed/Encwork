# Created by MysteryBlokHed on 13/12/2019.
import socket
from datetime import datetime
from math import ceil
from threading import Thread
from time import sleep

from .encryption import *
from .exceptions import *
from .status import *

HEADERSIZE = 16

class P2P(object):
    """
    `port: int` - The port to host Encwork on.

    `peer_port: int` - The port that the peer is hosting Encwork on.
    """
    def __init__(self, port: int=2006, peer_port: int=2006):
        self._peer_public_key = None
        self._latest_statuses = []

        self.port = port
        self.peer_port = peer_port
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
        """Internal function to accept connections to receive and then start a new thread of itself."""
        self._latest_statuses.append(Status(5))

        # Accept connection and make sure it's from the target
        while True:
            self._ss, addr = self._sv.accept()
            self._latest_statuses.append(Status(9, addr))
            if addr[0] == self._target:
                self._latest_statuses.append(Status(22, addr))
                cont = True
                break
            else:
                self._latest_statuses.append(Status(23, addr))
                self._s.close()

        # Receive public key
        self._latest_statuses.append(Status(18, addr))
        try:
            full_msg = b""
            new_msg = True

            while True:
                msg = self._ss.recv(16)

                if new_msg:
                    msg_len = int(msg[:HEADERSIZE])
                    new_msg = False
                
                full_msg += msg

                if(len(full_msg) - HEADERSIZE == msg_len):
                    # Save the public key
                    self._peer_public_key = full_msg[HEADERSIZE:]
                    self._latest_statuses.append(Status(11, addr))
                    break
        except Exception as e:
            self._latest_statuses.append(Status(19, addr))
            cont = False

        # Message receive loop
        while cont:
            # Get message length
            full_msg = b""
            try:
                new_msg = True

                while True:
                    msg = self._ss.recv(16)

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
                                    msg = self._ss.recv(16)

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
    
    def start(self, target: str, utf8: bool=True):
        """
        Start the Encwork connection.

        `target: str` The IP to connect to/receive connection from.

        `utf8: bool` Whether or not to send/receive encoded as UTF-8. Must be `False` for receiving/sending files such as executables or media.
        """
        self._utf8 = utf8
        # Set up server
        self._target = target
        self._latest_statuses.append(Status(3, "server"))
        self._sv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sv.bind(("0.0.0.0", self.port))
        self._sv.listen(4)
        self._latest_statuses.append(Status(4, "server"))
        Thread(target=self._connection).start()
        while True:
            try:
                # Try to connect
                self._latest_statuses.append(Status(12, target))
                self._s.connect((target, self.peer_port))
                self._latest_statuses.append(Status(13, target))
                # Send public key
                self._latest_statuses.append(Status(10, target))
                self._s.send(self.headerify(get_public_key_text(get_public_key(self._private_key))))
                self._latest_statuses.append(Status(15, target))
                break
            except:
                # Connection failed
                self._latest_statuses.append(Status(14, target))
                sleep(5)

    def send_msg(self, message: str or bytes):
        """
        Send a message to the peer.

        `message: str or bytes` The message to send. Should be str if utf8=True, and bytes if utf8=False.
        """
        # Check if the target is real
        if self._target is None:
            raise NoTargetError("No target is available to send messages to.")
        if self._peer_public_key is None:
            raise NoEncryptionKeyError("There is no public key to encrypt with.")

        # Tell the peer many messages that come in are a part of this one
        # (Done due to the size limit of RSA keys)
        split_size = ceil(len(message)/446)
        split_size_enc = self.headerify(encrypt(bytes(str(split_size), "utf-8"), self._peer_public_key))
        self._s.send(split_size_enc)
        # Send the message in as many parts as needed
        for i in range(split_size):
            if self._utf8:
                enc_message = self.headerify(encrypt(bytes(message[446*i:446*(i+1)], "utf-8"), self._peer_public_key))
            else:
                enc_message = self.headerify(encrypt(message[446*i:446*(i+1)], self._peer_public_key))
            self._s.send(enc_message)
        self._latest_statuses.append(Status(17, self._target))