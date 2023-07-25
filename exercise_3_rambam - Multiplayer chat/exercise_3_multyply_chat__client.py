
""" multiply chat server exercise nadav zimmerman 318291997 """

import msvcrt
import select
import socket
import exercise_3_multyply_chat__protocol as protocol

PORT = 5555


def is_valid_cmd(s):
    return protocol.NAME_CMD in s or protocol.ALL_NAMES_CMD in s or protocol.SEND_MSG_CMD in s or protocol.EXIT_CMD in s


def main():
    my_socket = socket.socket()
    my_socket.connect(("127.0.0.1", PORT))

    print("please enter commands")
    user_input, c = '', ''
    keep_running = True
    while keep_running:
        read_list, write_list, error_list = select.select([my_socket], [my_socket], [])
        for curr_socket in read_list:
            valid, response = protocol.get_msg(curr_socket)
            if not valid:  # if there is no 2 digits in the receive msg as the protocol ordered
                print(response)
            if response == '':
                keep_running = False
                my_socket.close()
            else:
                print("server replied: " + response)
                if not user_input == '':
                    print(user_input, flush=True, end='')

        for curr_socket in write_list:
            if msvcrt.kbhit():
                c = msvcrt.getch()
                if c == b'\xe0':  # if the input was arrow key - ignore it
                    msvcrt.getch()
                    break
                else:
                    c = c.decode()
                    user_input += c
                print(c, end='', flush=True)
                if c == '\r':
                    print(c)
                    user_input = user_input.replace('\r', "")
                    cmd = protocol.create_msg(user_input)
                    curr_socket.send(cmd.encode())
                    if user_input == protocol.EXIT_CMD:
                        curr_socket.close()
                        keep_running = False

                    user_input = ''
                    break


if __name__ == '__main__':
    main()
