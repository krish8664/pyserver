# -*- coding:utf-8 -*-

import pyuv
import signal

def on_write(client, error):
    print(''' callback for write''')
    client.close()

def on_read(client, data, error):
    print(''' callback for the start_read''')
    if not data:
        pass
    else:
        client.write(data, on_write)

def on_connection(server, error):
    print(''' callback for listen''')
    client = pyuv.TCP(server.loop)
    server.accept(client)
    client.start_read(on_read)

def bind_loop(loop, ip, port):
    print("@ bind_loop")
    print(loop, ip, port)
    server = pyuv.TCP(loop)
    server.bind((ip, port))
    server.listen(on_connection)
    

def run(ip="127.0.0.1", port=8080):
    print ("@ run")

    # declare an event loop
    loop = pyuv.Loop.default_loop()
    
    # Start the server
    #bind_loop(loop, ip, port)
    server = pyuv.TCP(loop)
    server.bind((ip, port))
    server.listen(on_connection)

    # Signal handlers to quit
    sigint_h = pyuv.Signal(loop)
    sigint_h.start(lambda *x: loop.stop(), signal.SIGINT)
    sigterm_h = pyuv.Signal(loop)
    sigterm_h.start(lambda *x: loop.stop(), signal.SIGTERM)    

    # Start the event loop
    loop.run()

    for handle in loop.handles:
        if not handle.closed:
            handle.close()
