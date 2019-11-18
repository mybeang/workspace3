import socket
import time

buf_list = list()
port = 56000
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2 ** 20)
sock.settimeout(60)
sock.bind(('192.192.192.100', port))
sock.listen(100)
sock.accept()
i = 0
while True:
    time.sleep(0.1)
    if i > 10:
        print("Running Server")
        i = 0
    i += 1
    try:
        buf = sock.recv(65535).decode()
    except OSError as e:
        print("ERROR: {}".format(e))
        break
    except socket.timeout:
        break
    except KeyboardInterrupt:
        break
    else:
        if buf:
            buf_list.append(buf)

sock.close()
del sock