#! /usr/bin/env python3

import sys

sys.path.append("../lib")       # for params

import  os, socket, params


switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

while True:
    sock, addr = lsock.accept()

    from framedSock import framedSend, framedReceive

    if not os.fork():
        print("new child process handling connection from", addr)
        while True:
            #payload = framedReceive(sock, debug)
            #if debug: print("rec'd: ", payload)
            #if not payload:
            #    if debug: print("child exiting")
            #    sys.exit(0)
            #payload += b"!"             # make emphatic!
            #framedSend(sock, payload, debug)
            payload = framedReceive(sock, debug)
            if debug: print("rec'd: ", payload)
            if not payload:
                break
            payload = payload.decode('utf-8')
            print("sending " + payload)
            if os.path.isfile(payload):
     #   size = os.stat(payload)
     #   size = size.st_size
     #   count = int(size/100)+1 #number of messages plus one for expected remainder bytes
     #   print (str(count) + "messages") # for debugging
     #   count = size.encode('utf-8')
     #   sock.send(count)
                getruns = open(payload, "rb")
                sock.send(b'LETSGO') #Lets drive this file to the end zone.. football references
                while True:
                    run = getruns.read(100)
                    print("sending ", run.decode('utf-8'))
                    sock.send(run)
                    print("sent " + run.decode('utf-8'))
                    if not run:
                        print("Done")
                        break
                sock.send(b'TDBABY') #Touchdown you're done
                getruns.close()
                sys.exit(0)
