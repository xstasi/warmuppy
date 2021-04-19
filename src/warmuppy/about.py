from PySide2.QtWidgets import QDialog
from PySide2.QtGui import QIcon

from warmuppy.ui.about import Ui_About
from warmuppy.constants import APPLICATION_VERSION, APPLICATION_NAME


class aboutwindow(QDialog):
    def __init__(self, parent=None):
        super(aboutwindow, self).__init__()
        self.ui = Ui_About()
        self.setWindowIcon(QIcon(':/icons/icon.ico'))
        self.ui.setupUi(self)
        self.ui.labelNameVersion.setText(
            f"{APPLICATION_NAME} {APPLICATION_VERSION}"
        )
        self.ui.pushButton.clicked.connect(self.accept)
