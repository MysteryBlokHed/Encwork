# Created by MysteryBlokHed on 14/12/2019.
from ttchat.p2p import P2P
from threading import Thread

class PrintMessages(Thread):
    def __init__(self, chat):
        Thread.__init__(self)
        self._chat = chat

    def run(self):
        for msg in self._chat.stream_messages():
            print(msg)

target = input("Enter the target machine IP: ")
chat = P2P()
chat.start(target)

PrintMessages(chat).start()

while True:
    msg = input("")
    chat.send_msg(msg)