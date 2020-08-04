# Created by MysteryBlokHed on 04/01/2020.
class ExitTryExcept(Exception):
    """To break out of a try/catch without breaking a while/for loop."""
    pass

class NoTargetError(Exception):
    """No target is available to send messages to."""
    pass

class NoEncryptionKeyError(Exception):
    """There is no public key to encrypt with."""
    pass
