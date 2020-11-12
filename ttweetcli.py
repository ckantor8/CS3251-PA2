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
import re
import threading
import _thread
from _thread import *

tl = []

def invaliduser(string): 
    if string == "":
        return True
    for s in string:
        val = ord(s)
        if (val < 48 or (val > 57 and val < 65) or (val > 90 and val < 97) or (val > 122)):
            return True
    return False

def invalidhashtag(string): 
    if (string[0] != "#" or "##" in string or string == "#ALL"):
        return True

    for s in string:
        val = ord(s)
        if (val < 48 or (val > 57 and val < 65) or (val > 90 and val < 97) or (val > 122)):
            if (val != 35):
                return True
    return False


args = sys.argv ## Retrieve arguments passed to terminal
numArgs = len(sys.argv) ## Acquire number of arguments passed

## Verify and Handle Number of Args
if numArgs < 4: ## Too few arguments
    print("error: args should contain <ServerIP> <ServerPort> <Username>") ## Provide error statement
    exit() ## exit gracefully

if numArgs > 4: ## Too many arguments
    print("error: args should contain <ServerIP> <ServerPort> <Username>") ## Provide error statement
    exit() ## exit gracefully
    
if (numArgs == 4): ## No message included, so flag should should be -d
    params = {"ip": args[1], "port": args[2], "user": args[3],} ## Enumerate arguments as parameters
    if (params["ip"] < "0.0.0.0" or params["ip"] > "255.255.255.255"): ## Check if IP is valid
        print("error: server ip invalid, connection refused.") ## Provide error statement
        exit() ## Exit gracefully
    if (params["port"] < "1" or params["port"] > "65535"):
        print("error: server port invalid, connection refused.")
        exit() ## exit gracefully
    if (invaliduser(params["user"])):
        print("error: username has wrong format, connection refused.")
        exit() ## exit gracefully

HOST = params["ip"]    ## Retrieve provided IP
PORT = (int)(params["port"])  ## Retrieve provided port (should be same as server)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) ## Initialize socket
try: ## Wrap connect in try block in case of connection error
    s.connect((HOST, PORT)) ## Connect socket
except: ## If connection fails, go to exception handler
    print("Error: Server Not Found") ## Provide error statement
    exit() ## Exit gracefully

s.send((params["user"]).encode())
validUsername = s.recv(1024).decode()
if (validUsername == "False"):
    print("username illegal, connection refused.")
    exit()

print("username legal, connection established.")

def sending():
    mysubs = []
    
    
    while True:

        Input = str(input())
        if "\"" in Input:
            cmd = Input.split("\"")
            cmd = [c.strip() for c in cmd]
        else:
            cmd = Input.split()
                
        t2 = 0
        
        if (cmd[0] == "exit"):
            s.send((params["user"]+" "+Input).encode())
            break ## exit gracefully
        
        t2 = threading.Thread(target=receiving)
        t2.start()

        if (cmd[0] == "tweet"):
            if (len(cmd[1]) <= 0):
                print("message format illegal")
                continue ## exit gracefully
            if (len(cmd[1]) > 150):
                print("message length illegal, connection refused.")
                continue ## exit gracefully
            if (invalidhashtag(cmd[2]) or cmd[2] == "#ALL"):
                print("hashtag illegal format, connection refused.")
                continue ## exits gracefully
            s.send((params["user"]+" "+cmd[0] + ': "' + cmd[1] + '" ' + cmd[2]).encode())
            continue
        
        if (cmd[0] == "subscribe"):
            if(len(mysubs) == 3 or cmd[1] in mysubs):
                print("operation failed: sub " + cmd[1] + " failed, already exists or exceeds 3 limitation")
                continue ## exits gracefully
            mysubs.append(cmd[1])
            s.send((params["user"] + " " + Input).encode())
        
        if (cmd[0] == "unsubscribe"):
            if(cmd[1] == "#ALL"):
                mysubs = []
            for subs in mysubs:
                if subs == cmd[1]:
                    mysubs.remove(subs)
            s.send((params["user"] + " " + Input).encode())
        
        if (cmd[0] == "getusers"):
            s.send((params["user"]+" "+Input).encode())
            
        if (cmd[0] == "gettweets"):
            s.send(Input.encode())
        
        if (cmd[0] == "timeline"):
            s.send((params["user"]+" "+Input).encode())
            
    print("bye bye")
    s.close()
    sys.exit()  #shouting

def receiving(): #listening
    while True:
        try:
            if s:
                res = s.recv(1024)
                res = res.decode()
                if (": " in res and "*" not in res):
                    tl.append(res)
                if len(res) == 0:
                    pass
                if "*" in res:
                    res = res.strip("*")
                if (res == "Timeline:"):
                    for post in tl:
                        print(post)
                else:
                    print(res)
        except:
            sys.exit()



t1 = threading.Thread(target=sending)
t1.start()



####################################################################################################################################
#Citation of External References and Templates Used
##
##Real Python's Socket Programming in Python Guide: https://realpython.com/python-sockets/
##Python Module of the Week's TCP/IP Client and Server Page: https://pymotw.com/2/socket/tcp.html
##Geeks for Geeks' Socket Programming in Python: https://www.geeksforgeeks.org/socket-programming-python/
##Python Documentation's Socket Programming HOWTO: https://docs.python.org/2/howto/sockets.html
####################################################################################################################################