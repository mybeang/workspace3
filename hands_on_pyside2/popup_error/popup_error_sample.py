import asyncio
import logging, sys, time
import msvcrt as m
from sct.example.popup_error.ui import Ui_MainWindow
from PySide2 import QtWidgets, QtCore, QtGui


class MyTc(object):
    def __init__(self, log, popup, sleep):
        self.sleep_hdr = False
        self.log = log
        self.popup = popup
        self.sleep = sleep
        self.sleep.connect(self.update_sleep_hdr)

    def update_sleep_hdr(self, flags):
        self.sleep_hdr = flags

    def test(self):
        for i in range(20):
            logging.debug("Print on Terminal 1")
            self.log.emit("Print on Terminal 1")
            if i % 3 == 1:
                self.popup.emit("hello", 0)
                while True:
                    if not self.sleep_hdr:
                        time.sleep(1)
                    else:
                        break
            self.update_sleep_hdr(False)
            time.sleep(0.2)


class Th1(QtCore.QThread):
    log = QtCore.Signal(str)
    popup = QtCore.Signal(str, int)
    sleep = QtCore.Signal(bool)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.sleep_hdr = False
        self.add_tc()

    def update_sleep_hdr(self, flags):
        self.sleep_hdr = flags

    def add_tc(self):
        self.tc = MyTc(self.log, self.popup, self.sleep)

    def run(self):
        self.tc.test()


class Th2(QtCore.QThread):
    log = QtCore.Signal(str)

    def __init__(self, popup_msg):
        QtCore.QThread.__init__(self)
        self.popup_msg = popup_msg

    def run(self):
        for i in range(20):
            logging.debug("Print on Terminal 2")
            self.log.emit("Print on Terminal 2")
            if i % 3 == 1:
                self.popup_msg("hello")
            time.sleep(0.2)


class MainWD(Ui_MainWindow):
    def __init__(self):
        self.t1 = Th1()
        self.t2 = Th2(self.popup_msg)
        self.t1.log.connect(self.print_1)
        self.t2.log.connect(self.print_2)
        self.t1.popup.connect(self.pause_th)

    def popup_msg(self, msg, level=0):
        """
        :param msg: Message
        :param level: 0 == 'Info", 1 == 'Warning", 2 == 'Critical'
        """
        logging.debug("func: popup_msg({}, {})".format(msg, level))
        _level = [QtWidgets.QMessageBox.Information,
                  QtWidgets.QMessageBox.Warning,
                  QtWidgets.QMessageBox.Critical]
        msg_box = QtWidgets.QMessageBox()
        if level == 0:
            msg_box.setWindowTitle("INFO")
        elif level == 1:
            msg_box.setWindowTitle("WARNING")
        else:
            msg_box.setWindowTitle("CRITICAL")
        msg_box.setText(msg)
        msg_box.setIcon(_level[level])
        msg_box.exec_()
        del msg_box
        return True

    def pause_th(self, msg, level=0):
        res = self.popup_msg(msg, level)
        self.t1.sleep.emit(res)

    def start_1(self):
        self.t1.start()

    def start_2(self):
        self.t2.start()

    def print_1(self, string):
        self.TE_1.append(string)

    def print_2(self, string):
        self.TE_2.append(string)


if __name__=="__main__":
    logger = logging.getLogger()
    fmt = "[%(levelname)s] %(msg)s"
    log_level = logging.DEBUG
    logger.setLevel(log_level)
    hdl = logging.StreamHandler(sys.stdout)
    fmtter = logging.Formatter(fmt)
    hdl.setFormatter(fmtter)
    logger.addHandler(hdl)

    app = QtWidgets.QApplication(sys.argv)
    ui = MainWD()
    win = QtWidgets.QMainWindow()
    ui.setupUi(win)
    ui.retranslateUi(win)
    ui.PB_1.clicked.connect(ui.start_1) # after change code, verify this button.
    ui.PB_2.clicked.connect(ui.start_2) # this is button which is made by previous code.

    win.show()
    sys.exit(app.exec_())
