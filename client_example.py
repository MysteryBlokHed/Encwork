# Created by MysteryBlokHed on 23/02/2020.
from encwork.client import Client
from datetime import datetime
from threading import Thread

global time_sent
time_sent = None # The time the client sent the ping request (used to calculate ping)
global ready_to_send
ready_to_send  = -1 # Will become 1 when both sides have exchanged keys

class StatusThread(Thread):
    def __init__(self, client):
        Thread.__init__(self)
        self._client = client
    
    def run(self):
        global time_sent
        global ready_to_send
        for status in self._client.statuses():
            if status["code"] == 8: # Message received
                # Convert sent date to datetime object
                date_array = []
                for i in status["data"][0].split("-"):
                    date_array.append(int(i))
                date = datetime(*date_array)
                # From client to server
                print(f"PING TO SERVER (s)         : {str(date-time_sent).strip('00:')}")
                print(f"PING TO SERVER AND BACK (s): {str(status['date']-time_sent).strip('00:')}")
            elif status["code"] == 13: # Connection established
                print("Connection established.")
            elif status["code"] == 15: # Sent public key
                print("Sent public key.")
                ready_to_send += 1
            elif status["code"] == 11: # Received public key
                print("Received public key.")
                ready_to_send += 1

client = Client()
client.start(input("Server IP: "))
StatusThread(client).start()

print("Waiting for key exchange...")
while True:
    while ready_to_send < 1:
        pass
    print("Press ENTER to get encrypted traffic ping to server.")
    input("")
    time_sent = datetime.now()
    client.send_msg("")
