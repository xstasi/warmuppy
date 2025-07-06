import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QShortcut, QKeySequence

from warmuppy.ui.warmuppy_window import WarmuppyWindow
from warmuppy.constants import APPLICATION_NAME


def main():
    app = QApplication([])
    QCoreApplication.setOrganizationName(APPLICATION_NAME)
    QCoreApplication.setApplicationName(APPLICATION_NAME)
    widget = WarmuppyWindow()
    widget.show()
    sys.exit(app.exec_())
