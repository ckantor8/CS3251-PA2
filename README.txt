README


Name: Cody Kantor
GTID: 903412020
E-mail: ckantor8@gatech.edu
Class: CS 3251 - Networking I
Date: 9/22/2020
Assignment: Programming Assignment 1 - Trivial Twitter

---------------------------------------------------------------------------------------------------------------

Assignment Description:
	In this application a ttweet server has room for exactly one message and is used by exactly one client.
	The client uploads a message to the server, then the same or another client downloads the message to read it.
	An uploaded message is stored at the server will overwrite an existing message if the server already has a message.
	A download request returns the last uploaded message or returns “Empty Message” if no message has been uploaded yet.
	The server is simple and can handle only one client at a time.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Files:

README.txt - Text file containing info regarding author, course, assignment, instructions for compiling & running, descriptions, etc.

Sample.txt - Text file containing sample output based on the provided test scenario (same output included below)

ttweetsrv.py - Python server file that takes a ServerPort as an argument and prints "Waiting for connection..." until the client connects when it then prints "Connected by <ConnectionAddress>"
	Note: On my local machine, Ctrl-C does not exit/quit/close/shutdown the program so you must use Ctrl-Break (via Ctrl-ScrollLock for my on-screen keyboard) but it does seem to work on the shuttle.

ttweetcl.py - Python client file that takes in a -u flag for uploading or a -d flag for downloading, a ServerIP, a ServerPort, and, if the flag is -u, a message to upload to the server.
	This will either return an error, "Upload of message " <message> " successful" (when uploading), or, when downloading, either "Last Message: <last message uploaded>" or
	"Last Message: Empty Message" if no message is currently uploaded.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Instructions:

	After saving both the server file and the client file in the same folder/directory,
	use a terminal to navigate to that directory and run the server file with the following command:
		$ python ttweetsrv.py <ServerPort>
	where <ServerPort> is replaced with whatever port you would like to run the server on.
	Next, open another terminal, navigate to the directory containing the files, and run the client file:
		$ python ttweetcl.py -u <ServerIP> <ServerPort> <message> 
		or
		$ python ttweetcl.py -d <ServerIP> <ServerPort>
	If you wish to upload a message to the server, use the -u flag and replace <ServerIP>
	with the IP address of the server in explicit dotted decimal notation, replace <ServerPort>
	with the port you ran the server on, and replace <message> with whatever message you wish to upload.
	In the event that your upload was successful a message stating so will appear; otherwise you will receive an error message indicating the error.
	If you wish to download a message from the server, use the -d flag and replace the Server fields the same way.
	This will return "Last Message: <last message uploaded>" or, if there is no message, "Last Message: Empty Message".

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Output Sample:

C:\Users\royal\OneDrive\Desktop\CS3251\PA1>python client.py -u localhost 12000 yes
Error: Server Not Found

C:\Users\royal\OneDrive\Desktop\CS3251\PA1>python client.py -d localhost 12000
Error: Server Not Found

C:\Users\royal\OneDrive\Desktop\CS3251\PA1>python server.py 12000
Waiting for connection...

C:\Users\royal\OneDrive\Desktop\CS3251\PA1>python client.py -d localhost 12000
Last Message: Empty Message

C:\Users\royal\OneDrive\Desktop\CS3251\PA1>python client.py -u localhost 12000 hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
Error: Message exceeds 150 characters.

C:\Users\royal\OneDrive\Desktop\CS3251\PA1>python client.py -d localhost 12000
Last Message: Empty Message

C:\Users\royal\OneDrive\Desktop\CS3251\PA1>python client.py -u localhost 12000 yes
Upload of Message " yes " successful

C:\Users\royal\OneDrive\Desktop\CS3251\PA1>python client.py -d localhost 12000
Last Message: yes

C:\Users\royal\OneDrive\Desktop\CS3251\PA1>python client.py -u localhost 12000 no
Upload of Message " no " successful

C:\Users\royal\OneDrive\Desktop\CS3251\PA1>python client.py -d localhost 12000
Last Message: no

C:\Users\royal\OneDrive\Desktop\CS3251\PA1>python client.py -u localhost 12000 hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
Error: Message exceeds 150 characters.

C:\Users\royal\OneDrive\Desktop\CS3251\PA1>python client.py -d localhost 12000
Last Message: no

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Protocol Description:

	For our specific scenario, the server is run by providing a ServerPort that we assume is valid.
	The client is then run by providing a -u or -d flag, a ServerIP, a ServerPort, and a message if the -u flag is used.
	The flag indicates whether we are uploading or download messages to/from the server.
	The ServerIP is input by the user and if invalid will trigger a "Server Not Found" error.
	The ServerPort given by the client must be the same as the one used to run the server or else the same "Server Not Found" will be triggered.
	This error will also be triggered if the server is not yet running when the client attempts to connect.
	The message is a string of characters with a 150-character limit. If this is exceeded it will cause an error and indicate that maximum length was exceeded.
	If no message is input at all, an error stating no message was inputted will be displayed.

	Given that the user provides valid arguments and all connections are successful, the program should run normally.
	If the download flag is used, the flag itself is sent to the server which checks if there is currently a message on the server or not.
	If not, the server will send back "Empty Message so that "Last Message: Empty Message" is printed.
	If there is a message on the server, it will be sent to the client so that "Last Message: <last message>" will be printed.
	If the upload flag is used, the provided message is sent to the server where it is stored as the current message and also returned to the client
	in order to print "Upload of message " <message> " successful". Upon completion the client closes gracefully while the server does not close or crash
	except through an error or a Keyboard Interrupt.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Known Bugs or Limitations:
	None that I know of other than our restricting the message to 150 characters and the Ctrl-C bug I have noted under ttweetsrc.py:
	On my local machine, Ctrl-C does not exit/quit/close/shutdown the program so you must use Ctrl-Break (via Ctrl-ScrollLock for my on-screen keyboard) but it does seem to work on the shuttle.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
####################################################################################################################################
#Citation of External References and Templates Used
##
##Real Python's Socket Programming in Python Guide: https://realpython.com/python-sockets/
##Python Module of the Week's TCP/IP Client and Server Page: https://pymotw.com/2/socket/tcp.html
##Geeks for Geeks' Socket Programming in Python: https://www.geeksforgeeks.org/socket-programming-python/
##Python Documentation's Socket Programming HOWTO: https://docs.python.org/2/howto/sockets.html
####################################################################################################################################

