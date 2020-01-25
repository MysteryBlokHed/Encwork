# Created by MysteryBlokHed on 05/01/2019.
statuses = ["GEN_PV_KEY_START",
            "GEN_PV_KEY_END",
            "SETUP_CLIENT_START",
            "SETUP_CLIENT_END",
            "TARGET_CONNECTION_START",
            "TARGET_CONNECTION_SUCCESS",
            "TARGET_CONNECTION_FAIL",
            "SEND_PB_KEY_START",
            "SEND_PB_KEY_END",
            "CLIENT_TO_PEER_ESTABLISHED",
            "SPLIT_SIZE_DETERMINED",
            "SPLIT_SIZE_ENCRYPTED",
            "SPLIT_SIZE_SENT",
            "MESSAGE_SEND_START",
            "MESSAGE_SEND_ITER",
            "MESSAGE_SEND_END",
            "SETUP_SERVER_START",
            "SERVER_BIND",
            "SETUP_SERVER_END",
            "GET_LOOP_STARTED",
            "PEER_CONNECTION_RECEIVED",
            "PEER_CONNECTION_CONFIRMED_TARGET",
            "PEER_CONNECTION_NOT_TARGET",
            "RECEIVE_PB_KEY_START",
            "RECEIVE_PB_KEY_SUCCESS",
            "RECEIVE_PB_KEY_FAIL",
            "PEER_TO_SERVER_ESTABLISHED"]

class Status(object):
    """
    Used in a stream generator to handle status updates, such as incoming messages, decryption status, etc.

    status_code - Either an integer or a string for a status code.  
    The string will be the status code (eg. GEN_PV_KEY_START), and the integer will be the index in the statuses  
    variable where that text code is.
    """
    def __init__(self, status_code):
        if type(status_code):
            if status_code.upper() in statuses:
                self._code = statuses[status_code]
                self._code_int = status_code
    
    def get_code(self):
        """Return the string version of the status code."""
        return self._code
    
    def get_code_int(self):
        """Return the int version of the status code."""
        return self._code_int