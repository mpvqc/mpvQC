from typing import Set

from PyKF5.KWidgetsAddons import KMessageWidget


class MessageWidget:
    """ A small wrapper for the KDE KMessage Widget."""

    def __init__(self, message_widget: KMessageWidget):
        self.message_widget = message_widget
        self.message_widget_messages: Set[str] = set()
        self.__update_widget()

    def add_message(self, message: str):
        """Adds a new message. Displays the message immediately."""

        self.message_widget_messages.add(message)
        self.__update_widget()

    def remove_message(self, message: str):
        """Removes the passed message immediately."""

        if message in self.message_widget_messages:
            self.message_widget_messages.remove(message)
            self.__update_widget()

    def clear(self):
        """Clears all messages immediately."""

        self.message_widget_messages.clear()
        self.__update_widget()

    def __update_widget(self):
        """Changes the text of the KMessageWidget."""

        new_text = "\n".join(set(self.message_widget_messages))
        print(new_text)
        self.message_widget.setText(new_text)
        if self.message_widget_messages:
            self.message_widget.show()
        else:
            self.message_widget.hide()
