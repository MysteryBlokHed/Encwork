# Created by MysteryBlokHed on 03/01/2020.
from encwork.p2p import P2P
from encwork.client import Client
from threading import Thread

# P2P
class PrintMessages(Thread):
    def __init__(self, chat):
        Thread.__init__(self)
        self._chat = chat

    def run(self):
        for msg in self._chat.stream_messages():
            print(msg)
# Server

# Ask which chat mode to use
while True:
    mode = input("Which chat mode is being used? (P2P, Server): ")
    if mode.upper() in ("P2P", "SERVER"):
        break
    else:
        print("Invalid choice.")

# P2P being used
if mode.upper() == "P2P":
    target = input("Enter the target machine IP: ")
    chat = P2P()
    chat.start(target)

    PrintMessages(chat).start()

    while True:
        msg = input("")
        chat.send_msg(msg)
# Server-based being used
elif mode.upper() == "SERVER":
    pass
else:
    print("Invalid chat mode.")