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

    
while 1:
    c = input("filename\n")
    command = c.encode('utf-8')
    s.send(command)
    cl = c.split(" ")
    data = s.recv(1024) #recieve the number of 100 byte messages needed
    count = data.decode('utf-8')
    writer = open("from-server" + cl[1], 'wb') #says "from server" to keep track when done
    while count  >= 0:
        filedata = s.recv(100)
        d = writer.write(filedata)
        count = count - 1        
    writer.close()
    print(done)
    sys.exit()
        
#print("sending hello world")
#framedSend(s, b"hello world", debug)
#print("received:", framedReceive(s, debug))

#print("sending hello world")
#framedSend(s, b"hello world", debug)
#print("received:", framedReceive(s, debug))

