"""EX 2.6 protocol implementation
   Author: nadav zimmerman
   Date: 5 nov 2022

   Possible client commands:
   NUMBER - server should reply with a random number, 0-99
   HELLO - server should reply with the server's name, anything you want
   TIME - server should reply with time and date
   EXIT - server should send acknowledge and quit
"""

LENGTH_FIELD_SIZE = 2
PORT = 8820
TIME_COMMAND = "TIME"
NAME_COMMAND = "WHORU"
RAND_COMMAND = "RAND"
EXIT_COMMAND = "EXIT"
MIN = 0
MAX = 99


def create_msg(data):
    """Create a valid protocol message, with length field"""
    data = str(len(data)).zfill(LENGTH_FIELD_SIZE) + data
    return data


def remove_len_field(my_socket):
    try:
        cmd_len = my_socket.recv(LENGTH_FIELD_SIZE)  # read the two first chars from the server that tell the msg length
        if not cmd_len.isalnum():
            return "there is no 2 digits for cmd length"
        msg_rcv = my_socket.recv(int(cmd_len)).decode()  # read the response from the server according to the  cmd_len
    except:
        return "there is no 2 digits for cmd length"
    return msg_rcv


def valid_cmd(msg):
    return msg in [TIME_COMMAND, NAME_COMMAND, RAND_COMMAND, EXIT_COMMAND]


def get_msg(my_socket):
    """Extract message from protocol, without the length field
       If length field does not include a number, returns False, "Error" """
    cmd = remove_len_field(my_socket)
    valid = valid_cmd(cmd)
    return valid, cmd
