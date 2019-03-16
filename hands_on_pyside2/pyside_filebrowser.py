from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
import sys
from os.path import expanduser

ICON = "D:\\python_project\\python-lgu-sct\\sct\\data\\uidata\\folder.png"


class UI(object):
    def setupUI(self, window):
        window.setObjectName("window")
        window.resize(300, 70)
        self.label = QtWidgets.QLabel("File", parent=window)
        self.label.setGeometry(10, 10, 20, 20)
        self.text = QtWidgets.QLineEdit("", parent=window)
        self.text.setGeometry(40, 10, 200, 20)
        self.button = QtWidgets.QPushButton(icon=QtGui.QIcon(ICON), parent=window)
        self.button.setGeometry(250, 10, 20, 20)
        self.button.setStyleSheet("background: transparent;")
        self.exit = QtWidgets.QPushButton("Exit", parent=window)
        self.exit.setGeometry(10, 40, 50, 20)
        QtCore.QMetaObject.connectSlotsByName(window)

    def open_file(self):
        fileDialog = QtWidgets.QFileDialog()
        #self.fileDialog.setFileMode(QtCore.QObject.tr("asdfasfd"))

        file_name = QtWidgets.QFileDialog.getSaveFileName(fileDialog,
                                                               "Open a foler",
                                                               expanduser("~"))[0]
        print(file_name)
        self.text.setText(QtWidgets.QApplication.translate("window", file_name, None, -1))


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QWidget()
    ui = UI()
    ui.setupUI(window)
    window.show()
    ui.button.clicked.connect(ui.open_file)
    ui.exit.clicked.connect(app.exit)
    sys.exit(app.exec_())