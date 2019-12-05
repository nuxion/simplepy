import threading
import queue
import logging
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from crdt_server import parse_ports, Node

q = queue.Queue()
logger = logging.getLogger(__name__)

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        path = self.path.split("/")[1]
        try:
            value = int(path)
            server.add(value)
            time.sleep(3)

            self.wfile.write('Actual state: {}'.format(server.query()).encode())
        except ValueError:
            self.wfile.write('Actual state: {}'.format(server.query()).encode())

        #q.put(value)
        

if __name__ == '__main__':
    import sys
    
    port_crdt = sys.argv[1]
    port_client = int(sys.argv[2])
    to_parse = sys.argv[3]
    peers = parse_ports(to_parse)

    #import pdb; pdb.set_trace()
    server = Node(int(port_crdt), peers)
    server.listen()

    httpd = HTTPServer(('localhost', port_client), SimpleHTTPRequestHandler)
    logger.info("Http listening on: {}".format(port_client))
    
    http = threading.Thread(target=httpd.serve_forever)
    http.start()
    #while True:
    #    value = q.get()
    #    server.add(int(value))


 
