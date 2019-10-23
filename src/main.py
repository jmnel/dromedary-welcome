import sys
import os
from PySide2.QtWidgets import QApplication
from main_window import MainWindow
from help_browser import HelpBrowser

if __name__ == '__main__':
    app = QApplication(sys.argv)
    root_window = MainWindow()
    root_window.show()

    # Get the directory of main.py and set documentation directory for help browser.
    script_path = os.path.dirname(os.path.realpath(__file__))
    documentation_subdirectory = 'docs'
    HelpBrowser.set_documentation_path(os.path.join( script_path, documentation_subdirectory))

    # Launch application.
    sys.exit(app.exec_())
