
""" multiply chat server exercise nadav zimmerman 318291997 """

import socket
import select
import exercise_3_multyply_chat__protocol as protocol

SERVER_PORT = 5555
SERVER_IP = "0.0.0.0"
SPACE = ' '
INVALID_CMD = "ERROR! there is no such cmd"


def server_response(data, _socket, users):
    res, op = '', ''
    try:
        data = data.split(SPACE)
        cmd = data[0]
        if cmd == protocol.NAME_CMD:
            op = protocol.NAME_CMD
            """ NAME cmd """
            if len(data) == 1:
                res = "You didn't enter any name"

            else:
                name = data[1]
                if name in users.keys():  # if the name is already exist
                    res = 'The username is already taken'
                elif _socket in users.values():  # if the name isn't exist - change the name and delete the earlier name
                    k = list(users.keys())[list(users.values()).index(_socket)]
                    users.pop(k)
                    res = "HELLO " + name
                    users.update({name: _socket})

        elif cmd == protocol.ALL_NAMES_CMD:  # if cmd is print all names - res = all names in dic
            op = protocol.ALL_NAMES_CMD
            for s in users.keys():
                res += s + ' '

        elif cmd == protocol.SEND_MSG_CMD:  # if cmd is send msg - return the msg
            op = protocol.SEND_MSG_CMD
            try:
                res = data[1]
            except Exception as e:
                res = ''   # there is no actual msg...

        elif cmd == protocol.EXIT_CMD:  # if cmd is exit
            op = protocol.EXIT_CMD
            res = ''
        return res, op
    except Exception as e:
        return INVALID_CMD, ''


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    print("server is running")
    server_socket.listen()

    client_sockets = []
    messages_to_send = []
    names_of_users = {}

    while True:
        valid = True
        read_list, write_list, error_list = select.select([server_socket] + client_sockets, client_sockets, [])
        for current_socket in read_list:
            if current_socket is server_socket:
                """add new client to the chat"""
                (connection, client_address) = current_socket.accept()
                print("New client joined!", client_address)
                client_sockets.append(connection)

            else:
                print("Data from existing client\n")
                try:
                    valid, data = protocol.get_msg(current_socket)
                    msg, op = server_response(data, current_socket, names_of_users)
                    if not valid:  # if there is no 2 digits in the receive msg as the protocol ordered
                        msg = INVALID_CMD
                    elif op == protocol.NAME_CMD:
                        continue
                    elif op == protocol.ALL_NAMES_CMD:
                        continue
                    elif op == protocol.SEND_MSG_CMD:
                        continue
                except ConnectionResetError as err:  # if the connection close forcibly
                    op = protocol.EXIT_CMD
                    print(err.strerror)
                if op == protocol.EXIT_CMD:
                    print("Connection closed")
                    k = list(names_of_users.keys())[list(names_of_users.values()).index(current_socket)]
                    # find the socket according to the key- name, and close and delete it
                    names_of_users.pop(k)
                    client_sockets.remove(current_socket)
                    current_socket.close()
                    break
                else:
                    messages_to_send.append((current_socket, msg, op))

            for message in messages_to_send:
                current_socket, msg, op = message
                if current_socket in write_list:  # if the target socket is available
                    if op == protocol.SEND_MSG_CMD:
                        sender_name = list(names_of_users.keys())[list(names_of_users.values()).index(current_socket)]
                        try:
                            target_name, msg = msg.split(SPACE, 1)
                            target_socket = names_of_users.get(target_name)
                            if target_socket in write_list:
                                if msg == '':
                                    messages_to_send.remove(message)
                                    continue
                            msg = sender_name + ' sent ' + msg
                        except:  # if the user usn't at the dic
                            msg = "ERROR! there is no such user"
                        msg = protocol.create_msg(msg)
                        current_socket.send(msg.encode())

                    msg = protocol.create_msg(msg)
                    current_socket.send(msg.encode())
                    messages_to_send.remove(message)


if __name__ == '__main__':
    main()
