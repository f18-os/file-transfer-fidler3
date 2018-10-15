#! /usr/bin/env python3

# Echo client program
import socket, sys, re, os

sys.path.append("../lib")       # for params
import params

from framedSock import framedSend, framedReceive


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

    
#print("sending hello world")

def puts(c):
    
        s.send(b'PUTS')
        #f = input("Enter file to put in server")
        txtfile = c[1].encode('utf-8')
        framedSend(s, txtfile, debug)
        message = framedReceive(s, debug)
        if message == b'begin':
            getruns = open(c[1], "rb") #open file for reading bytes
            s.send(b'LETSGO') #Lets drive this file to the end zone.. football references
            while True:
                run = getruns.read(100)
                s.send(run)
                print("sent ") #sent 100 bytes
                if not run:
                    print("Done")
                    #s.shutdown(socket.SHUT_WR)
                    #s.send(b'TDBABY')
                    break
            s.send(b'TDBABY') #Touchdown you're done
            getruns.close()
            s.close()
        else:
            print("File already exists in server")
            s.close()


def get(f):
    s.send(b'GETS')
    check = True
    while check:
        #f = input("Enter filename to get from server\n")
        if os.path.isfile(f):
            print("This file already exists in directory")
        else:
            check = False
            txtfile = f.encode('utf-8')
            framedSend(s, txtfile, debug)
            txtfile = f

            
    with open("copy " + txtfile, 'wb') as r:
        while True:
            input = s.recv(100)
            if input == b'LETSGO':
                continue #lets begin reading file
            elif input == b'TDBABY':
                print("Done writing")
                break
            elif input == b'WRONG': #wrong and tdbaby serve the similar purposes, but are different
                print("File does not exist exiting")
                break
            else:
                r.write(input)
        r.close()
        print("All done")
        s.close()

while True:
    command = input("put or get <filename>")
    c = command.split()
    print(c)
    filename = c[1]
    if c[0] == "put":
        puts(c)
    elif c[0] == "get":
        get(c)
    else:
        print("Incorrect command")
#print("received:", framedReceive(s, debug))





#print("sending hello world")
#framedSend(s, b"hello world", debug)
#print("received:", framedReceive(s, debug))

