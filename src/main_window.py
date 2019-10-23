from PySide2.QtWidgets import (QMainWindow, QWidget, QTextBrowser, QVBoxLayout,
        QPlainTextEdit, QPushButton, QAction, QMessageBox)
from PySide2.QtCore import Slot, Signal
from PySide2.QtGui import QCloseEvent
from help_browser import HelpBrowser


class MainWindow(QMainWindow):

    # This signal is emitted by overridden closeEvent function, when main window is closed.
    is_closing = Signal()

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle('Example of help browser')

        # Create a text example editor widget.
        main_widget = QWidget()
        main_widget.edit = QPlainTextEdit()
        main_widget.edit.appendPlainText( 'Code editor\nsome code' )

        # Layout main window widgets and apply to central widget.
        layout = QVBoxLayout()
        layout.addWidget(main_widget.edit)
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        # Setup example menu bar and its actions.
        self.create_actions()
        self.create_menus()


    def create_actions(self):
        self.new_action = QAction(self.tr('&New'), self)
        self.open_action = QAction(self.tr('&Open'), self)
        self.save_action = QAction(self.tr('&Save'), self)
        self.save_as_action = QAction(self.tr('Save as'), self)
        self.quit_action = QAction(self.tr('&Quit'), self)

        self.copy_action = QAction(self.tr('Copy'))
        self.paste_action = QAction(self.tr('Paste'))

        # Action to show documenation in help browser.
        self.documentation_action = QAction(self.tr('Dromedary &Documentation'),
                triggered=self.show_documentation)
        # Action to show examples in help browser.
        self.examples_action = QAction(self.tr('Dromedary &Examples'), triggered=self.show_examples)
        # Action to show welcome screen. You could have this show a QDialog that is also shown
        # when app launches, similar to Mathematica's welcome screen.
        self.welcome_action = QAction(self.tr('Welcome &Screen'), triggered=self.show_welcome)
        self.about_action = QAction(self.tr('&About'), triggered=self.about)

    def create_menus(self):
        # Create menu bar.
        self.file_menu = self.menuBar().addMenu(self.tr('&File'))
        self.file_menu.addAction(self.new_action)
        self.file_menu.addAction(self.open_action)
        self.file_menu.addAction(self.save_action)
        self.file_menu.addAction(self.save_as_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.quit_action)

        self.edit_menu = self.menuBar().addMenu('&Edit')
        self.edit_menu.addAction(self.copy_action)
        self.edit_menu.addAction(self.paste_action)

        self.help_menu = self.menuBar().addMenu(self.tr('&Help'))
        self.help_menu.addAction(self.documentation_action)
        self.help_menu.addAction(self.examples_action)
        # This seperator is not showing correctly in Linux, possibly Qt or PySide2 bug.
        self.help_menu.addSeparator()
        self.help_menu.addAction(self.welcome_action)
        self.help_menu.addAction(self.about_action)

    # Shows documentation page in help browser.
    def show_documentation(self):
        HelpBrowser.show_page('index.html', parent=self)

    # Shows examples page in help browser.
    def show_examples(self):
        HelpBrowser.show_page('examples.html', parent=self)

    # This could show welcome screen.
    def show_welcome(self):
        pass

    # Show about message box with app info.
    def about(self):
        msgbox = QMessageBox(self)
        msgbox.setText("About")
        msgbox.setInformativeText("Dromedary version 1.0 ...")
        msgbox.show()

    # Overrides close event, so that is_closing signals is emitted. This is needed so that when
    # main window closes, help browser also closes. Maybe this behavior is undesirable depending on
    # your preference.
    def closeEvent(self, event: QCloseEvent):
        # Emit custom is_closing slot.
        self.is_closing.emit()
