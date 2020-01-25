# Created by MysteryBlokHed on 15/12/2019.
from datetime import datetime
import json
import socket
from threading import Thread

from .encryption import *

# Username-related
global saved_usernames
global saved_usernames_file
global username_map
saved_usernames = None
usernames_file = ""
username_map = {}
# Logging-related
global log
log = None
# Connection(s)-related
global ip_socket_pairs
global peer_pairs
ip_socket_pairs = {}
peer_pairs = {}

def headerify(self, message: bytes):
        """Add the 16-byte header (specifies msg length) to the message"""
        return bytes(f"{len(message):<{HEADERSIZE}}", "utf-8") + message

class Server(object):
    def __init__(self, port=2006, allow_saved_usernames: bool=True, log_ips: bool=False, saved_usernames_file: str="encwork_saved_usernames.json", log_file: str="ip_logs.txt"):
        # Globals
        global saved_usernames
        global usernames_file
        global log
        # Class-specific
        self._port = port
        self._log_ips = log_ips
        # See if saved usernames are allowed, and load the list if they are.
        if allow_saved_usernames:
            usernames_file = saved_usernames_file
            try:
                with open(usernames_file, "r") as f:
                    saved_usernames = json.loads(f.read())
            # If no list is found, create an empty one.
            except FileNotFoundError:
                with open(usernames_file, "w") as f:
                    f.write("[]")
                    saved_usernames = []
        # See if IP logging is enabled, and set the file if it is.
        if log_ips:
            log = log_file
            
        # Set up server socket
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.bind((socket.gethostbyname(socket.gethostname), self.port))

class ConnectionManager(Thread):
    def __init__(self, s: socket, port: int, log_ips: bool, allow_saved_usernames: bool):
        self._s = s
        self._port = port
        self._log_ips = log_ips
        self._allow_saved_usenames = allow_saved_usernames
    
    def run(self):
        global log

        # Accept connections
        while True:
            s, addr = self._s.accept()
            print(f"Connection received from {addr[0]}.")
            print(f"Informing {addr[0]} of server settings...")
            ## Create data about IP logging/saved usernames
            # IP Logging
            inform_string = "logging="
            if self._log_ips:
                with open(log, "a") as f:
                    f.writelines(datetime.now().strftime(f"{addr[0]} [%d/%m/%Y %H:%M:%S]"))
                inform_string += "y"
            else:
                inform_string += "n"
            # Saved usernames
            if self._allow_saved_usenames:
                inform_string += "saved=y"
            else:
                inform_string += "saved=n"
            s.send(headerify(bytes(inform_string)))