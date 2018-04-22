from abc import ABC, abstractmethod
from typing import List

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QMessageBox, QDialogButtonBox, QLineEdit, QListView, QAbstractItemView

from src import configuration
from src.gui.preferences import Ui_Dialog
from src.preferences.messageWidget import MessageWidget

_tr = _translate = QtCore.QCoreApplication.translate


#  from PyKF5.KWidgetsAddons import KEditListWidget, KMessageWidget


class PreferenceDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.config = configuration.get_config()
        self.ui: Ui_Dialog = Ui_Dialog()
        self.ui.setupUi(self)

        set_fac = SettingsFactory(ui=self.ui, config=self.config, message_widget=MessageWidget(self.ui.kmessagewidget))
        self.nickname_settings: NickNameSettingEntry = set_fac.nickname_settings
        self.commenttypes_settings: CommentTypeSettingEntry = set_fac.commenttypes_settings
        self.autosave_settings: AutoSaveSettingsEntry = set_fac.autosave_settings
        self.write_vid_path_to_file: QcDocumentWriteVideoPathToFile = set_fac.write_vid_path_to_file
        self.write_nick_tofile: QcDocumentWriteNickNameToFile = set_fac.write_nick_to_file

        self.all_settings: List[AbstractSettingEntry] = [self.nickname_settings,
                                                         self.commenttypes_settings,
                                                         self.autosave_settings,
                                                         self.write_vid_path_to_file,
                                                         self.write_nick_tofile]

        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)

        self.__setup()

    def __setup(self):
        for s in self.all_settings:
            s.prepare()
            s.insert()
            s.bind_to_accept_button(self.__update_accept_button_state)

    def __is_data_valid(self) -> bool:
        valid: bool = True
        for s in self.all_settings:
            if not s.is_valid():
                valid = False
        return valid

    def __has_changed(self) -> bool:
        return any(x for x in self.all_settings if x.has_changed())

    def __update_accept_button_state(self):
        valid_ = self.__has_changed() and self.__is_data_valid()
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(valid_)
        pass

    def mousePressEvent(self, mouse_ev: QtGui.QMouseEvent):
        self.commenttypes_settings.remove_focus()
        super().mousePressEvent(mouse_ev)

    def accept(self):
        for s in self.all_settings:
            s.update_config()

        self.config.save()
        super().accept()

    def reject(self):
        if self.__has_changed():
            q = QMessageBox()
            q.setText(_tr("Misc", "Your configuration has changed.") + " " + _tr("Misc", "Discard changes?"))
            q.setIcon(QMessageBox.Warning)
            q.setWindowTitle(_tr("Misc", "Discard changes?"))
            q.addButton(_tr("Misc", "Yes"), QMessageBox.YesRole)
            q.addButton(_tr("Misc", "No"), QMessageBox.NoRole)

            if not q.exec_():
                super().reject()
        else:
            super().reject()


class SettingsFactory:

    def __init__(self, ui: Ui_Dialog, config, message_widget):
        self.nickname_settings: NickNameSettingEntry = NickNameSettingEntry(ui, config, message_widget)
        self.commenttypes_settings: CommentTypeSettingEntry = CommentTypeSettingEntry(ui, config, message_widget)
        self.autosave_settings: AutoSaveSettingsEntry = AutoSaveSettingsEntry(ui, config, message_widget)
        self.write_vid_path_to_file: QcDocumentWriteVideoPathToFile = QcDocumentWriteVideoPathToFile(ui, config,
                                                                                                     message_widget)
        self.write_nick_to_file: QcDocumentWriteNickNameToFile = QcDocumentWriteNickNameToFile(ui, config,
                                                                                               message_widget)


