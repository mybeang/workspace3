import serial
import re
import yaml
import time
import pdb
import logging
import sys


class SerialSession(object):
    BAUDRATE = 'baudrate'
    PORT = 'port'
    def __init__(self, env_data):
        self.s = serial.Serial()
        self.s.baudrate = env_data[self.BAUDRATE]
        self.s.port = env_data[self.PORT]
        self.open()

    def __del__(self):
        self.close()

    def _cK_prompt(self, data, user_prompt):
        if user_prompt:
            up_rex = re.compile(user_prompt)
            if up_rex.findall(data):
                return True
            else:
                return False
        else:
            if re.findall(r'\w+>', data):
                return True
            elif re.findall(r'\w+#', data):
                return True
            elif re.findall(r'\w+\(\w+\)#', data):
                return True
            elif re.findall(r'\w+@', data):
                return True
            else:
                return False

    def open(self):
        connection_info = "Open Session - [ Port: %s, Baudrate: %s ]" % (self.s.port, self.s.baudrate)
        logging.info(connection_info)
        self.s.open()

    def close(self):
        logging.info("Close Session")
        self.s.close()

    def send_command(self, cmd, read_time=1, user_prompt=None, timeout=float(1)):
        logging.debug("CMD: %s" % cmd)
        self.s.write(cmd.encode('ascii') + b'\n')
        time.sleep(read_time)
        __buf = ''
        _timeout = timeout * 1000
        while _timeout:
            try:
                __buf += self.s.read().decode('utf-8')
            except:
                __buf += ''
            time.sleep(0.001)
            if self._cK_prompt(__buf, user_prompt):
                break
            _timeout = _timeout - 1

        logging.debug("RES: %s" % __buf)

        string_data = '\n'.join(__buf.splitlines()[1:-1])
        self.s.flushInput()
        self.s.flushOutput()
        return string_data


if __name__=="__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    stdout_handler = logging.StreamHandler(sys.stdout)
    fmter = logging.Formatter('%(asctime)-15s %(levelname)-7s %(message)s')
    stdout_handler.setFormatter(fmter)
    logger.addHandler(stdout_handler)

    with open('env.yml', 'r') as f:
        env_data = yaml.load(f)

    ss = SerialSession(env_data['Serial'])
    ss.send_command('flashinfo')
    ss.send_command('reboot', user_prompt='Boot Mode:')
    ss.send_command('s')
    ss.send_command('\n')
    ss.send_command('\n')
    ss.send_command('flashinfo')

