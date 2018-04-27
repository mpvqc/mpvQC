from PyQt5.QtWidgets import QTableView, QStatusBar, QApplication


class References:
    """
    A holder class for all important widgets in the application.

    All referenced values have in common that:
        * all values are set in the ApplicationWindow.__init__ method
        * all values are final

    Although it is bad style, I find it to be easier in this small application to pass an object instead of six.
    """

    def __init__(self):
        from src.player.widgets import MpvWidget
        from src.player.players import MpvPlayer
        from start import ApplicationWindow

        self.__application: QApplication
        self.__widget_main: ApplicationWindow
        self.__widget_mpv: MpvWidget
        self.__widget_comments: QTableView
        self.__player: MpvPlayer
        self.__widget_status_bar: QStatusBar

    @property
    def application(self) -> QApplication:
        """
        :return: The Qt application currently running.
        """

        return self.__application

    @application.setter
    def application(self, value):
        self.__application = value

    @property
    def widget_main(self):
        """
        :return: The main container of this application the mpv- and comments widgets are located in.
        """

        return self.__widget_main

    @widget_main.setter
    def widget_main(self, value):
        self.__widget_main = value

    @property
    def widget_mpv(self):
        """
        :return: The mpv widget the player is located in.
        """

        return self.__widget_mpv

    @widget_mpv.setter
    def widget_mpv(self, value):
        self.__widget_mpv = value

    @property
    def widget_comments(self):
        """
        :return: The comments widget.
        """

        return self.__widget_comments

    @widget_comments.setter
    def widget_comments(self, value):
        self.__widget_comments = value

    @property
    def player(self):
        """
        :return: The mpv player.
        """

        return self.__player

    @player.setter
    def player(self, value):
        self.__player = value

    @property
    def widget_status_bar(self) -> QStatusBar:
        return self.__widget_status_bar

    @widget_status_bar.setter
    def widget_status_bar(self, value):
        self.__widget_status_bar = value
