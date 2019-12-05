import socket
import random
import time
import logging
import threading
import pickle
from gcounter import GCounter

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
        self.counter = GCounter(port, peers)
        self.lock = threading.Lock()
        logger.debug(peers)

    def add(self, x):
        self.counter.add(x)
        data = pickle.dumps(self.counter)
        self.infect(data)
    
    def query(self):
        return self.counter.query()

    def recv(self):
        logger.info("Node {} listen on {}"\
                .format(self.host, self.port))
        while True:
            msg, address = self.socket.recvfrom(1024)
            remote_counter = pickle.loads(msg)
            self.lock.acquire()
            try:
                self.counter.merge(remote_counter)
                logger.info("Counter now: {}".format(self.counter.query()))
                data = pickle.dumps(self.counter)
                self.infect(data, address)
            finally:
                self.lock.release()

            # self.state = int(msg)
            logger.debug("address: {}".format(address))
            logger.debug("msg: {}".format(msg))

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
    
    def choice_port(self, origin=None):
        tmp = self.peers.copy()
        if origin:
            _idx = tmp.index(origin)
            del(tmp[_idx])
        port1 = random.choice(tmp)
        return port1
    

    def infect(self, data, origin=None):

        if origin:
            port1 = self.choice_port(origin[1])
        else:
            port1 = self.choice_port()
        logger.debug("port1 {}".format(port1))
        self.send(data, port1)
        #time.sleep(WAIT)
        time.sleep(random.uniform(0, 1)*2)

    def listen(self):
         recv = threading.Thread(target=self.recv)
         rumor = threading.Thread(target=self.infect)
         recv.start()
         #rumor.start()
         #self.socket.close()

def parse_ports(chain):
    return [ int(x) for x in chain.split(",")]

if __name__ == '__main__':
    import sys

    port_crdt = sys.argv[1]
    port_client = sys.argv[2]
    to_parse = sys.argv[3]
    peers = parse_ports(to_parse)

    #import pdb; pdb.set_trace()
    server = Node(int(port_crdt), peers)
    server.listen()
    print("Hi!!!")

    #clients = sys.argv[2]
