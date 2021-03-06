import sys

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QCoreApplication

from warmuppy.ui.warmuppy_window import WarmuppyWindow
from warmuppy.constants import APPLICATION_NAME


def main():
    app = QApplication([])
    QCoreApplication.setOrganizationName(APPLICATION_NAME)
    QCoreApplication.setApplicationName(APPLICATION_NAME)
    widget = WarmuppyWindow()
    widget.show()
    sys.exit(app.exec_())
