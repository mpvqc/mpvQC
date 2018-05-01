from os import path

from src.gui.uihandler.main import MainHandler
from src.settings import Settings


class Comment:

    def __init__(self, time: str, coty: str, note: str):
        self.time = time
        self.coty = coty
        self.note = note

    def __str__(self):
        return "[{}][{}] {}".format(self.time, self.coty, self.note)


class QualityCheck:

    def __init__(self, main_handler: MainHandler):
        self.main_handler = main_handler
        self.path_document: path = None

    @property
    def comments(self):
        return self.main_handler.widget_comments.get_all_comments()

    @property
    def qc_author(self):
        return Settings.Holder.NICKNAME.value

    @property
    def video_path(self):
        return self.main_handler.widget_mpv.mpv_player.video_file_current()

    @property
    def is_up_to_date(self):
        return self.main_handler.widget_comments.comments_up_to_date

    def should_save(self) -> bool:
        """
        Returns whether the QC should be saved in order to prevent data loss. In particular:

            1. Comments are available (not 0)
            2. Comment table changed

        :return: whether saving would be valuable
        """
        return bool(self.comments) and not self.is_up_to_date

    def save(self):
        self.main_handler.widget_comments.comments_up_to_date = True
        print("Will save as ", self.path_document)

        pass
