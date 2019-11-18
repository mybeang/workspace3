import socket
import time
import threading
import random


SERVER_PORT = random.randrange(10000, 50000)
CLIENT_PORT = random.randrange(10000, 50000)
FLAGS = "_DASANZHONE_"
UNIT = 1024
SEQ_SIZE = 8
DATA = "0" * (UNIT - (len(FLAGS) + SEQ_SIZE)) + FLAGS


def format_bytes(size, real=False):
    # 2**10 = 1024
    l_power = 1000
    r_power = 2**10
    n = 0
    _size = size
    power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    if real:
        power = r_power
    else:
        power = l_power
    while _size > power:
        _size /= power
        n += 1
    return _size, power_labels[n]+'B'


def server():
    print("Start Server")
    _buff = ""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('192.192.192.100', SERVER_PORT))
    sock.listen(100)
    conn, addr = sock.accept()
    cnt = 0
    _buff = ""
    while True:
        buf = conn.recv(65535).decode()
        if buf:
            _buff += buf
            if DATA in _buff:
                for _ in range(len(_buff.split(FLAGS)) - 1):
                    _buff = _buff[len(DATA):]
                    cnt += 1
        else:
            break
    conn.close()
    sock.close()
    del conn
    del sock
    print("\nCounts: %d" % cnt)


def client(data_size=100000):
    time.sleep(1)
    print("Start Client")
    print(UNIT * data_size)
    num, data_unit = format_bytes(UNIT * data_size)
    print("Send DataSize = %d %s" % (num, data_unit))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('192.192.192.101', CLIENT_PORT))
    sock.connect(("192.192.192.100", SERVER_PORT))
    print("Send Packet")
    percent = 0
    print("percent: [0%]", end="\r")
    for i in range(data_size):
        if i % (data_size/100) == 0:
            percent += 1
            print("percent: [{}%]".format(percent), end='\r')
        sock.send(DATA.encode())
    sock.close()
    del sock


if __name__=="__main__":
    th = threading.Thread(target=server)
    th.daemon = True
    th.start()

    client()

    th.join(1)
    del th