class AbstractSettingEntry(ABC):

    def __init__(self, ui: Ui_Dialog, config, message_widget):
        super().__init__()
        self.ui = ui
        self.config = config
        self.message_widget = message_widget

    @abstractmethod
    def prepare(self):
        raise NotImplementedError

    @abstractmethod
    def bind_to_accept_button(self, accept_button_update_function):
        raise NotImplementedError

    @abstractmethod
    def insert(self):
        raise NotImplementedError

    @abstractmethod
    def is_valid(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def has_changed(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def update_config(self):
        raise NotImplementedError


class NickNameSettingEntry(AbstractSettingEntry):

    def __init__(self, ui: Ui_Dialog, config, message_widget):
        super().__init__(ui, config, message_widget)
        self.nickname_LineEdit = self.ui.authorLineEdit

    def prepare(self):
        self.nickname_LineEdit.setPlaceholderText(_tr("Misc", "Type here to change the nick name"))

    def bind_to_accept_button(self, accept_button_update_function):
        self.nickname_LineEdit.textChanged.connect(accept_button_update_function)

    def insert(self):
        self.nickname_LineEdit.setText(self.config.nickname)

    def is_valid(self) -> bool:
        message = _tr("Misc", "Nick name must not be empty")

        if bool(self.nickname_LineEdit.text()):
            self.message_widget.remove_message(message)
            return True
        else:
            self.message_widget.add_message(message)
            return False

    def has_changed(self) -> bool:
        return not self.config.nickname == self.nickname_LineEdit.text()

    def update_config(self):
        self.config.nickname = self.nickname_LineEdit.text()


class CommentTypeSettingEntry(AbstractSettingEntry):

    def __init__(self, ui: Ui_Dialog, config, message_widget):
        super().__init__(ui, config, message_widget)
        self.kCommentTypes = self.ui.kCommentTypes

        self.ct_tl_eng = {}
        for ct in configuration.Settings.COMMENT_TYPES.value[1]:
            self.ct_tl_eng.update({_tr("Misc", ct): ct})

    def prepare(self):
        cts = self.kCommentTypes
        cts.setStyleSheet(" QPushButton { text-align:left; padding: 8px; } ")

        cts_lv: QListView = cts.listView()
        cts_lv.setEditTriggers(QAbstractItemView.NoEditTriggers)

        cts_lv_le: QLineEdit = cts.lineEdit()
        cts_lv_le.setPlaceholderText(_tr("Misc", "Type here to add new comment types"))

        cts.addButton().setText(_tr("Misc", "Add"))
        cts.removeButton().setText(_tr("Misc", "Remove"))
        cts.upButton().setText(_tr("Misc", "Move Up"))
        cts.downButton().setText(_tr("Misc", "Move Down"))

    def bind_to_accept_button(self, accept_button_update_function):
        self.kCommentTypes.changed.connect(accept_button_update_function)

    def insert(self):
        for ct in self.config.comment_types:
            self.kCommentTypes.insertItem(_tr("Misc", ct))

    def is_valid(self) -> bool:
        ct_items: List[str] = self.kCommentTypes.items()

        items_are_not_empty = bool(ct_items)

        no_item_empty_str = True
        for ct_item in ct_items:
            message = _tr("Misc", "Each comment type needs a valid name")
            if not ct_item:
                no_item_empty_str = False
                self.message_widget.add_message(message)
                break
            else:
                self.message_widget.remove_message(message)

        return items_are_not_empty and no_item_empty_str

    def has_changed(self) -> bool:
        return not self.config.comment_types == [self.ct_tl_eng.get(x, None) for x in self.kCommentTypes.items()]

    def update_config(self):
        self.config.comment_types = [self.ct_tl_eng.get(x, x).strip() for x in self.kCommentTypes.items()]

    def remove_focus(self):
        # Remove selection from comment type items
        ct_list_view: QListView = self.kCommentTypes.listView()

        if ct_list_view.selectionModel().selectedIndexes():
            ct_list_view.clearSelection()
            edit = self.kCommentTypes.lineEdit()
            edit.setReadOnly(False)
            edit.setPlaceholderText(_tr("Misc", "Type here to add new comment types"))


class AutoSaveSettingsEntry(AbstractSettingEntry):

    def __init__(self, ui: Ui_Dialog, config, message_widget):
        super().__init__(ui, config, message_widget)
        self.spinBox = ui.autosaveSpinBox

    def prepare(self):
        pass

    def bind_to_accept_button(self, accept_button_update_function):
        self.spinBox.valueChanged.connect(accept_button_update_function)

    def insert(self):
        self.spinBox.setValue(int(self.config.autosave_interval_seconds))

    def is_valid(self) -> bool:
        return True

    def has_changed(self) -> bool:
        return not self.config.autosave_interval_seconds == self.spinBox.value()

    def update_config(self):
        self.config.autosave_interval_seconds = self.spinBox.value()


class QcDocumentWriteVideoPathToFile(AbstractSettingEntry):

    def __init__(self, ui: Ui_Dialog, config, message_widget):
        super().__init__(ui, config, message_widget)
        self.chkBox = ui.saveVideoPathCheckBox

    def prepare(self):
        pass

    def bind_to_accept_button(self, accept_button_update_function):
        self.chkBox.stateChanged.connect(accept_button_update_function)

    def insert(self):
        self.chkBox.setChecked(self.config.qc_doc_write_video_path_to_file)

    def is_valid(self) -> bool:
        return True

    def has_changed(self) -> bool:
        return not self.config.qc_doc_write_video_path_to_file == self.chkBox.isChecked()

    def update_config(self):
        self.config.qc_doc_write_video_path_to_file = self.chkBox.isChecked()


class QcDocumentWriteNickNameToFile(AbstractSettingEntry):

    def __init__(self, ui: Ui_Dialog, config, message_widget):
        super().__init__(ui, config, message_widget)
        self.chkBox = ui.saveNickNameCheckBox

    def prepare(self):
        pass

    def bind_to_accept_button(self, accept_button_update_function):
        self.chkBox.stateChanged.connect(accept_button_update_function)

    def insert(self):
        self.chkBox.setChecked(self.config.qc_doc_write_nick_name_to_file)

    def is_valid(self) -> bool:
        return True

    def has_changed(self) -> bool:
        return not self.config.qc_doc_write_nick_name_to_file == self.chkBox.isChecked()

    def update_config(self):
        self.config.qc_doc_write_nick_name_to_file = self.chkBox.isChecked()
