# Simple File Transfer

### Intoduction

This file transfer protocol is client and server based. The client will request a file from the server and the server will send the file 100 bytes at a time. The program uses TCP in order to conduct it's file transfer.

### Running
In order to run the program you must have framedSock.py file and the lib directory availabe to the client and server programs.

There are two server types, one is a server.py this program handles one client strictly. The other framedForkServer.py will handle multiple clients by forking.