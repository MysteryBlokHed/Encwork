# Created by MysteryBlokHed on 14/12/2019.
from encwork.p2p import P2P
from threading import Thread

global ready_to_send
ready_to_send = -1 # Will become 1 when both sides have exchanged keys

class StatusThread(Thread):
    def __init__(self, p2p):
        Thread.__init__(self)
        self._p2p = p2p
    
    def run(self):
        global ready_to_send
        for status in self._p2p.statuses():
            print(f"[{status['code']}] {status['data']}")
            if status["code"] == 8: # Message received
                print(f"[{status['data'][1][0]}] {status['data'][0]}")
            elif status["code"] == 12: # Connecting
                print("Connecting...")
            elif status["code"] == 14: # Connection failed
                print("Connection failed.")
            elif status["code"] == 13: # Connection established
                print("Connection established.")
            elif status["code"] == 15: # Sent public key
                ready_to_send += 1
                print("Sent public key.")
            elif status["code"] == 11: # Received public key
                print("Received public key.")
                ready_to_send += 1

p2p = P2P()
StatusThread(p2p).start()
p2p.start(input("Enter the target machine IP: "))

while True:
    while ready_to_send < 1:
        pass
    msg = input("Enter a message to send\n")
    p2p.send_msg(msg)