# Created by MysteryBlokHed on 23/02/2020.
from datetime import datetime

class Status(object):
    """
    `code: int` - The status code.

    `data` - The data included with the status. Will be `None` if there is no data.
    """
    def __init__(self, code: int=-1, data: str=None):
        # Check types
        if type(code) is int:
            self._code = code
        else:
            raise TypeError(f"Expected int for code, got {type(code).__name__}.")
        self._data = data
        # Set date
        self._date = datetime.now()

    def __getitem__(self, item):
        if item == "code":
            return self._code
        elif item == "data":
            return self._data
        elif item == "date":
            return self._date
        else:
            raise KeyError(item)
    
    def __setitem__(self, item, value):
        if item == "code":
            # Check types
            if type(value) is int:
                self._code = value
            else:
                raise TypeError(f"Expected int for code, got {type(value).__name__}.")
        elif item == "data":
            self._data = value
        else:
            raise KeyError(item)
