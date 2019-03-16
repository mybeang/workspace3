import PySide2
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
from time import sleep
import sys
from multiprocessing import Queue

from pathlib import Path


OPENFILE = Path(__file__).parent.joinpath("conf.txt")
STOP_LED = Path(__file__).parent.parent.joinpath('data').joinpath("uidata").joinpath("re_led_black.png")
RUN_LED = Path(__file__).parent.parent.joinpath('data').joinpath("uidata").joinpath("re_led_blue.png")


def start_test(led):
    led.start()
    q = Queue(maxsize=10)
    with open(OPENFILE, "r") as f:
        strings = f.readlines()
    for string in strings:
        if q.full():
            q.get()
        q.put(string)
        sleep(0.1)
    led.finish()
    return q


class Tester(QtCore.QThread):
    test_signal = QtCore.Signal(int)
    flags = False
    def __init__(self, led):
        QtCore.QThread.__init__(self)
        self.led = led

    def run(self):
        self.flags = True
        self.start_test()
        print("oh no")
        self.flags = False

    def start_test(self):
        self.led.start()
        with open(OPENFILE, "r") as f:
            strings = f.readlines()
        for string in strings:
            if q.full():
                q.get()
            q.put(string)
            sleep(0.1)
        self.led.finish()


class Worker(QtCore.QThread):
    job_sig = QtCore.Signal(str)
    flags = False

    def __init__(self, terminal):
        QtCore.QThread.__init__(self)
        self.terminate = terminal

    def run(self):
        self.print_out()

    def print_out(self):
        self.flags = True
        while self.flags:
            sleep(0.1)
            if not q.empty():
                for _ in range(q.qsize()):
                    string = q.get()
                    self.job_sig.emit(string)


class _ConsoleUI(object):
    def setupUI(self, window):
        self.terminal_head = QtWidgets.QLabel("Terminal Monitor", parent=window)
        self.terminal_head.setGeometry(10, 10, 480, 15)
        self.terminal_head.setStyleSheet("font-size: 12px; align-content: center; font-weight: bold")

        self.terminal = QtWidgets.QTextEdit(parent=window)
        self.terminal.setGeometry(10, 35, 780, 300)

        self.terminal.setStyleSheet("background-color: black; "
                                    "color: white; "
                                    "font-size: 10px; "
                                    "font-family: Courier New")
        self.terminal.setReadOnly(True)

        self.clear_bt = QtWidgets.QPushButton("Clear Screen", parent=window)
        self.clear_bt.setGeometry(10, 350, 100, 20)


class ConsoleWindow(_ConsoleUI):
    def __init__(self, parent=None):
        self.window = QtWidgets.QWidget(parent=parent)
        self.window.setObjectName("window")
        self.window.resize(800, 400)
        self.window.setWindowTitle("Ternimal Window")
        self.setupUI(self.window)
        self.worker = Worker(self.terminal)
        self.worker.job_sig.connect(self.print_out)
        self.clear_bt.clicked.connect(self.clear_screen)

    def print_out(self, string):
        self.terminal.append(str(string).strip())
        self.terminal.moveCursor(QtGui.QTextCursor.End)

    def clear_screen(self):
        self.terminal.clear()


class LEDStatus(QtCore.QThread):
    def __init__(self, led_obj):
        QtCore.QThread.__init__(self)
        self.led_obj = led_obj
        stop_led = QtGui.QPixmap(str(STOP_LED))
        self.stop_led = stop_led.scaled(25, 25, QtCore.Qt.KeepAspectRatio)
        run_led = QtGui.QPixmap(str(RUN_LED))
        self.run_led = run_led.scaled(25, 25, QtCore.Qt.KeepAspectRatio)

    def run(self):
        while True:
            self.led_obj.setPixmap(self.run_led)
            sleep(1)
            self.led_obj.setPixmap(self.stop_led)
            sleep(1)

    def finish(self):
        self.led_obj.setPixmap(self.stop_led)
        self.terminate()


class MainUI(object):

    def setupUI(self, window):
        window.setObjectName("window")
        window.resize(400, 100)
        window.setWindowTitle("Ternimal Window")
        self.console_flag = False
        self.popup_button = QtWidgets.QPushButton("Popup", parent=window)
        self.popup_button.setGeometry(10, 10, 50, 20)
        self.start_test_bt = QtWidgets.QPushButton("Start Test", parent=window)
        self.start_test_bt.setGeometry(10, 50, 100, 20)
        self.console = ConsoleWindow()
        self.led_status = QtWidgets.QLabel("", parent=window)
        self.led_status.setGeometry(150, 50, 25, 25)
        qimg = QtGui.QPixmap(str(STOP_LED))
        qimg = qimg.scaled(25, 25, QtCore.Qt.KeepAspectRatio)
        self.led_status.setPixmap(qimg)

    def popup(self):
        if not self.console.window.isVisible():
            self.console.window.show()
            if not self.console.worker.isRunning():
                self.console.worker.start()
        else:
            self.console.window.close()

    def start_test(self):
        print("start_test")
        if not hasattr(self, 'status_display'):
            self.status_display = LEDStatus(self.led_status)
        if not hasattr(self, 'tester'):
            self.tester = Tester(self.status_display)
        print("_testing")
        print(self.tester.flags)
        if not self.tester.flags:
            print("run test")
            self.tester.start()
            print(self.tester.flags)
        else:
            print("end test")
            self.tester.terminate()
            del self.tester
            del self.status_display
        if not self.console.worker.isRunning():
            self.console.worker.start()

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()
    ui = MainUI()
    ui.setupUI(window)
    ui.popup_button.clicked.connect(ui.popup)
    ui.start_test_bt.clicked.connect(ui.start_test)
    window.show()
    sys.exit(app.exec_())

