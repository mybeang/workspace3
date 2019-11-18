import logging, sys

import telnetlib, time, threading

class KKK(object):
    def __init__(self, ip_addr):
        self.logger = logging.getLogger('koods')
        strhdr = logging.StreamHandler(sys.stdout)
        self.logger.setLevel(logging.INFO)
        fmt = logging.Formatter("%(asctime)-15s %(levelname)-7s %(message)s")
        strhdr.setFormatter(fmt)
        self.logger.addHandler(strhdr)
        self.HOST = "10.55.195.97"
        self.tn = telnetlib.Telnet(ip_addr)
        self.buf = b""
        self.logging_flags = True
        self.login()
        self.start_logging()

    def __del__(self):
        self.stop_logging()
        self.th.join(1)
        del self.th

    def start_logging(self):
        self.th = threading.Thread(target=self.logging)
        self.th.daemon = True
        self.th.start()

    def stop_logging(self):
        self.logging_flags = False

    def logging(self):
        while True:
            time.sleep(0.01)
            if self.buf:
                self.logger.info(self.buf.decode().strip())
            self.buf = b""
            if not self.logging_flags:
                break

    def close(self):
        del self.tn

    def login(self):
        r_str = self.tn.read_until(b"ogin: ")
        self.buf += r_str

    def communication(self, text, expect):
        self.buf += b" " + text.encode() + b"\n"
        self.tn.write((text + "\n").encode())
        reply = self.tn.read_until(expect.encode())
        self.buf += reply.replace((text + "\r\n").encode(), b"")

cmds = [
    ('admin', 'ord:'),
    (" ", ">"),
    ("en", "#"),
    ("show run", "#"),
    ("show mac", "#"),
    ("conf t", "#"),
    ("show ip route", "#"),
    ("end", "#"),
    (" ", "#"),
    (" ", "#"),
    (" ", "#"),
    ("exit", "")
]

kkk = KKK("10.55.195.97")

for text, expect in cmds:
    kkk.communication(text, expect)

kkk.close()
del kkk