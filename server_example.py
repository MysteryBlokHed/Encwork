# Created by MysteryBlokHed on 23/02/2020.
from encwork.server import Server
from datetime import datetime
from threading import Thread

server = Server()

class StatusThread(Thread):
    def __init__(self, server):
        Thread.__init__(self)
        self._server = server

    def run(self):
        for status in server.statuses():
            print(f"[{status['date']}] {status['code']}: {status['data']}")
            if status["code"] == 8: # Message received
                server.send_msg(status["date"].strftime("%Y-%m-%d-%H-%M-%S-%f"), status['data'][1]) # Send the date the message was received serverside

server.start()
StatusThread(server).start()
