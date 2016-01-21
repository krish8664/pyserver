# -*- coding: utf-8 -*-
from __future__ import print_function

import signal
import pyuv

def on_write(client, error):
    print ("on_write")
    #client.keepalive(False, 0)
    client.close()

def on_read(client, data, error):
    print ("on_read")
    if data is None:
        client.close()
        clients.remove(client)
        return
    print (client, data)
    client.write(b"HTTP/1.1 200 OK\r\n\r\nHello World!", on_write)

def on_connection(server, error):
    print ("on_connection")
    print (server)
    client = pyuv.TCP(server.loop)
    server.accept(client)
    clients.append(client)
    client.start_read(on_read)

def signal_cb(handle, signum):
    #[c.close() for c in clients]
    signal_h.close()
    server.close()


print("PyUV version %s" % pyuv.__version__)

loop = pyuv.Loop.default_loop()
clients = []

server = pyuv.TCP(loop)
server.bind(("0.0.0.0", 8200))
server.listen(on_connection)

signal_h = pyuv.Signal(loop)
signal_h.start(signal_cb, signal.SIGINT)

loop.run()
#for client in clients:
    #print (client.getsockname())
print("Stopped!")
