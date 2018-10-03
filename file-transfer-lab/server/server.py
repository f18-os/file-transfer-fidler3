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

#while True:
#    payload = framedReceive(sock, debug)
#    if debug: print("rec'd: ", payload)
#    if not payload:
#        break
#    payload += b"!"             # make emphatic!
#    framedSend(sock, payload, debug)

while True:
    message = sock.recv(1024)
    if os.path.isfile(message[1]):
        size = os.stat(message[1])
        size = size.st_size
        count = int(size/100)+1 #number of messages plus one for expected remainder bytes
        print (str(count) + "messages") # for debugging
        count = size.encode('utf-8')
        sock.send(count)
        getruns = open(message[1], "rb")
        while count >= 0:
           run = getruns.read(100)
           sock.send(run)
           count = count - 1
    print("Done")

        
    
