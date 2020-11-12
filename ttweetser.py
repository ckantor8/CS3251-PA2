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
import os
import _thread
import threading
from _thread import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) ## Initialize socket
HOST = ''             ## Symbolic name meaning the local host
PORT = (int)(sys.argv[1])      ##Retrive port provided as terminal argument

try:
    s.bind((HOST, PORT)) ## Bind socket
except socket.error as e:
    print(str(e))
    
print("Waiting for connection...") ## Print waiting for connection message to update user with status
s.listen(5) ## Set socket to listen for connection

tweets = []
subs = []
users = []
ThreadCount = 0          ## Initialize ThreadCount

def multi_threaded_client(connection):
    while True:
        data = connection.recv(2048)
        unsplitdata = data.decode()
        if not unsplitdata:
            break
        
        #print("data received by the server is ", unsplitdata)
        
        if "\"" in unsplitdata:
            data = unsplitdata.split("\"")
            data = [d.strip() for d in data]
            data0 = data[0].split()[0]
            data1 = data[0].split()[1]
            data.append(data[2])
            origintag = data[3]
            data[3] = data[3].split("#")
            data[3].remove("")
            data[2] = data[1]
            data[1] = data1
            data[0] = data0
        else:
            data = unsplitdata.split()
        
        data[1] = data[1].strip(":")
        
        if (data[1] == "timeline"):
            connection.send(("Timeline:").encode())

        if (data[1] == "getusers"):
            userlist = ""
            for user in users:
                userlist = userlist + user + "\n"
            connection.send(userlist.strip().encode())
        
        if(data[1] == "exit"):
            for tweet in tweets:
                if data[0] == tweet.get("user"):
                    tweets.remove(tweet)
            for sub in subs:
                if data[0] == sub.get("user"):
                    subs.remove(sub)
            for user in users:
                if data[0] == user:
                    users.remove(user)
            break
        
        if (data[1] == "tweet"):
            tweets.append({'user': data[0], 'msg': data[2], 'tag': origintag})
            subber = ""
            for sub in subs:
                if ((sub.get("tag") == "ALL" or sub.get("tag") in data[3]) and subber != sub.get("user")):
                    subber = sub.get("user")
                    sub.get('client').send((data[0]+": "+'"'+data[2]+'" '+origintag).encode())
            connection.send(("tweet operation success").encode())
        
        if (data[1] == "subscribe"):
            subs.append({'user': data[0], 'tag': data[2].strip("#"), 'client': connection})
            connection.send(("subscribe operation success").encode())
        
        if (data[1] == "unsubscribe"):
            if (data[2] == "#ALL"):
                for sub in subs:
                    if (data[0] == sub.get("user")):
                        subs.remove(sub)
                for sub in subs:
                    if (data[0] == sub.get("user")):
                        subs.remove(sub)
            else:
                for sub in subs:
                    if ((data[2].strip("#") == sub.get("tag") or data[2].strip("#") == "ALL") and data[0] == sub.get("user")):
                        subs.remove(sub)
            connection.send(("unsubscribe operation success").encode())
        
        if (data[0] == "gettweets"):
            tweetlist = ""
            for tweet in tweets:
                if data[1] == tweet.get("user"):
                    tweetlist = tweetlist+tweet.get("user")+': "'+tweet.get("msg")+'" '+tweet.get("tag")+"\n"

            if not (data[1] in users):
                connection.send(("no user "+data[1]+" in the system").encode())
            else:
                connection.send((tweetlist.strip()+"*").encode())
        
    connection.close()

while True: ## while True will run forever without crashing
    conn, addr = s.accept() ## Accept socket connection
    print('Connected by', addr) ## Print connection information
    
    name = conn.recv(1024)
    name = name.decode()
    validName = True
    for u in users:
    	if u == name:
    		validName = False             #duplicate username check
    		break

    if (validName):
    	users.append(name)
    	#print("successfully accepted user", name)
    	conn.send("True".encode())
    	start_new_thread(multi_threaded_client, (conn, ))
    	ThreadCount = ThreadCount + 1
    else:
    	conn.send("False".encode())
    	conn.close()
s.close()

####################################################################################################################################
#Citation of External References and Templates Used
##
##Real Python's Socket Programming in Python Guide: https://realpython.com/python-sockets/
##Python Module of the Week's TCP/IP Client and Server Page: https://pymotw.com/2/socket/tcp.html
##Geeks for Geeks' Socket Programming in Python: https://www.geeksforgeeks.org/socket-programming-python/
##Python Documentation's Socket Programming HOWTO: https://docs.python.org/2/howto/sockets.html
####################################################################################################################################