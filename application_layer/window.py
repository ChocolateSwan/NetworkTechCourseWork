from PyQt5 import QtGui
import PyQt5.QtWidgets


class Form1(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.button1.clicked.connect(self.handleButton)
        self.window2 = None

    def handleButton(self):
        if self.window2 is None:
            self.window2 = Form2(self)
        self.window2.show()

class Form2(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Form1()
    window.show()
    sys.exit(app.exec_())
