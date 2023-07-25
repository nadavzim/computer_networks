# write in python a http server base on socket that get the webroot raw address r"C:\Networks\work\exercise_5_rambam\webroot".
# the port will be 80 and the way to connect the server is 127.0.0.1 .
# the default path for the server is r"\index.html".
# import socket and os.
# extract the path fom the server get cmd.
# if the path from the server has / replace it with \
# if the file get / or \\ change the path to the default path.
# add the webroot to the received path.
# if the path is valid send the 200 ok response with '\r\n' to the server.
# read from the file path.
# check the content type and send the content type header and content file_length heder , each heder end with '\r\n'
#
# the server will continue get new request until the request is "".
# check if it in the REDIRECTION_DICTIONARY for e302 with location header and location header.
# if the path is not valid return e404.
# REDIRECTION_DICTIONARY = {r"C:\Networks\work\exercise_5_rambam\webroot\changed_direction1": r"/imgs/abstract.jpg", r"C:\Networks\work\exercise_5_rambam\webroot\changed_direction2": r"/webroot/imgs/favicon.ico", r"C:\Networks\work\exercise_5_rambam\webroot\changed_direction3": r"/webroot/imgs/loading.gif"}
#
# after send the data from the file to the server close the connection and wait for a new connection


# in a exsist http server socket, check if the server received a in the 'path' variable msg that start with "/calculate-area?"/then take from the "msg received the value of the 2 variables names width and height and check if thet are both positive.
# if they are it returns the size of the triangle made from them.
# send back the answer to the 'connection' socket in connection. Send() method.
# the socket already exists, change msg to "path'. dont open a socket the socket already exists.


import socket
import os

webroot_raw_address = r"C:\Networks\work\exercise_5_rambam\webroot"

REDIRECTION_DICTIONARY = {r"C:\Networks\work\exercise_5_rambam\webroot\changed_direction1": r"/imgs/abstract.jpg",
r"C:\Networks\work\exercise_5_rambam\webroot\changed_direction2": r"/imgs/favicon.ico",
r"C:\Networks\work\exercise_5_rambam\webroot\changed_direction3": r"/imgs/loading.gif"}

default_path = r"\index.html"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 80))
server_socket.listen(5)

while True:
    connection, address = server_socket.accept()
    request = connection.recv(1024).decode("utf-8")

    if request == "":
        break
    path = request.split(" ")[1]

    if path.startswith('/calculate-area?'):
        # Parse the width and height from the path
        width, height = path.split('&')
        width = int(width.split('=')[1])
        height = int(height.split('=')[1])
        # Check if width and height are positive
        if width > 0 and height > 0:
            # Calculate the area of the triangle
            area = 0.5 * width * height
            # Encode the result before sending it back to the client
            result = str(area).encode()
            connection.send(result)
            # Break out of the loop
        break

    path = path.replace("/", "\\")
    if path == "/" or path == "\\":
        path = default_path
    path = os.path.join(webroot_raw_address, path[1:])
    if os.path.exists(path):
        response = "HTTP/1.1 200 OK\r\n"
        file_type = os.path.splitext(path)[1]
        content_type = ""
        if file_type == ".html":
            content_type = "text/html"
        elif file_type == ".jpg":
            content_type = "image/jpg"
        elif file_type == ".png":
            content_type = "image/png"
        elif file_type == ".gif":
            content_type = "image/gif"
        response += "Content-Type: {}\r\n".format(content_type)
        file_length = os.stat(path).st_size
        response += "Content-Length: {}\r\n\r\n".format(file_length)
        connection.sendall(response.encode("utf-8"))
        with open(path, "rb") as f:
            connection.sendfile(f)
    else:
        if path in REDIRECTION_DICTIONARY:
            response = "HTTP/1.1 302 Found\r\n"
            response += "Location: {}{}\r\n\r\n".format("", REDIRECTION_DICTIONARY[path])
            connection.sendall(response.encode("utf-8"))
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\n"
            connection.sendall(response.encode("utf-8"))
    connection.close()

server_socket.close()
