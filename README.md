# Happy_SRVR
A bot server and search script that will allow for remote administration of a system.

USAGE: python3 happy_bot.py <> python3 happy_srvr.py

    All messages that start with [-] are server side
    All messages that start with [!] are client side
    The script will start as follows:
    [-] Binding Port: <port>
    [-] Listening for connections...(until you receive a connection)
    [-] Connection Received
    [-] Connection established with client at <ip>
    [-] Enter server commands or ? for list of server commands
    [-] user@ip:working_dir> 

    You will see the following prompt once you connect to a client:
    [-] user@ip: working_dir> 
    For example, if connecting to sam at 127.0.0.1 in the home folder:
    [-] sam@127.0.0.1: /home> 
    
    Server commands are listed below with example usage and output everything 
    inside <> will need to be replaced with your data or commands. 
    
    cmd = command     - Send a single shell command to the client. 
    |    [-] user@ip: working_dir> cmd
    |    [!] Client ready for command
    |    [-] s - single or m - multiple:> s
    |    [!] user@ip: working_dir> os command
    |    [!] Command output:
    |    <command output if there is any>
    |    [!] Client command complete
    
    For download and upload, the absolute path is required for source file and destination.
    The absolute path includes the file name and extension.
    
    dl = download    - receive a file from the client.
    |    [-] user@ip: working_dir> dl
    |    [-] Please provide the absolute path for the client file and server destination
    |    [!] Ready for file name
    |    [-] What is the client file?> <Full path to file with extension>
    |    [-] What is the server destination?> <Full path to new location with extension>
    |    [-] File successfully downloaded to : <path provided>
    |    [!] Client download complete
    
    ul = upload      - send a file to the client.
    |    [-] user@ip: working_dir> > ul
    |    [-] Please provide the absolute path for the server file 
    |    [-] What server file?> <full file path of server file>
    |    [-] Please provide the absolute path for the client destination:>
    |    [-] What client destination?> <full file path to destination on the client system>
    |    [!] Ready for file contents
    |    [!] File uploaded to client at : <file location specified>
    |    [!] Client upload Complete

    src = search      - search the file system using regular expressions
    |    [-] user@ip: working_dir> src
    |    [-] Where should we start looking?> <start location on client>
    |    [-] Do you know the file name?> <yes or no>
    |    If you answer yes:
    |    |    [!] Ready for file name
    |    |    [-] What is the file name?> <file name on client system>
    |    If you answer no:
    |    |    [!] No file name, using default pattern 
    |    [-] Searching for file...
    |    <Results of search>
    |    [!] Client search complete
    
    sh = shell       - receive a terminal connection to the client on linux
    |    [-] user@ip: working_dir> sh
    |    [!] Client received shell command
    |    Listening on [0.0.0.0] for connections...
    |    Connection from <ip> <port>
    |    student@kali:~/Desktop$ <os command>

    h = help        - display the basic or advanced help string  
    |    [-] <username>@<user_ip>:<user_working_dir> h
    |    [-] Would you like the basic or advanced help?> <b or adv>
    |    <help string>
    
    dc = disconnect   - disconnect from the client
    |    [-] user@ip: working_dir> dc
    |    [!] Connection terminated at client
    |    [-] Listening for Connections...
    
    qt/ex = quit/exit    - exit the program
    |    [-] user@ip: working_dir> qt
    |    [!] Connection terminated at client
    |    [-] Good Day sir, you win nothing nada zip.
    |    [-] I said Good Day!
    
    cl = clear       - clear the terminal screen
    |    [-] user@ip: working_dir> cl
    
    b = banner       - Reroll the banner
    |    [-] user@ip: working_dir> b
    
