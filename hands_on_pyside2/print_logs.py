from queue import Queue
import threading
import time


class MessageQueue(object):
    def __init__(self):
        self.queue = dict()

    def create_queue(self, id):
        self.queue.update({id: Queue()})


class Session(object):
    def __init__(self, session_num, mq):
        self.s = session_num
        mq.create_queue(self.s)
        self.my_q = mq.queue[session_num]

    def print_log(self, log):
        time.sleep(0.1)
        if self.my_q.full():
            self.my_q.get()
            self.my_q.put(log)
        else:
            self.my_q.put(log)
        #print("gen[{}]: {}".format(self.s, log))


def screen_on(mq, timeout=300):
    _timeout = timeout
    while True:
        for k, v in mq.queue.items():
            time.sleep(0.1)
            if not v.empty():
                _timeout = timeout
                for _ in range(v.qsize()):
                    print("son[{}]: {}".format(k, v.get()))
            else:
                _timeout = _timeout - 1
        if _timeout < 1:
            break


if __name__=="__main__":
    with open("D:\\python_project\\python-lgu-sct\\sct\\example\\dev_logs.txt") as f:
        logs_data = f.readlines()

    mq = MessageQueue()
    session0 = Session("0", mq)
    session1 = Session("1", mq)
    print_th = threading.Thread(target=screen_on, args=(mq,))
    print_th.start()
    for log in logs_data:
        session0.print_log(log)
        session1.print_log(log)
    print_th.join()