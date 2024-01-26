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


from PyQt5.QtCore import QPoint, QCoreApplication
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QMenu

from mpvqc import get_settings
from mpvqc.uihandler import MainHandler


class ContextMenu(QMenu):
    """
    Pseudo context menu when user right clicks into the video or presses the 'e' button and if video is loaded.
    """

    def __init__(self, main_handler: MainHandler):
        super().__init__()
        self.__main_handler = main_handler
        self.__widget_comments = main_handler.widget_comments
        self.__mpv_player = main_handler.widget_mpv.player
        self.update_entries()

    def update_entries(self):
        """
        Will update the entries of this context menu to match the comment types from the settings.
        """

        self.clear()

        ct_list = get_settings().comment_types
        if not ct_list:
            no_ct_action = QCoreApplication.translate("CommentTypes",
                                                      "No comment types defined." + " " + "Define new comment types in the settings.")
            ac = self.addAction(no_ct_action)
            ac.setEnabled(False)
        else:
            for ct in ct_list:
                act = self.addAction(ct)
                act.triggered.connect(lambda x, t=ct, f=self.__widget_comments.add_comment: f(t))

    def exec_(self):
        """
        Will display the menu with comment types.
        """

        self.__mpv_player.pause()
        self.__main_handler.display_normal()

        m_pos = QCursor.pos()

        # Fixes following: Qt puts the context menu in a place
        # where double clicking would trigger the fist menu option
        # instead of just calling the menu a second time
        # or ignoring the second press
        super().exec_(QPoint(m_pos.x() + 1, m_pos.y()))
