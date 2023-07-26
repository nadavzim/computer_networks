import socket


server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 1234))
server_socket.listen()
print("Server is up and running")
(client_socket, client_address) = server_socket.accept()
print("Client connected")
data = client_socket.recv(1024).decode()
print("Client sent: " + data)
client_socket.send(data.encode())
client_socket.close()
server_socket.close()
