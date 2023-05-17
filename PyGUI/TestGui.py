import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 800, 600)
        self.resize(400, 300)
        # 坐标0 0 大小800 600
        self.setWindowTitle("myapp")
        self.setToolTip("ToolTip")
        QToolTip.setFont(QFont("微软雅黑", 12))
        menu_control = self.menuBar().addMenu("Menu")
        act_quit = menu_control.addAction("Action-Quit")
        act_quit.triggered.connect(self.close)

        self.statusBar().showMessage("程序已就绪...")
        self.show()


myapp = QApplication(sys.argv)
widget = MyWidget()
sys.exit(myapp.exec_())
