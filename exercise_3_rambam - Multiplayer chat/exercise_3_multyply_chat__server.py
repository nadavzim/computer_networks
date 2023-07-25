""" multiply chat server exercise nadav zimmerman 318291997 """

import socket
import select
import exercise_3_multyply_chat__protocol as protocol

SERVER_PORT = 5555
SERVER_IP = "0.0.0.0"
SPACE = ' '


def my_dns(site, op_code=0):
    try:
        res = ''
        if op_code == 0:
            dns_req = IP(dst='8.8.8.8')/UDP(sport=2000, dport=53)/DNS(qdcount=1)/DNSQR(qname=site)
            dns_rcv = sr1(dns_req, verbose=0)
            for i in range(0, dns_rcv[DNS].ancount):
                try:
                    return_ip = dns_rcv[DNSRR][i].rdata
                    if ipaddress.ip_address(return_ip):
                        res += return_ip + '\n'
                except ValueError:
                    continue
        else:
            site = ipaddress.ip_address(site).reverse_pointer
            dns_req = IP(dst='8.8.8.8')/UDP(dport=53)/DNS(qdcount=1, )/DNSQR(qname=site, qtype='PTR')
            dns_rcv = sr1(dns_req, verbose=0)
            dns_rcv.show()
            res = dns_rcv[DNSRR].rdata
        return res  # res[DNSRR].rdata
    except:
        return 'error'


def server_response(data, _socket, users):
    """ a func that get the data and return the msg according to the cmd"""
    res = ''
    if data.startswith(protocol.NAME_CMD + SPACE):
        """ NAME cmd """
        if data.endswith(protocol.NAME_CMD):
            res = "You didn't enter any name"
            return res
        name = data.split(' ', 1)[1]
        if name in users.keys():  # if the name is already exist
            res = 'The username is already taken'
            return res
        elif _socket in users.values():  # if the name isn't exist - change the name and delete the earlier name
            k = list(users.keys())[list(users.values()).index(_socket)]
            users.pop(k)
        res = "HELLO " + name
        users.update({name: _socket})

    elif data == protocol.ALL_NAMES_CMD:  # if cmd is print all names - res = all names in dic
        for s in users.keys():
            res += s + ' '

    elif data.startswith(protocol.SEND_MSG_CMD + SPACE):  # if cmd is send msg - return the msg
        if data.count(' ') >= 2:  # if there is a msg to send after the user name
            res = data.split(' ', 2)[2]
        else:
            res = ''  # there is no actual msg...

    elif data == protocol.EXIT_CMD:  # if cmd is exit
        res = ''
    else:
        res = "ERROR! there is no such cmd"
    return res


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
                """if the curr socket is the server socket - add new client to the chat"""
                (connection, client_address) = current_socket.accept()
                print("New client joined!", client_address)
                client_sockets.append(connection)

            else:
                print("Data from existing client\n")
                try:
                    valid, data = protocol.get_msg(current_socket)
                    if data.find(SPACE) > 0:  # if there a space in the data received:
                        if data.split(SPACE)[0] not in [protocol.NAME_CMD, protocol.SEND_MSG_CMD]:
                            valid = False
                            data = "ERROR! there is no such cmd"
                    elif data not in [protocol.EXIT_CMD, protocol.ALL_NAMES_CMD]:
                        valid = False
                        data = "ERROR! there is no such cmd"
                except ConnectionResetError as err:  # if the connection close forcibly
                    print(err.strerror)
                    data = protocol.EXIT_CMD
                if not valid:  # if there is no 2 digits in the receive msg as the protocol ordered
                    data = protocol.create_msg(data)
                    current_socket.send(data.encode())
                    break
                if data == protocol.EXIT_CMD:
                    print("Connection closed")
                    k = list(names_of_users.keys())[list(names_of_users.values()).index(current_socket)]
                    # find the socket according to the key- name, and close and delete it
                    names_of_users.pop(k)
                    client_sockets.remove(current_socket)
                    current_socket.close()
                else:
                    messages_to_send.append((current_socket, data))

            for message in messages_to_send:
                current_socket, data = message
                if current_socket in write_list:  # if the target socket is available
                    res = server_response(data, current_socket, names_of_users)

                    if data.startswith(protocol.SEND_MSG_CMD):  # if cmd is send msg:
                        sender_name = list(names_of_users.keys())[list(names_of_users.values()).index(current_socket)]
                        target_name = data.split(' ', 2)[1]
                        target_socket = names_of_users.get(target_name)
                        if target_socket in write_list:
                            if res == '':
                                messages_to_send.remove(message)
                                continue

                            res = sender_name + ' sent ' + res
                            res = protocol.create_msg(res)
                            target_socket.send(res.encode())
                        else:  # if the user usn't at the dic
                            res = "ERROR! there is no such user"
                            res = protocol.create_msg(res)
                            current_socket.send(res.encode())

                    else:
                        res = protocol.create_msg(res)
                        current_socket.send(res.encode())
                    messages_to_send.remove(message)


if __name__ == '__main__':
    main()

