"""מבחן ברשתות מחשבים בגישה מחקרית - סמסטר א' מועד ב' תשפב"""
import socket
import os

ADD = '1'
SUB = '2'
MULT = '3'
DIV = '4'
ERROR_MSG = 'ERROR'
CONTENT_TYPE = "text/html"
CMD_END_LINE = b"\r\n"
CMD_END = "HTTP/1.1"
GET_CMD = "GET "


def validate_http_request(request):
    """Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL"""
    packet_end_index = request.find(CMD_END_LINE.decode())
    first_packet = request[:packet_end_index]
    valid = False
    if first_packet.startswith(GET_CMD) and first_packet.endswith(CMD_END):
        valid = True
    return valid


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 80))
    server_socket.listen()

    while True:
        res = ERROR_MSG
        connection, address = server_socket.accept()
        print('Client connected')
        request = connection.recv(1024).decode()
        valid = validate_http_request(request)
        if not valid:
            print("got an invalid request")
        else:
            print("got a valid request")

            try:
                request = request.split(' ')[1][1:]
                op, num1, num2 = request.split('/')
                num1, num2 = int(num1), int(num2)
                if op == ADD:
                    res = str(num1 + num2)
                elif op == SUB:
                    res = str(num1 - num2)
                elif op == MULT:
                    res = str(num1 * num2)
                elif op == DIV:
                    res = str(num1 / num2)
                res = res.encode()
                # Encode the res before sending it back to the client
                response = "HTTP/1.1 200 OK\r\n".encode()
            except ValueError:
                res = res.encode()
                response = "HTTP/1.1 404 Not Found\r\n".encode()

            file_len = b"Content-Length: " + str(len(res)).encode() + CMD_END_LINE
            file_type = b'Content-Type: ' + b'text/html' + CMD_END_LINE
            connection.send(b''.join([response, file_len, file_type, CMD_END_LINE, res]))
        connection.close()
        print('Closing connection')


if __name__ == "__main__":
    # Call the main handler function
    main()
