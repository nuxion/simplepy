import socket
import random
import logging
import threading

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Node:

    def __init__(self, port):
        self.socket = socket.socket(type=socket.SOCK_DGRAM)
        #self.host = socket.gethostname()
        self.host = "localhost"
        self.port = port
        self.socket.bind((self.host, self.port))
        logger.info("Node {} listen on {}"\
                .format(self.host, self.port))

    def recv(self):
        while True:
            msg, address = self.socket.recvfrom(1024)
            print(msg)
            logger.info("address: {}".format(address))

    def send(self, msg, port):
        self.socket.sendto(msg, (self.host, port))

    def listen(self):
         t = threading.Thread(target=self.recv)
         t.start()
         t.join()
         self.socket.close()

if __name__ == '__main__':
    import sys

    port = sys.argv[1]
    #import pdb; pdb.set_trace()
    server = Node(int(port))
    server.listen()
    #clients = sys.argv[2]
