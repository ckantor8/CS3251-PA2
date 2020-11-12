####################################################################################################################################
#Information
##
##Name: Cody Kantor
##GTID: 903412020
##E-mail: ckantor8@gatech.edu
##Class: CS 3251 - Networking I
##Date: 9/22/2020
##Assignment: Programming Assignment 1 - Trivial Twitter
####################################################################################################################################

## Necessary imports for socket programming and using terminal arguments
import socket
import sys

HOST = ''             ## Symbolic name meaning the local host
PORT = (int)(sys.argv[1])      ##Retrive port provided as terminal argument
message = ""          ## Initialize message
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) ## Initialize socket
s.bind((HOST, PORT)) ## Bind socket
s.listen(1) ## Set socket to listen for connection
print("Waiting for connection...") ## Print waiting for connection message to update user with status
while True: ## while True will run forever without crashing
    try:
        conn, addr = s.accept() ## Accept socket connection
        print 'Connected by', addr ## Print connection information
        data = conn.recv(1024) ## Receive data sent from client through connection
        if(data != "-d"): ## If the data received is not -d, it must be -u for upload (thanks to client-side argument handling)
            conn.send(data) ## Since flag is -u, just send the uploaded message right back to client for confirmation
            message = data ## Set message variable to the last uploaded message
        if(data == "-d"): ## If the data is -d, then download has been chosen
            if (message == ""): ## Check if message is empty
                conn.send("Empty Message") ## If message is empty, send "Empty Message" back to client
            else: ## Message is not empty
                conn.send(message) ## Since message isn't empty, send last uploaded message back to client
    except KeyboardInterrupt: ## Check for Keyboard interrupt
        print("Keyboard Interrupt Used to Close Server") ## Print statement
        s.close() ## Close socket
        conn.close() ## Close connection
        exit() ## Exit program
    finally: ## Assure that we close the connection either way
        conn.close() ##Close connection

####################################################################################################################################
#Citation of External References and Templates Used
##
##Real Python's Socket Programming in Python Guide: https://realpython.com/python-sockets/
##Python Module of the Week's TCP/IP Client and Server Page: https://pymotw.com/2/socket/tcp.html
##Geeks for Geeks' Socket Programming in Python: https://www.geeksforgeeks.org/socket-programming-python/
##Python Documentation's Socket Programming HOWTO: https://docs.python.org/2/howto/sockets.html
####################################################################################################################################
