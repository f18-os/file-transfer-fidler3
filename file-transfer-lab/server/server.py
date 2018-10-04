#! /usr/bin/env python3

import sys

sys.path.append("../lib")       # for params

import re, socket, params, os

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

sock, addr = lsock.accept()

print("connection rec'd from", addr)


from framedSock import framedSend, framedReceive

b =True
while b:
    payload = framedReceive(sock, debug)
    if debug: print("rec'd: ", payload)
    if not payload:
        break
       # make emphatic
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
        while True:
           run = getruns.read(100)
           print("sending ", run.decode('utf-8'))
           sock.send(run)
           print("sent " + run.decode('utf-8'))
           if not run:
                 print("Done")
                 break
        getruns.close()
        b = False
