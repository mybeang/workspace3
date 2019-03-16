import tftpy as tftp
import threading as th
import time
from pathlib2 import Path
import os


SERVER_PATH = "D:\\tftp_test\\tftp_server"
CLIENT_PATH = "D:\\tftp_test\\tftp_client"
REMOTE_FILE_NAME = "hello_tftp.txt"
LOCAL_FILE_NAME = "hello_tftp.txt"
IP = "127.0.0.1"
PORT = 69

my_file = Path(CLIENT_PATH + "\\" + LOCAL_FILE_NAME)
if my_file.is_file():
    os.remove(str(my_file))
tftp_server = tftp.TftpServer(SERVER_PATH)
tftp_server_th = th.Thread(target=tftp_server.listen, args=(IP, PORT))
tftp_server_th.start()
time.sleep(1)
tftp_client = tftp.TftpClient(IP, PORT)
tftp_client.download(REMOTE_FILE_NAME, CLIENT_PATH + "\\" + LOCAL_FILE_NAME)
time.sleep(1)
tftp_server.stop()
tftp_server_th.join(1)
my_file = Path(CLIENT_PATH + "\\" + LOCAL_FILE_NAME)
if my_file.is_file():
    print("result: PASS")
else:
    print("result: FAIL")
