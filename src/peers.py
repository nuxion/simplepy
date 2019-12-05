import socket
import random
import time
import logging
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WAIT = 1


class Node:

    def __init__(self, port, peers):
        self.socket = socket.socket(type=socket.SOCK_DGRAM)
        #self.host = socket.gethostname()
        self.host = "localhost"
        self.port = port
        self.socket.bind((self.host, self.port))
        self.state = b"ack"
        self.peers = peers
        logger.debug(peers)

    def recv(self):
        logger.info("Node {} listen on {}"\
                .format(self.host, self.port))
        while True:
            msg, address = self.socket.recvfrom(1024)
            # add lock
            self.state = msg
            print(msg)
            logger.debug("address: {}".format(address))
            logger.info("msg: {}".format(msg))

    def send(self, msg, port):

        try:
            self.socket.sendto(msg, (self.host, port))
            logger.debug("sent to {}".format(port))
        except OSError:
            logger.debug("Failed to connecto to {}".format(port))

    def random_ports(self):
        tmp = self.peers.copy()
        port1 = random.choice(tmp)
        _idx = tmp.index(port1)
        del(tmp[_idx])
        port2 = random.choice(tmp)
        return port1, port2
    
    def infect(self):

        while True:
            port1, port2 = self.random_ports()
            logger.debug("port1 {}, port2 {}".format(port1, port2))
            self.send(self.state, port1)
            self.send(self.state, port2)
            #time.sleep(WAIT)
            time.sleep(random.uniform(0, 1)*2)

    def listen(self):
         recv = threading.Thread(target=self.recv)
         rumor = threading.Thread(target=self.infect)
         recv.start()
         rumor.start()
         #self.socket.close()

def parse_ports(chain):
    return [ int(x) for x in chain.split(",")]

if __name__ == '__main__':
    import sys

    port = sys.argv[1]
    to_parse = sys.argv[2]
    peers = parse_ports(to_parse)

    #import pdb; pdb.set_trace()
    server = Node(int(port), peers)
    server.listen()
    #clients = sys.argv[2]
