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
from _thread import *

import _thread
import threading

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
    ##connection.send(str.encode('Server is working:'))
    while True:
        data = connection.recv(2048)
        data = data.decode()
        if not data:
            break
        
        print("data received by the server is ", data)
        
        if (data.split()[1] == "timeline"):
            connection.send(("Timeline:\n").encode())

        if (data.split()[1] == "getusers"):
            userlist = ""
            for user in users:
                userlist = userlist + user + "\n"
            connection.send(userlist.encode())
        
        if(data.split()[1] == "exit"):
            for tweet in tweets:
                if data.split()[0] == tweet.get("user"):
                    tweets.remove(tweet)
            for sub in subs:
                if data.split()[0] == sub.get("user"):
                    subs.remove(sub)
            for user in users:
                if data.split()[0] == user:
                    users.remove(user)
            connection.send(("bye bye").encode())
            break
        
        if (data.split()[1] == "tweet"):
            #print('data.split()[1] is ', data.split()[1])
            tweets.append({'user': data.split()[0], 'msg': data.split()[2], 'tag': data.split()[3]})
            for sub in subs:
                tweetMessageToSend = ""
                for i in range(2, len(data.split()) - 1):
                    tweetMessageToSend += data.split()[i]
                    if (i != len(data.split()) - 2):
                        tweetMessageToSend += " "

                if (data.split()[len(data.split()) - 1] == sub.get("tag")):
                    sub.get('client').send((data.split()[0] + ': "' + tweetMessageToSend + '" ' + data.split()[len(data.split()) - 1]).encode())
                elif (sub.get("tag") == "#ALL"):
                    sub.get('client').send((data.split()[0]+': "'+data.split()[2]+'" '+data.split()[3]).encode())
            connection.send(("tweet operation success").encode())
        
        if (data.split()[1] == "subscribe"):
            subs.append({'user': data.split()[0], 'tag': data.split()[2], 'client': connection})
            connection.send(("subscribe operation success").encode())
        
        if (data.split()[1] == "unsubscribe"):
            for sub in subs:
                if data.split()[2] == sub.get("tag") and data.split()[0] == sub.get("user"):
                    subs.remove(sub)
            connection.send(("unsubscribe operation success").encode())
        
        if (data.split()[0] == "gettweets"):
            tweetlist = ""
            for tweet in tweets:
                if data.split()[1] == tweet.get("user"):
                    tweetlist = tweetlist+tweet.get("user")+': "'+tweet.get("msg")+'" '+tweet.get("tag")+"\n"
            
            userExists = False
            for u in users:
            	if u == data.split()[1]:
            		userExists = True
            		break

            if userExists == False:
                connection.send(("no user "+data.split()[1]+" in the system").encode())
            else:
                connection.send(tweetlist.encode())
        
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
    	print("successfully accepted user", name)
    	conn.send("True".encode())
    	start_new_thread(multi_threaded_client, (conn, ))
    	ThreadCount = ThreadCount + 1
    	#print('Thread Number: ' + str(ThreadCount))
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