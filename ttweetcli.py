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

def invaliduser(string): #given a string for the username, determines whether/not it is legal.
    if string == "":
        return True
    for s in string:
        val = ord(s)    #name is invalid if it contains any character not in [A-Z, a-z, 0-9]
        if (val < 48 or (val > 57 and val < 65) or (val > 90 and val < 97) or (val > 122)):
            return True
    return False

def invalidhashtag(string):  #given a string for the hashtag, determines whether/not it is legal.
    if (string[0] != "#" or "##" in string or string == "#ALL"):
        return True    #basic cases for validity

    for s in string:
        val = ord(s)    #tests for invalid characters not in [A-Z, a-z, 0-9]
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

s.send((params["user"]).encode()) #after performing all other input checks, send username to server to see if it is already in use.
validUsername = s.recv(2048).decode() #if it is in use, then the server will determine this and send back "False".
if (validUsername == "False"):   #let user know it's invalid and gracefully exit
    print("username illegal, connection refused.")
    exit() 

print("username legal, connection established.")

def sending():
    mysubs = [] #for storing a client's subscribed tweets    
    
    while True: #repeats until the user wishes to exit

        Input = str(input()) #gets the user's input command
        if "\"" in Input: #if there are quotes in the input that means we need to split by quote to properly save the tweet.
            cmd = Input.split("\"")    #split by quote,
            cmd = [c.strip() for c in cmd]  #and remove trailing whitespace
            if (Input.split("\"")[1].isspace()):
                cmd[1] = Input.split("\"")[1]
        else:
            cmd = Input.split() #otherwise, if there are no quotes then just split the input up into distinct words
        
        t2 = 0 #initialization for receiving thread
        
        #at this point, cmd[0] contains the main command; i.e. tweet, getusers, etc.
        
        if (cmd[0] == "exit"): #if the command is exit:
            s.send((params["user"]+" "+Input).encode()) #send the server a message to inform which user, and that the user is exiting.
            break ## exit gracefully
        
        t2 = threading.Thread(target=receiving) #begin the receiving thread, to form other half of send/receive threading per client
        t2.start()   #begin thread activity

        if (cmd[0] == "tweet"): #if command is tweet
            if ((len(cmd[1]) <= 0) and (not cmd[1].isspace())): #check not empty
                print("message format illegal") #let user know otherwise
                continue ## exit gracefully
            if (len(cmd[1]) > 150): #make sure the tweet isnt too long
                print("message length illegal, connection refused.") #let user know if so
                continue ## exit gracefully
            if (invalidhashtag(cmd[2]) or cmd[2] == "#ALL"): #if the hashtag is invalid (based on method above)
                print("hashtag illegal format, connection refused.") #let user know
                continue ## exits gracefully
            s.send((params["user"]+" "+cmd[0] + ': "' + cmd[1] + '" ' + cmd[2]).encode()) #at this point the tweet is valid, so send it to the server,
            continue                                                                    #along with the user that it originated from.
        
        if (cmd[0] == "subscribe"): #if command is subscribe
            if(len(mysubs) == 3 or cmd[1] in mysubs): #if already subscribed or too many subscriptions:
                print("operation failed: sub " + cmd[1] + " failed, already exists or exceeds 3 limitation") #let user know.
                continue ## exits gracefully
            mysubs.append(cmd[1]) #add the sub to the subs list, since it is valid.
            s.send((params["user"] + " " + Input).encode()) #send this information to the server.
        
        if (cmd[0] == "unsubscribe"): #if command is unsubscribe
            if(cmd[1] == "#ALL"): #if all, then reset the subs list.
                mysubs = []
            for subs in mysubs: #if not all, then search through the subs list to find correct one to
                if subs == cmd[1]:              #unsubscribe to
                    mysubs.remove(subs) #remove it
            s.send((params["user"] + " " + Input).encode()) #send this information to the server.
        
        if (cmd[0] == "getusers"): #if command is getusers
            s.send((params["user"]+" "+Input).encode()) #send this information to the server.
            
        if (cmd[0] == "gettweets"):#if command is gettweets
            s.send(Input.encode()) #send this information to the server.
        
        if (cmd[0] == "timeline"): #if command is timeline
            s.send((params["user"]+" "+Input).encode()) #send this information to the server
        #repeat back until the user is done.
            
    print("bye bye".strip())
    s.close() #close the current client connection, and exit.
    sys.exit()  #shouting

def receiving(): #code for the receiving thread for the current client
    while True:
        try: #the socket might have been closed, in which case jump to the except and exit.
            if s: #if the socket still exists while listening (aka the connection is still open)
                res = s.recv(2048) #accept data from the server for parsing
                res = res.decode()
                if len(res) == 0: #ignore if no data
                    pass
                if (": " in res and res[0] != "G"):
                    tl.append(res) #for gettweets; add the tweetlist for display.
                if (res[0] == "G"):
                    res = res[1:]
                if (res == "Timeline:"):
                    for post in tl: #if timeline, then display everything in t1,
                        print(post)
                else: #otherwise just print the tweetlist.
                    print(res)
        except:
            sys.exit() #if the socket is closed, then exit the program.



t1 = threading.Thread(target=sending) #initializes and starts the sending thread for the calling client.
t1.start()    #each client will have two threads associated with it.



####################################################################################################################################
#Citation of External References and Templates Used
##
##Real Python's Socket Programming in Python Guide: https://realpython.com/python-sockets/
##Python Module of the Week's TCP/IP Client and Server Page: https://pymotw.com/2/socket/tcp.html
##Geeks for Geeks' Socket Programming in Python: https://www.geeksforgeeks.org/socket-programming-python/
##Python Documentation's Socket Programming HOWTO: https://docs.python.org/2/howto/sockets.html
####################################################################################################################################