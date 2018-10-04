# Simple File Transfer

### Intoduction

This file transfer protocol is client and server based. The client will request a file from the server and the server will send the file 100 bytes at a time. The program uses TCP in order to conduct it's file transfer.

### Running
In order to run the program you must have framedSock.py file and the lib directory availabe to the client and server programs.

There are two server types, one is a server.py this program handles one client strictly. The other framedForkServer.py will handle multiple clients by forking.

To test them have the server and client programs in different directories or folders. Then have a txt document availabe for transfer in the server directory. Run the server in one terminal first, then open a seperate terminal for the client. When running the client you will be prompted to enter the file you wish to "get" from the server.


