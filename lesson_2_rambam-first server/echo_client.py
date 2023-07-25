import socket
import timeit


def echo_client():
    my_socket = socket.socket()
    my_socket.connect(("127.0.0.1", 1234))

    my_socket.send("Omer".encode())
    data = my_socket.recv(1024).decode()
    print("The tcp server sent: " + data)  # + ' it\'s took ' + str(send_t - rcv_t) + " second")
    my_socket.close()


# record start time
t_0 = timeit.default_timer()
# call function
echo_client()
# record end time
t_1 = timeit.default_timer()

# calculate elapsed time and print
elapsed_time = round((t_1 - t_0) * 10 ** 6, 3)
print(f"tcp server Elapsed time: {elapsed_time} µs")
