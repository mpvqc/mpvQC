from PyQt5 import QtCore


class __T:
    """
    This file is only present to make the translation process easier.
    Each string passed to the '_translate' function will be recognized by pylupdate5 when generating the .ts file.
    """

    def __init__(self):
        # Comment Types
        _translate = QtCore.QCoreApplication.translate

        # Author
        _translate("Misc", "Type here to change the nick name")

        # Comment types
        _translate("Misc", "Translation")
        _translate("Misc", "Punctuation")
        _translate("Misc", "Spelling")
        _translate("Misc", "Phrasing")
        _translate("Misc", "Timing")
        _translate("Misc", "Typeset")
        _translate("Misc", "Note")
        _translate("Misc", "Type here to add new comment types")
        _translate("Misc", "Add")
        _translate("Misc", "Remove")
        _translate("Misc", "Move Up")
        _translate("Misc", "Move Down")

        # Message Widget
        _translate("Misc", "Each comment type needs a valid name")
        _translate("Misc", "At least one comment type is required")
        _translate("Misc", "Nick name must not be empty")

        # Alert & Dialog ############################################################################# Alert & Dialog #
        _translate("Misc", "Yes")
        _translate("Misc", "No")

        # Dialog: Open Video
        _translate("Misc", "Open Video File")
        _translate("Misc", "Video files (*.mkv *.mp4);;All files (*.*)")

        # Alert: Configuration has changed
        _translate("Misc", "Discard changes?")
        _translate("Misc", "Your configuration has changed.")
