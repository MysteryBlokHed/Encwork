# Created by MysteryBlokHed on 14/12/2019.
from ttchat.p2p import P2P

target = input("Enter the target machine IP: ")
chat = P2P()
chat.start(target)

while True:
    msg = input("")
    chat.send_msg(msg)