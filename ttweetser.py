####################################################################################################################################
#Information
##
##Names: Cody Kantor, Mark Mossien
##Class: CS 3251 - Networking I
##Date: 11/11/2020
##Assignment: Programming Assignment 2
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
subs = [] #initialize lists for tweets, subs and users
users = []
ThreadCount = 0  ## Initialize ThreadCount

def multi_threaded_client(connection): #function for each new thread
    while True: #repeat indefinitely:
        data = connection.recv(2048) #receive data from client
        unsplitdata = data.decode()
        if not unsplitdata:
            break
                
        if "\"" in unsplitdata: 
            data = unsplitdata.split("\"")
            data = [d.strip() for d in data]
            data0 = data[0].split()[0]
            data1 = data[0].split()[1]         #this section parses the code into a list of data[] so that
            data.append(data[2])               #the client's commands can be more easily parsed later in the function.
            origintag = data[3]                #only run this section if the unparsed data has quotes; so, essentially,
            data[3] = data[3].split("#")       #only when the client's command is a tweet.
            data[3].remove("")
            data[2] = data[1]
            data[1] = data1
            data[0] = data0
        else:
            data = unsplitdata.split() #if not tweet, then just split by space.
        
        data[1] = data[1].strip(":")
        
        if (data[1] == "timeline"): #if the command is timeline,
            connection.send(("Timeline:").encode()) #send this info to the client, and let client handle.

        if (data[1] == "getusers"): #if the command is getusers,
            userlist = ""
            for user in users: #generate a user list from the server userlist.
                userlist = userlist + user + "\n"
            connection.send(userlist.strip().encode()) #send this info to the client.
        
        if(data[1] == "exit"): #if the command is exit, then clear out the server lists.
            for tweet in tweets: #clear the user's tweets,
                if data[0] == tweet.get("user"):
                    tweets.remove(tweet)
            for sub in subs:     #clear the user's subs,
                if data[0] == sub.get("user"):
                    subs.remove(sub)
            for user in users:   #and clear the user.
                if data[0] == user:
                    users.remove(user)
            break
        
        if (data[1] == "tweet"): #if the command is tweet
            tweets.append({'user': data[0], 'msg': data[2], 'tag': origintag}) #save the tweet
            subber = ""
            for sub in subs: #search through the list of subs to see which clients to push the tweet to.
                if ((sub.get("tag") == "ALL" or sub.get("tag") in data[3]) and subber != sub.get("user")):
                    subber = sub.get("user")     #push the tweet to the client if they are subbed to the hashtag.
                    sub.get('client').send((data[0]+": "+'"'+data[2]+'" '+origintag).encode())
        
        if (data[1] == "subscribe"): #if the command is subscribe
            subs.append({'user': data[0], 'tag': data[2].strip("#"), 'client': connection}) #add the hashtag to that user's list of subs.
            connection.send(("operation success").encode()) #then send success message to the client
        
        if (data[1] == "unsubscribe"): #if the command is unsubscribe
            if (data[2] == "#ALL"): #if unsubscribing from all hashtags,
                for sub in subs:
                    if (data[0] == sub.get("user")): #then remove all of the subs for that user.
                        subs.remove(sub)
                for sub in subs:
                    if (data[0] == sub.get("user")):
                        subs.remove(sub)
            else: 
                for sub in subs: #otherwise, find the specific sub for that user, and unsubscribe from just that hashtag.
                    if ((data[2].strip("#") == sub.get("tag") or data[2].strip("#") == "ALL") and data[0] == sub.get("user")):
                        subs.remove(sub)
            connection.send(("operation success").encode()) #then send success message to the client
        
        if (data[0] == "gettweets"): #if command is gettweets
            tweetlist = ""
            for tweet in tweets: #find all of the corresponding tweets to the called user, and add them to a list.
                if data[1] == tweet.get("user"):
                    tweetlist = tweetlist+tweet.get("user")+': "'+tweet.get("msg")+'" '+tweet.get("tag")+"\n"

            if not (data[1] in users): #if the user isn't found in the userlist, then there is nothing to display.
                connection.send(("no user "+data[1]+" in the system").encode()) #let user know
            else: #otherwise, send the user the tweet list for the desired user.
                connection.send((tweetlist.strip()+"*").encode())
        
    connection.close() #after the function exists, close the connection.

while True: ## while True will run forever without crashing
    conn, addr = s.accept() ## Accept socket connection
    print('Connected by', addr) ## Print connection information
    
    name = conn.recv(1024) #receive username information from the client
    name = name.decode()
    validName = True
    for u in users:
        if u == name:   #makes sure that the desired username is not already in use
            validName = False  #duplicate username check
            break

    if (validName): #if the username is valid, then add to the user list and begin a new thread for the corresponding client.
        users.append(name)
        #print("successfully accepted user", name)
        conn.send("True".encode()) #lets client know that the username was valid
        start_new_thread(multi_threaded_client, (conn, )) #starts a new thread for the client
        ThreadCount = ThreadCount + 1 #increment threadcount
    else: #otherwise, let the user know that the username was not valid.
        conn.send("False".encode())
        conn.close() #close the connection.
s.close() #closes the socket.

####################################################################################################################################
#Citation of External References and Templates Used
##
##Real Python's Socket Programming in Python Guide: https://realpython.com/python-sockets/
##Python Module of the Week's TCP/IP Client and Server Page: https://pymotw.com/2/socket/tcp.html
##Geeks for Geeks' Socket Programming in Python: https://www.geeksforgeeks.org/socket-programming-python/
##Python Documentation's Socket Programming HOWTO: https://docs.python.org/2/howto/sockets.html
####################################################################################################################################