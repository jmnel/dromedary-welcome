import os
from PySide2.QtWidgets import (QWidget, QPushButton, QTextBrowser, QHBoxLayout, QVBoxLayout,
        QDialog)
from PySide2.QtCore import Qt, Slot

class HelpBrowser(QWidget):

    instance = None         # Class variable instance of help browser
    documentation_path = '' # Documentation path

    def __init__(self, parent=None):
#    def __init__(self, path, page, parent=None):
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

        # Calls static function to clear help browser instance reference.
        self.destroyed.connect(HelpBrowser.on_close)

        # Close help browser on parent is_closing signal.
        parent.is_closing.connect(self.close)

    # Navigates to page in documentation path.
    def goto_page(self, page):
        page_file_path = os.path.join(HelpBrowser.documentation_path, page)
        self.text_browser.setSource(page_file_path)

    # Sets documenation path.
    @staticmethod
    def set_documentation_path(path):
        HelpBrowser.documentation_path = path

    # Unsets help browser instance reference. This gets called when help browser is destroyed.
    @staticmethod
    def on_close():
        if HelpBrowser.instance != None:
            HelpBrowser.instance = None

    # Creates and shows help browser window, stores instance in class variable, and navigates to
    # page in documentation path.
    @staticmethod
    def show_page(page, parent=None):
        if HelpBrowser.instance == None:
            HelpBrowser.instance = HelpBrowser(parent)
            HelpBrowser.instance.resize(500,400)

        HelpBrowser.instance.show()
        HelpBrowser.instance.goto_page(page)
