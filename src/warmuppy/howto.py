from PySide2.QtWidgets import QDialog
from PySide2.QtGui import QIcon

from warmuppy.ui.howto import Ui_Howto


class howtowindow(QDialog):
    def __init__(self, parent=None):
        super(howtowindow, self).__init__()
        self.ui = Ui_Howto()
        self.setWindowIcon(QIcon(':/icons/icon.ico'))
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.accept)
