import os
from PySide2.QtWidgets import (QWidget, QPushButton, QTextBrowser, QHBoxLayout, QVBoxLayout,
        QDialog)
from PySide2.QtCore import Qt, Slot

browser = None  # Global reference to help browser instance

class HelpBrowser(QWidget):

    def __init__(self, path, page, parent=None):
        # We don't pass parent to superclass, because we don't want help browser to be a child of
        # main window. We handle closing help browser when main window closes manually.
        super(HelpBrowser,self).__init__()

        # Set needed widget attributes. WA_DeleteOnClose is needed so that closing main window also
        # closes instance of help browser.
        self.setAttribute(Qt.WA_DeleteOnClose)  # Destroy widget when window is closed.
        self.setAttribute(Qt.WA_GroupLeader)

        # Create home, back, and close buttons.
        self.home_button = QPushButton(self.tr('&Home'))
        self.back_button = QPushButton(self.tr('&Back'))
        self.close_button = QPushButton(self.tr('Close'))
        self.close_button.setShortcut(self.tr('Esc'))

        # Layout home, back, and close buttons.
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.home_button)
        self.button_layout.addWidget(self.back_button)
        self.button_layout.addStretch()
        self.button_layout.addWidget(self.close_button)


        # Create basic layout containing QTextBrowser.
        self.text_browser = QTextBrowser()
        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.addWidget(self.text_browser)
        self.setLayout(self.main_layout)

        # Connect button signals
        self.home_button.clicked.connect(self.text_browser.home)
        self.back_button.clicked.connect(self.text_browser.backward)
        self.close_button.clicked.connect(self.close)

        # Calls static function to clear global help browser instance reference.
        self.destroyed.connect(HelpBrowser.on_close)

        # Get path of page and open it.
        file_path_abs = path + '/' + page
        self.text_browser.setSearchPaths(path)  # Not sure if this is needed
        self.text_browser.setSource(file_path_abs)

        # Close help browser on parent is_closing signal.
        parent.is_closing.connect(self.close)

    # Unsets global help browser instance reference. This gets called when help browser is
    # destroyed.
    @staticmethod
    def on_close():
        global browser
        browser = None

    # Creates help browser window as global object.
    @staticmethod
    def show_page( page, parent=None ):
        # Get absolute path to 'docs' subdirectory.
        path = os.path.abspath('docs/')
        global browser
        # Check that help browser doesn't already exist.
        if browser == None:
            # Create help browser and show it.
            browser = HelpBrowser(path, page, parent)
            browser.resize(500, 400)
            browser.show()
        else:
            # Browser already open, so just change page.
            file_path_abs = path + '/' + page
            browser.text_browser.setSearchPaths(path)
            browser.text_browser.setSource(file_path_abs)
