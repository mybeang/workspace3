import socket
import time

iface_name = "Realtek USB FE Family Controller #2"

port = 56000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2 ** 20)
sock.bind(('192.192.192.7', port))
sock.connect(("192.192.192.100", port))

time.sleep(5)

print("Send Packet")
for i in range(100000):
    seq = "DASANZHONE_%.8d" % i
    print(seq)
    sock.send(seq.encode())
    time.sleep(0.001)

sock.close()
del sock



