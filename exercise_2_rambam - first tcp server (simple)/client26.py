"""EX 2.6 client implementation
   Author: nadav zimmerman
   Date: 5 nov 2022
   Possible client commands defined in protocol.py
"""

import socket
import protocol


def valid_response(user_input, rspn):
    """a func that get the response from the server and check if ut valid"""
    if user_input == protocol.RAND_COMMAND:
        return str(rspn).isalnum() and int(rspn) in range(protocol.MIN, protocol.MAX)
    elif user_input == protocol.NAME_COMMAND or\
            user_input == protocol.TIME_COMMAND or user_input == protocol.EXIT_COMMAND:
        return True
    else:
        return False


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", protocol.PORT))

    while True:
        #   V 1. Add length field ("HELLO" -> "04HELLO")
        user_input = ''
        valid_input = False
        while not valid_input:
            user_input = input("Enter command\n")
            valid_input = protocol.valid_cmd(user_input)
            if not valid_input:
                print("invalid input, please try again")
        cmd = protocol.create_msg(user_input)

        #   V 2. Send it to the server
        my_socket.send((cmd.encode()))

        #   V 3. Get server's response
        respone_len = my_socket.recv(protocol.LENGTH_FIELD_SIZE)
        msg_rcv = my_socket.recv(int(respone_len)).decode()

        # 4. If server's response is valid, print it
        if valid_response(user_input, msg_rcv):
            print(msg_rcv)
        # 5. If command is EXIT, break from while loop
        if msg_rcv == protocol.EXIT_COMMAND:
            break

    print("Closing\n")
    # Close socket
    my_socket.close()

if __name__ == "__main__":
    main()
