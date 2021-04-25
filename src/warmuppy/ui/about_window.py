from PySide2.QtWidgets import QDialog
from PySide2.QtGui import QIcon

from warmuppy.ui.dialogs.aboutwindow import Ui_AboutWindow

from warmuppy.constants import APPLICATION_VERSION, APPLICATION_NAME


class AboutWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_AboutWindow()
        self.setWindowIcon(QIcon(':/icons/icon.ico'))
        self.ui.setupUi(self)
        self.ui.labelNameVersion.setText(
            f"{APPLICATION_NAME} {APPLICATION_VERSION}"
        )
        self.ui.pushButton.clicked.connect(self.accept)
