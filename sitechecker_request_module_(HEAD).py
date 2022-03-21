"""

A simple CLI (Command Line Interface) tool which can be used in order to diagnose the current status of a particular http server. 
The tool accepts one or two command line arguments:

1.(obligatory) the address (IP or qualified domain name) of the server to be diagnosed (the diagnosis will be extremely simple, we just want to know if the server is dead or alive)
2.(optional) the server's port number (any absence of the argument means that the tool should use port 80)
3.uses the HEAD method instead of GET — it forces the server to send the full response header but without any content; it's enough to check if the server is working properly; the rest of the request remains the same as for GET.

The tool does:

- the tool checks if it is invoked properly, and when the invocation lacks any arguments, the tool prints an error message and returns an exit code equal to 1;
- if there are two arguments in the invocation line and the second one is not an integer number in the range 1..65535, the tool prints an error message and returns an exit code equal to 2;
- if the tool experiences a timeout during connection, an error message is printed and 3 is returned as the exit code;
- if the server's addres is not existing or is typed wrongly, an error message is printed and 4 is returned as the exit code;
- if the connection fails due to any other reason, an error message appears and 5 is returned as the exit code;
- if the connection succeeds, the very first line of the server’s response is printed.


Run the code:
Using Windows Comand Prompt:
- go to the location of the code file (where this code is located on your computer)
cd "to code location"
- type in the Comand Prompt window (service port by default is 80 if not specified):
python sitechecker.py sever_address server_service_port

"""


import sys
import requests


# function used to establish a connection to the server and to ask it for a header request and to store that request
def request(server_addr, service_port):
    try:
        # initiate head request
        head_request = requests.head(
            "http://" + server_addr + ":" + service_port + "/", headers=sent_header_close)
    except requests.exceptions.InvalidURL:
        print("The server address is wrong")
        exit("Exit code: 5")
    except requests.exceptions.ConnectionError:
        print("Connection Error")
        exit("Exit code: 5")
    except requests.exceptions.Timeout:
        print(
            """Server is busy, it didn't respond in time.
                Retry again, please!""")
        exit("Exit code: 3")
    except requests.RequestException:
        print("Server error")
        exit("Exit code: 4")
    else:
        print(head_request.headers)


# header used in .head() method to tell the server to close our connection
sent_header_close = {"Connection": "close"}


# check if the tool has all necessary arguments
# min. arguments = 2 and max. arguments = 3
# if the required number of arguments is missing it will print a message and the code
# will be terminated
if len(sys.argv) not in [2, 3]:
    print("""Improper number of arguments: at least one is required and not more than two are allowed:
    - http server's address (required)
    - port number (defaults to 80 if not specified)""")
    exit("Exit code: 1")
# if the number of arguments is 2 (script's name and sever adress) the service port
# used by default is 80 and the code will try to send a header request to the
# addressed server using the "socket_function" function
elif len(sys.argv) == 2:
    # argv[1] stores server's address
    server_addr = sys.argv[1]
    request(server_addr, service_port="80")
# if the number of arguments is 3 (script's name, sever adress and service port) and
# the port number not an integer in the range 0 to 65535 it will print an error
# message and the code will be terminated
elif len(sys.argv) == 3 and int(sys.argv[2]) not in range(0, 65536):
    print("Port number is invalid: enter an integer from 0 to 65535")
    exit("Exit code: 2")
# if all the requirements are satisfied (all three arguments are valid) the code will
# try to send a header request to the addressed server using the "socket_function"
# function
else:
    server_addr = sys.argv[1]
    service_port = sys.argv[2]
    request(server_addr, service_port)
