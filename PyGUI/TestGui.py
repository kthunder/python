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
        menu_control = self.menuBar().addMenu("Contorl")
        act_quit = menu_control.addAction("quit")
        act_quit.triggered.connect(self.close)


myapp = QApplication(sys.argv)
mywidget = MyWidget()
mywidget.show()
mywidget.statusBar().showMessage("程序已就绪...")
sys.exit(myapp.exec_())
