"""EX 2.6 server implementation
   Author: nadav zimmerman
   Date: 5 nov 2022
   Possible client commands defined in protocol.py
"""

import socket
import protocol
import datetime
import random

SERVER_NAME = "NADAV'S SUPER SERVER"


def create_server_rsp(cmd):
    """Based on the command, create a proper response"""
    if cmd == protocol.TIME_COMMAND:
        now = datetime.datetime.now()
        res = "the time right now is " + now.strftime("%H:%M:%S")
    elif cmd == protocol.NAME_COMMAND:
        res = SERVER_NAME
    elif cmd == protocol.RAND_COMMAND:
        res = str(random.randint(protocol.MIN, protocol.MAX))
    elif cmd == protocol.EXIT_COMMAND:
        res = protocol.EXIT_COMMAND
    else:
        res = 'ERROR'
    return res


def check_cmd(data):
    """Check if the command is defined in the protocol (e.g NUMBER, HELLO, TIME, EXIT)"""
    if data in [protocol.TIME_COMMAND, protocol.NAME_COMMAND, protocol.RAND_COMMAND, protocol.EXIT_COMMAND]:
        return True


def main():
    # Create TCP/IP socket object
    server_socket = socket.socket()
    # Bind server socket to IP and Port
    server_socket.bind(("127.0.0.1", protocol.PORT))

    # Listen to incoming connections
    server_socket.listen()
    print("Server is up and running")

    # Create client socket for incoming connection
    (client_socket, client_address) = server_socket.accept()
    print("Client connected")

    while True:
        # Get message from socket and check if it is according to protocol
        valid_msg, cmd = protocol.get_msg(client_socket)
        if valid_msg:
            # 1. Print received message
            print(cmd)
            # 2. Check if the command is valid, use "check_cmd" function
            # 3. If valid command - create response
            response = create_server_rsp(cmd)
        else:
            response = "Wrong protocol" + cmd
            client_socket.recv(1024)  # Attempt to empty the socket from possible garbage

        # Send response to the client
        response = protocol.create_msg(response)
        client_socket.send(response.encode())

        # If EXIT command, break from loop
        if response == protocol.EXIT_COMMAND:
            break
    print("Closing\n")
    # Close sockets
    client_socket.close()
    server_socket.close()


if __name__ == "__main__":
    main()
