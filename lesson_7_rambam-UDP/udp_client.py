import socket
import timeit


def udp_server():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.sendto('Omer'.encode(), ('127.0.0.1', 8821))
    (data, remote_address) = my_socket.recvfrom(1024)
    print('The server sent: ' + data.decode())
    my_socket.close()


# record start time
t_0 = timeit.default_timer()
# call function
udp_server()
# record end time
t_1 = timeit.default_timer()

# calculate elapsed time and print
elapsed_time = round((t_1 - t_0) * 10 ** 6, 3)
print(f"udp server Elapsed time: {elapsed_time} µs")
