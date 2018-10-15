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

def receive():
    take = framedReceive(sock, debug)
    print(take)
    f = take.decode('utf-8')
    if os.path.isfile(f):
        print("This file already exists in directory")
        sock.send(b'wrrong')
        sys.exit(0)
    else:
        framedSend(sock, b'begin', debug)
        #txtfile = f.encode('utf-8')
       #framedSend(sock, txtfile, debug)
        txtfile = f
    with open("copy " + txtfile, 'wb') as r:
        while True:
            a = sock.recv(100)
            if a == b'LETSGO':
                continue #lets begin reading file
            elif a == b'TDBABY':
                print("Done writing")
                break
            elif a == b'WRONG': #wrong and tdbaby serve the similar purposes, but are different
                print("File does not exist exiting")
                break
            else:
               # print(a.decode('utf-8'))
                r.write(a)
        r.close()
        print("All done")
        sock.close()

def send():
     payload = framedReceive(sock, debug)
     if debug: print("rec'd: ", payload)
     payload = payload.decode('utf-8')
     print("sending " + payload)
     if os.path.isfile(payload):
         getruns = open(payload, "rb") #open file for reading bytes
         sock.send(b'LETSGO') #Lets drive this file to the end zone.. football references
         while True:
             run = getruns.read(100)
             sock.send(run)
             print("sent ") #sent 100 bytes
             if not run:
                 print("Done")
                 break
             sock.send(b'TDBABY') #Touchdown you're done
             getruns.close()
             sys.exit(0)
     else:
         print("File does not exist informing client and  exiting program")
         sock.send(b'WRONG')
         sys.exit(0)
    
while True:
    sock, addr = lsock.accept()

    from framedSock import framedSend, framedReceive

    if not os.fork():
        print("new child process handling connection from", addr)
        while True:
            command = sock.recv(4) #4 bytes for PUTS or GETS
            print(command)
            if command == b'PUTS':
                receive()
                sock.close()
            elif command == b'GETS':
                send()
           # payload = framedReceive(sock, debug)
           # if debug: print("rec'd: ", payload)
           # if not payload:
           #     break
           # payload = payload.decode('utf-8')
           # print("sending " + payload)
           # if os.path.isfile(payload):
           #     getruns = open(payload, "rb") #open file for reading bytes
           #     sock.send(b'LETSGO') #Lets drive this file to the end zone.. football references
           #     while True:
           #         run = getruns.read(100)
           #         sock.send(run)
           #         print("sent ") #sent 100 bytes
           #         if not run:
           #             print("Done")
           #             break
           #     sock.send(b'TDBABY') #Touchdown you're done
           #     getruns.close()
           #     sys.exit(0)
            else:
                print("Not a good command")
                sys.exit(0)
                break;
            sys.exit(0)
