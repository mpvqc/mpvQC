# mpvQC
#
# Copyright (C) 2020 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from PyQt5.QtWidgets import QMessageBox

from src import get_settings
from src.uiutil import dialogs, messageboxes


class Comment:
    """
    A representation of a comment line.
    """

    def __init__(self, comment_time, comment_type, comment_note):
        self.comment_time = comment_time
        self.comment_type = comment_type
        self.comment_note = comment_note

    def __str__(self):
        return "[{}] [{}] {}".format(self.comment_time, self.comment_type, self.comment_note)

    def __eq__(self, other):
        if isinstance(other, Comment):
            return self.comment_time == other.comment_time \
                   and self.comment_type == other.comment_type \
                   and self.comment_note == other.comment_note
        return False


class QcManager(QObject):

    # Signal, that indicates a state change. p1='new state (saved/unsaved)'
    state_changed = pyqtSignal(bool)

    # Signal, that indicates a new video import. p1='new video path'
    video_imported = pyqtSignal(str)

    def __init__(self, window, video_widget, table_widget):
        """
        The qc manager will take care of the state of the current video and documents.

        :param window: the application window
        :param video_widget: a reference to the video widget (not the player!)
        :param table_widget: a reference to the table widget
        """

        super(QcManager, self).__init__()

        # Widgets
        self.__a = window
        self.__t = table_widget
        self.__m = video_widget

        self.__t.comments_changed.connect(lambda x, y=self.on_table_content_modified: y())

        # State
        from src.manager._states import get_initial_state, Signals
        Signals.video_imported.connect(lambda video: self.video_imported.emit(video))

        self.__state = get_initial_state()
        self.__state_last_saved = self.__state
        self.__during_state_change = False

        # Auto save
        self.__auto_save_timer = None
        self.reset_auto_save()

    def on_table_content_modified(self, *_):
        """
        Called after the table content changed
        """

        if not self.__during_state_change:
            # Filling the table during a state change causes this method (event) being fired
            # So we block it to avoid multiple state change events
            self.__before_stage_change()
            self.__state = self.__state.on_comments_modified(self.__t)
            self.__after_state_change()

    def has_changes(self) -> bool:
        return self.__state.has_changes

    def request_new_document(self):
        """
        Called when the user presses the 'New' button
        """

        self.__before_stage_change()
        self.__state = self.__state.on_create_new_document(self.__a, self.__t, self.__m)
        self.__after_state_change()

    def request_open_qc_documents(self):
        """
        Called when the user presses the 'Open' button and then selects the documents to import
        """

        paths = dialogs.get_open_file_names(self.__a)

        self.__before_stage_change()
        self.__state = self.__state.on_import(docs=paths, vids=None, subs=None, a=self.__a, t=self.__t, m=self.__m)
        self.__after_state_change()

    def request_open_video(self):
        """
        Called when the user presses the 'Open' button and then selects the videos to import
        """

        vid = dialogs.get_open_video(self.__a)
        vids = [vid] if vid else None

        self.__before_stage_change()
        self.__state = self.__state.on_import(docs=None, vids=vids, subs=None, a=self.__a, t=self.__t, m=self.__m)
        self.__after_state_change()

    def request_open_subtitles(self):
        """
        Called when the user presses the 'Open' button and then selects the subtitles to import
        """

        subs = dialogs.get_open_subs(self.__a)

        self.__before_stage_change()
        self.__state = self.__state.on_import(docs=None, vids=None, subs=subs, a=self.__a, t=self.__t, m=self.__m)
        self.__after_state_change()

    def request_save_qc_document(self):
        """
        Called when the user presses the 'Save' button
        """

        self.__before_stage_change()
        self.__state = self.__state.on_save_pressed(self.__a, self.__t, self.__m)
        self.__after_state_change()

    def request_save_qc_document_as(self):
        """
        Called when the user presses the 'Save As...' button
        """

        self.__before_stage_change()
        self.__state = self.__state.on_save_as_pressed(self.__a, self.__t, self.__m)
        self.__after_state_change()

    def request_quit_application(self):
        """
        Asks the manager whether there are unsaved changes.

        :return: True if quit, False else
        """

        if not self.__state.has_changes:
            return True

        self.__m.player.pause()

        do_quit = messageboxes.QuitNotSavedMB().exec_()
        if do_quit == QMessageBox.Yes:  # Still leave
            return True
        return False

    def do_open_drag_and_drop_data(self, vids, docs, subs):
        """
        Opens the given videos, text documents and subtitle documents.
        If a video is passed in, the passed in video will be preferred over videos found in documents.

        :param vids: a list with paths pointing to video files
        :param docs: a list with paths pointing to qc documents files
        :param subs: a list with paths pointing to subtitles
        """

        self.__before_stage_change()
        self.__state = self.__state.on_import(docs, vids, subs, self.__a, self.__t, self.__m)
        self.__after_state_change()

    def reset_auto_save(self):
        """
        Sets up/resets auto save timer
        """

        def __do_auto_save():
            """
            Function which triggers auto save
            """

            self.__state.on_write_auto_save(self.__a, self.__t, self.__m)
            return True

        if self.__auto_save_timer is not None:
            self.__auto_save_timer.stop()

        s = get_settings()
        interval = s.backup_interval

        if s.backup_enabled and interval >= 15:
            self.__auto_save_timer = QTimer()
            self.__auto_save_timer.timeout.connect(__do_auto_save)
            self.__auto_save_timer.start(interval * 1000)

    def __before_stage_change(self):
        """
        Requires to be called before any state change originated from a user action except table changes
        """

        self.__during_state_change = True

    def __after_state_change(self):
        """
        Called after the state has changed
        """

        if not self.__state.has_changes:
            self.__state_last_saved = self.__state.copy()
        else:

            matches_last_save = self.__state_last_saved is not None \
                                and self.__state_last_saved.has_same_content_as(self.__state)
            if matches_last_save:
                self.__state = self.__state_last_saved

        self.state_changed.emit(self.__state.has_changes)

        self.__during_state_change = False
