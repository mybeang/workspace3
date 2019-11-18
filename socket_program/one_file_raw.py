import socket
import time
import threading
import random
import colorlog
import logging


SERVER_PORT = random.randrange(10000, 50000)
CLIENT_PORT = random.randrange(10000, 50000)
FLAGS = "_DASANZHONE_"
UNIT = 1024
SEQ_SIZE = 8

DATA = "0" * (UNIT - len(FLAGS)) + FLAGS


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

class OneFile(object):
    def __init__(self):
        self.buf = list()

    def server(self):
        logging.info("Start Server")
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2 ** 20)
        sock.bind(('192.192.192.101', SERVER_PORT))
        logging.info("The Server Port: {}".format(SERVER_PORT))
        sock.settimeout(60)

        #while True:
        #    self.buf.append(sock.recvfrom(65535))

    def start(self):
        th = threading.Thread(target=self.server)
        th.daemon = True
        th.start()

        self.client()
        # n_client()

        th.join(1)
        del th

    def client(self, data_size=1000000):
        time.sleep(1)
        logging.info("Start Client")
        logging.debug("Data UNIT Size = {} Bytes".format(UNIT))
        logging.debug("Packet Size = {} Bytes".format(UNIT + 40))
        num, data_unit = format_bytes(UNIT * data_size)
        logging.debug("Send DataSize = %d %s" % (num, data_unit))
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 2 ** 20)
        sock.bind(('192.192.192.100', CLIENT_PORT))
        logging.info("The Client Port: {}".format(CLIENT_PORT))
        logging.info("Send Packet")
        data = DATA.encode()
        for i in range(data_size):
            sock.sendto(data, ('192.192.192.101', SERVER_PORT))
        sock.close()
        del sock

    def result(self):
        logging.info("TOTAL COUNT: {}".format(len(self.buf)))
        cnt = 0
        for buf_ in self.buf:
            if FLAGS in buf_[0].decode():
                cnt += 1
        logging.info("COUNT: {}".format(cnt))

if __name__=="__main__":
    logger = colorlog.getLogger()
    logger.setLevel(logging.DEBUG)
    chdr = colorlog.StreamHandler()
    chdr.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)-15s %(message)s'
    ))
    logger.addHandler(chdr)
    one = OneFile()
    one.start()
    #one.result()
