# Ex 6 - HTTP Server Shell
# Author: nadav zimmerman

# TO DO: import modules
import socket
from scapy.all import *

# TO DO: set constants
MY_IP = '127.0.0.1'
PORT = 8153
IP_MAX = 255
IP_MIN = 0
SOCKET_TIMEOUT = 0.1
NAME_ERROR = 3
GET_CMD = "GET "
CMD_END_LINE = b"\r\n"
CMD_END = "HTTP/1.1"

FIXED_RESPONSE = "HTTP/1.0 200 OK\r\n"
E404_RESPONSE = "HTTP/1.0 404 Not found\r\n"
URL_DID_NOT_FOUND = '<html><body>' + "ERROR - the domain name didn't found"
IP_DID_NOT_FOUND = '<html><body>' + "ERROR - the ip didn't found"
IP_INVALID = '<html><body>' + "ERROR - the ip isn't valid"

REVERSE_MATTING = 'reverse'
DNS_SERVER = '8.8.8.8'
DOT_CHAR = '.'


def reverse_ip(ip):
    res = ''
    numbers = str(ip).split(DOT_CHAR)
    for i in reversed(numbers):
        res += i + DOT_CHAR
    res += 'in-addr.arpa'
    return res


def validate_ip_address(ip):
    try:
        numbers = str(ip).split(DOT_CHAR)
        for i in numbers:
            if int(i) < IP_MIN or int(i) > IP_MAX or not i.isdigit():
                return False
        return True
    except ValueError:
        return False


def handle_client_request(resource, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client"""
    # TO DO : add code that given a resource (URL and parameters) generates the proper response
    body = '<html><body>'
    resource = resource[1::]
    if resource == 'favicon.ico':
        client_socket.send(FIXED_RESPONSE.encode())
        return
    if resource.split('\\')[0] ==REVERSE_MATTING:
        ip_to_srch = resource.split('\\')[1]
        if validate_ip_address(ip_to_srch):
            ip_to_srch = reverse_ip(ip_to_srch)
            dns_req = IP(dst=DNS_SERVER)/UDP(sport=24601, dport=53)/DNS(qdcount=1)/DNSQR(qtype=12, qname=ip_to_srch)
            dns_req[DNS].show()
            answer = IP()/UDP()/DNS()/DNSQR()
            try:
                answer = sr1(dns_req, timeout=2)
                print(answer[DNS].show())
            except TypeError:
                body = IP_DID_NOT_FOUND
            if answer is not None and answer[DNS].rcode != NAME_ERROR and DNSRR in answer:
                body += answer[DNSRR].rdata.decode()
            else:
                body = IP_DID_NOT_FOUND
        else:
            body = IP_INVALID

    else:
        dns_req = IP(dst=DNS_SERVER)/UDP(sport=24601, dport=53)/DNS(qdcount=1)/DNSQR(qname=resource)
        dns_req.show()
        answer = IP()/UDP()/DNS()/DNSQR()
        try:
            answer = sr1(dns_req, timeout=2)
            print(answer[DNS].show())
        except TypeError:
            body = URL_DID_NOT_FOUND
        if answer is not None and answer[DNS].rcode != NAME_ERROR:
            for i in range(0, answer[DNS].ancount):
                try:
                    body += '<p>' + answer[DNSRR][i].rdata + "\n <p>"
                except Exception as e:
                    e
                    continue
        else:
            body = URL_DID_NOT_FOUND
    body += '<body></html>'
    body = body.encode()
    responses_line = FIXED_RESPONSE.encode()
    line_end = CMD_END_LINE
    file_type = b'Content-Type: ' + b'text/html' + CMD_END_LINE
    file_len = b"Content-Length: " + str(len(body)).encode() + CMD_END_LINE
    # send_repley(responses_line, file_type, file_len, body)
    client_socket.send(b''.join([responses_line, file_type, file_len, line_end, body]))
    return


def validate_http_request(request):
    """
    Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL
    """
    packet_end_index = request.find(CMD_END_LINE.decode())
    first_packet = request[:packet_end_index]
    valid = False
    url = ''
    if first_packet.startswith(GET_CMD) and first_packet.endswith(CMD_END):
        valid = True
        url = str(request).split(' ')[1]
        url = url.replace('/', '\\')
    return valid, url


def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print('Client connected')
    while True:
        client_request = client_socket.recv(1024).decode()  # need to add protocol!!!!!!!!!!!!!!!!!!!!!!!!
        valid_http, resource = validate_http_request(client_request)
        if valid_http:
            print('Got a valid HTTP request')
            handle_client_request(resource, client_socket)
            break
        else:
            print('Error: Not a valid HTTP request')
            break
    print('Closing connection')
    client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((MY_IP, PORT))
    server_socket.listen()
    print("Listening for connections on port {}".format(PORT))

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print('New connection received')
            client_socket.settimeout(SOCKET_TIMEOUT)
            handle_client(client_socket)
        except socket.timeout:
            continue


if __name__ == "__main__":
    # Call the main handler function
    main()
