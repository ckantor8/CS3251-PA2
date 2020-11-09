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

# Function checks if the string 
# contains any special character 
def invaliduser(string): 
  
    # Make own character set and pass  
    # this as argument in compile method 
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]') 
      
    # Pass the string in search  
    # method of regex object.     
    if(regex.search(string) == None): 
        return True
          
    else: 
        return False
    
def invalidhashtag(string): 
  
    # Make own character set and pass  
    # this as argument in compile method 
    regex = re.compile('[@_!$%^&*()<>?/\|}{~:]') 
      
    # Pass the string in search  
    # method of regex object.     
    if(regex.search(string) == None): 
        return True
          
    else: 
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
    print("user = ",params["user"])
    if (params["ip"] < "0.0.0.0" or params["ip"] > "255.255.255.255"): ## Check if IP is valid
        print("error: server ip invalid, connection refused.") ## Provide error statement
        exit() ## Exit gracefully
    if (params["port"] < "1" or params["port"] > "65535"):
        print("error: server port invalid, connection refused.")
        exit() ## exit gracefully
    if not (invaliduser(params["user"])):
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

print("username legal, connection established.")
##res = s.recv(1024)
mysubs = []
while True:
    print('$ ')
    Input = raw_input()
    if "\"" in Input:
        cmd = Input.split("\"")
        cmd = [c.strip() for c in cmd]
    else:
        cmd = Input.split()
        
    if (cmd[0] == "tweet"):
        if (len(cmd[1]) <= 0):
            print("message format illegal")
            exit() ## exit gracefully
        if (len(cmd[1]) > 150):
            print("message length illegal, connection refused.")
            exit() ## exit gracefully
        if (cmd[2][0] != '#' or not invalidhashtag(cmd[2]) or "##" in cmd[2] or cmd[2] == "#ALL"):
            print("hashtag illegal format, connection refused.")
            exit() ## exits gracefully
        s.send(params["user"]+" "+cmd[0]+" "+cmd[1]+" "+cmd[2])
        res = s.recv(1024)
        print(res)
        if cmd[2] in mysubs:
            res = s.recv(1024)
            print(res)
        continue
    
    if (cmd[0] == "subscribe"):
        if(len(mysubs) == 3 or cmd[1] in mysubs):
            print("operation failed: sub " + cmd[1] + " failed, already exists or exceeds 3 limitation")
            exit() ## exits gracefully
        mysubs.append(cmd[1])
        s.send((params["user"] + " " + Input))
        res = s.recv(1024)
        print(res)
    
    if (cmd[0] == "unsubscribe"):
        if(cmd[1] == "#ALL"):
            mysubs = []
        for subs in mysubs:
            if subs == cmd[1]:
                mysubs.remove(subs)
        s.send((params["user"] + " " + Input))
        res = s.recv(1024)
        print(res)
    
    if (cmd[0] == "getusers"):
        s.send(str.encode(Input))
        res = s.recv(1024)
        
    if (cmd[0] == "gettweets"):
        s.send(str.encode(Input))
        res = s.recv(1024)
        
    if (cmd[0] == "exit"):
        s.send(Input)
        print("bye bye")
        exit() ## exit gracefully
    
s.close()

####################################################################################################################################
#Citation of External References and Templates Used
##
##Real Python's Socket Programming in Python Guide: https://realpython.com/python-sockets/
##Python Module of the Week's TCP/IP Client and Server Page: https://pymotw.com/2/socket/tcp.html
##Geeks for Geeks' Socket Programming in Python: https://www.geeksforgeeks.org/socket-programming-python/
##Python Documentation's Socket Programming HOWTO: https://docs.python.org/2/howto/sockets.html
####################################################################################################################################