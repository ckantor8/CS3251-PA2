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

args = sys.argv ## Retrieve arguments passed to terminal
numArgs = len(sys.argv) ## Acquire number of arguments passed

## Verify and Handle Number of Args
if numArgs < 4: ## Too few arguments
    print("Error: Invalid Number of Parameters (Too Few)") ## Provide error statement
    exit() ## exit gracefully
    
if (numArgs == 4): ## No message included, so flag should should be -d
    params = {"flag": args[1], "ip": args[2], "port": args[3],} ## Enumerate arguments as parameters
    if (params["flag"] == "-u"): ## Check if upload flag is used without message
        print("Error: No Message Inputted") ## Provide error statement
        exit() ## Exit gracefully

if numArgs == 5: ## Message included, so flag should be -u
    params = {"flag": args[1], "ip": args[2], "port": args[3], "message": args[4]} ## Enumerate arguments as parameters
    if len(params["message"]) > 150: ## check if message length exceeds 150 characters
        print("Error: Message exceeds 150 characters.") ## If message limit is exceeded, provide error statement
        exit() ## exit gracefully

if numArgs > 5: ##Too many arguments
    print("Error: Invalid Number of Parameters (Too Many)") ## Provide error statement
    exit() ## exit gracefully

if ((params["flag"] != "-d") & (params["flag"] != "-u")): ## Check if flag is not valid
    print("Error: Invalid flag -- Use -u for upload or -d for download") ## Provide error statement if flag is invalid
    exit() ## exit gracefully

HOST = params["ip"]    ## Retrieve provided IP
PORT = (int)(params["port"])  ## Retrieve provided port (should be same as server)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) ## Initialize socket
try: ## Wrap connect in try block in case of connection error
    s.connect((HOST, PORT)) ## Connect socket
except: ## If connection fails, go to exception handler
    print("Error: Server Not Found") ## Provide error statement
    exit() ## Exit gracefully
if params["flag"] == "-u": ## Check if flag is -u for uploading
    s.send(params["message"]) ## Since upload flag was used, send message to server
    print 'Upload of Message "',str(s.recv(1024)),'" successful' ## Retrieve message from server to print successful upload confirmation
    s.close() ## Close connection now
if params["flag"] == "-d": ## Check if flag is -d for downloading
    s.send(params["flag"]) ## Send flag to to server instead of message for server-side handling
    print "Last Message:", str(s.recv(1024)) ## Retrieve message from server to "download" and print Last Message
    s.close() ## Close connection now

####################################################################################################################################
#Citation of External References and Templates Used
##
##Real Python's Socket Programming in Python Guide: https://realpython.com/python-sockets/
##Python Module of the Week's TCP/IP Client and Server Page: https://pymotw.com/2/socket/tcp.html
##Geeks for Geeks' Socket Programming in Python: https://www.geeksforgeeks.org/socket-programming-python/
##Python Documentation's Socket Programming HOWTO: https://docs.python.org/2/howto/sockets.html
####################################################################################################################################