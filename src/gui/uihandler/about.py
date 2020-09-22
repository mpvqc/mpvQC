# Copyright (C) 2016-2017 Frechdachs <frechdachs@rekt.cc>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QPushButton, QAbstractItemView

from src.gui.generated.about import Ui_AboutDialog
from src.gui.generated.editCommentTypes import Ui_editCommentTypeDialog

_translate = QCoreApplication.translate


class AboutDialog(QDialog):
    VERSION_MPV = ""
    VERSION_FFMPEG = ""

    def __init__(self):
        super().__init__()
        self.__ui = Ui_AboutDialog()
        self.__ui.setupUi(self)

        from src import CREDITS, LICENCE, ABOUT

        self.__ui.creditsTextBrowser.setTextInteractionFlags(Qt.NoTextInteraction)
        self.__ui.creditsTextBrowser.setHtml(CREDITS)
        self.__ui.licenceTextBrowser.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.__ui.licenceTextBrowser.setHtml(LICENCE)

        self.__ui.aboutTextBrowser.setOpenExternalLinks(True)
        self.__ui.aboutTextBrowser.setTextInteractionFlags(Qt.LinksAccessibleByMouse)

        from start import APPLICATION_VERSION
        import platform
        from start import APPLICATION_NAME

        self.__ui.aboutTextBrowser.setHtml(ABOUT.format(
            version=APPLICATION_VERSION,
            platform=platform.architecture()[0],
            app_name=APPLICATION_NAME,
            version_mpv=self.VERSION_MPV,
            version_ffmpeg=self.VERSION_FFMPEG,
            years="2016-2018")
        )
