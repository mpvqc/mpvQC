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
from PyQt5.QtWidgets import QDialog

from src.gui.generated.about import Ui_AboutDialog

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

        import platform

        from src import get_metadata
        md = get_metadata()

        self.__ui.aboutTextBrowser.setHtml(ABOUT.format(
            version=md.app_version,
            platform=platform.architecture()[0],
            app_name=md.app_name,
            version_mpv=self.VERSION_MPV,
            version_ffmpeg=self.VERSION_FFMPEG,
            years="2016-2018")
        )
