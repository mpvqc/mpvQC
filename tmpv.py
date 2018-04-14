import sys

from PyQt5.QtWidgets import QMainWindow, QWidget, QSplitter, QApplication

from src.config.menubarJsonConfig import MenubarJsonConfig, MenuBarLoader, MenuBarActionInvoke


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        topmenubar = self.menuBar()

        loader = MenuBarLoader(MenuBarActionInvoke(), self)

        for menu in loader.load_menu_bar():
            topmenubar.addMenu(menu)

        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("PyQT tuts!")

        self.show()


if __name__ == "__main__":
    # json_config_loader = MenubarJsonConfig()
    #
    # factions = json_config_loader.menubar_file
    # vactions = json_config_loader.menubar_video
    # oactions = json_config_loader.menubar_options
    # hactions = json_config_loader.menubar_help
    #
    # for faction in hactions:
    #     print(faction.key_action)

    app = QApplication(sys.argv)
    GUI = MainWindow()
    app.exec_()
