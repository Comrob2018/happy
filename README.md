# happy
A bot server and search script that will allow for remote administration of a system.
USAGE: python3 happy_little_bot.py <> python3 happy_little_srvr.py
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
  
    You will see the following prompt once you connect to a client:
    [-] <username>@<user_ip>:<user_working_dir> > server command
  
    For example, if connecting to sam at 127.0.0.1 in the home folder:
    [-] sam@127.0.0.1:/home> server command
    
    Server commands are listed below with example usage and output everything 
    inside <> will need to be replaced with your data or commands. 
  
    For download and upload, the absolute path is required for source file and destination.
  
    The absolute path includes the file name and extension.
  
    command     - Send shell commands to the client. 
    |    [-] <username>@<user_ip>:<user_working_dir> > command
    |    [!] Enter client command
    |    [!] <username>@<user_ip>:<user_working_dir> > shell command
    |    [!] Command output:
    |    <command output if there is any>
    |    [!] Client command Complete
  
  
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
