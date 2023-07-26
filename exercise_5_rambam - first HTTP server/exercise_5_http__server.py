# Ex 4.4 - HTTP Server Shell
# Author: nadav zimmerman
# Purpose: Provide a basis for Ex. 4.4
# Note: The code is written in a simple way, without classes, log files or other utilities, for educational purpose
# Usage: Fill the missing functions and constants

# TO DO: import modules
import socket
import os
import mimetypes

# TO DO: set constants
IP = '127.0.0.1'
PORT = 80
SOCKET_TIMEOUT = 0.1
STD_RCV_LEN = 2048
GET_CMD = "GET "
CMD_END_LINE = b"\r\n"
CMD_END = "HTTP/1.1"

FIXED_RESPONSE = "HTTP/1.0 200 OK\r\n"
FOUND_RESPONSE = "HTTP/1.0 302 Found\r\n"
E404_RESPONSE = "HTTP/1.0 404 Not found\r\n"

ROOT_DIR = r"C:\Networks\work\exercise_5_rambam\webroot"
DEFAULT_URL = r"\index.html"
AREA_CALC = "\\calculate-area"

REDIRECTION_DICTIONARY = {ROOT_DIR + r"\changed_direction1":
                          ROOT_DIR + r"\imgs\abstract.jpg",
                          ROOT_DIR + r"\changed_direction2":
                          ROOT_DIR + r"\imgs\favicon.ico",
                          ROOT_DIR + r"\changed_direction3":
                          ROOT_DIR + r"\imgs\loading.gif"}


def get_file_data(filename):
    """ Get data from file """
    file_stream = open(filename, mode='rb')
    data = file_stream.read()
    file_stream.close()
    return data


def get_param(s):  # a func that get a str and return the parameter from it
    res = ''
    index = s.find('=')
    for ch in s[index+1:]:
        res += ch
    try:
        res = float(res)
        return res
    except ValueError:
        return -1


def handle_client_request(resource, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client"""
    if resource == '' or resource == '\\':  # if this is a root request
        url = DEFAULT_URL

    #  Find and handle 'get with parameters'
    elif resource.startswith(AREA_CALC) and 'height=' in resource and 'width' in resource:
        params = resource.split('?')[1]
        height = get_param(params.split('&')[0])
        width = get_param(params.split('&')[1])
        if height >= 0 and width >= 0:
            res = str(height*width / 2).encode()
        else:
            res = "invalid input! height and width has to be positive numbers".encode()
        responses_line = FIXED_RESPONSE.encode()
        line_end = CMD_END_LINE
        file_len = b"Content-Length: " + str(len(res)).encode() + CMD_END_LINE
        file_type = b'Content-Type: ' + b'text/html' + CMD_END_LINE
        client_socket.send(b''.join([responses_line, file_len, file_type, line_end, res]))
        return

    else:
        url = resource

    url = ROOT_DIR + url  # add the root dir to get the full url

    #  Handle e302
    if url in REDIRECTION_DICTIONARY:
        responses_line = FOUND_RESPONSE.encode()
        line_end = CMD_END_LINE
        location = REDIRECTION_DICTIONARY[url].replace(ROOT_DIR, '').replace('\\', '/')
        location = b'Location: ' + location.encode()
        client_socket.send(b''.join([responses_line, location, line_end]))

    #  Handle E404
    elif not os.path.isfile(url):
        print("ERROR - invalid path")
        responses_line = E404_RESPONSE.encode()
        line_end = CMD_END_LINE
        client_socket.send(b''.join([responses_line, line_end]))

    #  Handle 200 - ok
    else:
        responses_line = FIXED_RESPONSE.encode()
        line_end = CMD_END_LINE
        body_response = get_file_data(url)
        file_type = b'Content-Type: ' + (str(mimetypes.guess_type(url)[0]) or 'text/html').encode() + CMD_END_LINE
        file_len = b"Content-Length: " + str(len(body_response)).encode() + CMD_END_LINE
        client_socket.send(b''.join([responses_line, file_type, file_len, line_end, body_response]))
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
        client_request = client_socket.recv(STD_RCV_LEN).decode()
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
    server_socket.bind((IP, PORT))
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
