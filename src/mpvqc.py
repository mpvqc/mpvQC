import inspect

from src import configuration


# noinspection PyMethodMayBeStatic
class MpvActionHandler:

    def __init__(self):
        self.config = configuration.get_config()

    def on_pressed_new_qc_document(self):
        print(inspect.stack()[0][3])

    def on_pressed_open_qc_document(self):
        print(inspect.stack()[0][3])

    def on_pressed_save_qc_document(self):
        print(inspect.stack()[0][3])

    def on_pressed_save_qc_document_as(self):
        print(inspect.stack()[0][3])

    def on_pressed_exit(self):
        print(inspect.stack()[0][3])

    def on_pressed_open_video(self):
        print(inspect.stack()[0][3])

    def on_pressed_open_network_stream(self):
        print(inspect.stack()[0][3])

    def on_pressed_resize_video(self):
        print(inspect.stack()[0][3])

    def on_pressed_settings(selF):
        print(inspect.stack()[0][3])

    def on_pressed_check_for_update(self):
        print(inspect.stack()[0][3])

    def on_pressed_about_qt(self):
        print(inspect.stack()[0][3])

    def on_pressed_about_mpvqc(self):
        print(inspect.stack()[0][3])
