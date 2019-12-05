import socket
import logging
import threadig

logger = logging.getLogger(__name__)
class TCPClient:

    def __init__(self, port, q, srv=False):
        self.srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.q = q

    def recv(self):
        while True:
            data = self.src.recv(1024)
            q.put(data)

    def listen(self):
        self.srv.bind(('127.0.0.1', self.port))



