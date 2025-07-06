from PySide6.QtWidgets import QDialog
from PySide6.QtGui import QIcon

from warmuppy.ui.dialogs.howtowindow import Ui_HowtoWindow


class HowtoWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.ui = Ui_HowtoWindow()
        self.setWindowIcon(QIcon(':/icons/icon.ico'))
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.accept)
