
""" test protocol
    nadav zimmerman 318291997 """
MSG_LEN = 2
NAME_CMD = "NAME"
ALL_NAMES_CMD = "GET_NAMES"
SEND_MSG_CMD = 'MSG'
EXIT_CMD = 'EXIT'
IP_CMD = 'NSLOOKUP'

ERROR_MSG = "protocol error: there is no 2 digits for cmd length"


def create_msg(data):
    """add the protocol 2 digits len field th the data"""
    data = str(len(data)).zfill(MSG_LEN) + data
    return data


def get_msg(my_socket):
    """Extract message from protocol, without the length field
       If length field does not include a number, returns False, "Error" """
    cmd_len = my_socket.recv(MSG_LEN)  # read the two first chars from the server that tell the msg length
    if not cmd_len.isalnum():
        msg = ERROR_MSG
        return False, msg
    msg = my_socket.recv(int(cmd_len)).decode()  # read the response from according to the cmd_len protocol
    return True, msg
