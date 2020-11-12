README

CS3251 Fall 2020 - Programming Assignment 2 - Advanced Twitter Application

November 11th, 2020

This project was completed by Cody Kantor and Mark Mossien.

The main ideas behind implementation here were to build upon the basic structure of the first programming assignment to 
include support for multiple clients through multi-threading, and adding additionally tweeting functionalities. 
Initially, we used a basic multi-threading client-server setup where each client-server connection had 1 thread, but further into
working on the project this was changed so that each client had two threads: one for sending, and one for receiving. This change
was made upon the realization that the current setup we had did not allow for the server to push tweets to multiple subscribed clients.

Cody got the project off the ground running, implementing first in the client program the user input validation
for the IP address, port, and username. He implemented the initial TCP socket connection and user command parsing along with
the server, and fleshed out more than half of the possible user-server commands. He also initialized the server side TCP socket 
connection, and ensured that the basic client-server interactions were working successfully. Further along in the project, Cody 
performed further modifications of the initial multi-threaded framework that we had in our project, and was able to make user-server
commands work successfully for multiple clients.

Mark took Cody's initial frameworks and built upon them and debugged them. Initially the username input for the project allowed for
any sort of characters within usernames and hashtags. He fixed some issues with user input validation, and enhanced the initial 
multithreaded structure that Cody presented. He also performed some changes on the structure of message sending back and forth
between the client and server, and towards the completion of the project, Mark was able to fix a bug related to the user exit command 
that led to erroneous outputs on the client side.

To run our code, no dependent packages or special instructions are needed. Upon navigating to the executables' location, you can test our
project by performing the following:

      for ttweetser.py:   python ttweetser.py [port]

      for ttweetcli.py:   python ttweetcli.py [ip] [port] [username]

	ex:
	in 1st command line window: python ttweetser.py 10000
	in 2nd command line window: python ttweetcli.py 143.215.142.530 10000
                  ....


                       





