import inspect
import io
import json
import os
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any, List

from appdirs import unicode

from src.gui.preferences import Ui_Dialog
from src.preferences import configuration

try:
    to_unicode = unicode
except NameError:
    to_unicode = str


class _JsonLoader:
    JSON_SETTINGS: Dict = None
    instance: '_JsonLoader' = None

    def __init__(self):
        if _JsonLoader.JSON_SETTINGS is None:
            settings_json = configuration.get_paths().settings_json
            if not os.path.isfile(settings_json):
                with io.open(settings_json, 'w', encoding='utf8') as outfile:
                    str_ = json.dumps({}, indent=4, separators=(',', ': '), ensure_ascii=False)
                    outfile.write(to_unicode(str_))
            with open(settings_json) as df:
                _JsonLoader.JSON_SETTINGS = json.load(df)

    @staticmethod
    def get_value(key: str):
        if _JsonLoader.instance is None:
            _JsonLoader.instance = _JsonLoader()

        dictionary: Dict = _JsonLoader.JSON_SETTINGS

        return dictionary.get(key)


class SettingsType(Enum):
    """
    An enum for representing the settings type in the JSON file.

    Used in *AbstractNonUserEditableSetting* when parsing/casting the JSON string to the correct type.
    """

    LIST_STRING = 0
    STRING = 1
    FLOAT = 2
    BOOL = 3
    INT = 4

    CUSTOM = 5


class SettingsEntry:

    def __init__(self, name, default_value, var_type: SettingsType):
        """
        Holder for a settings entry's data.

        :param name: The name of this attribute. The name is only used to store this entry in the JSON file.
        :param default_value: The default value to assign if no attribute with **name** was found.
        :param var_type: The type of this variable.
            Used to assign the correct type to the variable when parsing the JSON string.
        """

        self.name = name
        self.default_value = default_value
        self.var_type = var_type


class AbstractNonUserEditableSetting(ABC):
    """
    A class for all settings which are stored in the settings.json
    **and** which **are not** editable by the user via the preference dialog.
    """

    def __init__(self):
        self.settings_entry = self.provide_settings_declaration()
        value_in_json = _JsonLoader.get_value(self.settings_entry.name)

        self._value = self.__parse_string_to_var_type(
            string=self.settings_entry.default_value if value_in_json is None else value_in_json,
            var_type=self.settings_entry.var_type)

    def __parse_string_to_var_type(self, string: str, var_type: SettingsType) -> Any:
        """Will parse/cast the string to a var_type object."""

        if var_type == SettingsType.LIST_STRING:
            return string
        elif var_type == SettingsType.STRING:
            return string
        elif var_type == SettingsType.FLOAT:
            return float(string)
        elif var_type == SettingsType.BOOL:
            return bool(string)
        elif var_type == SettingsType.INT:
            return int(string)
        else:
            return self.transform_to_custom_value(string)

    # noinspection PyUnusedLocal
    def transform_to_custom_value(self, string: str) -> Any:
        """Override this method in case some custom setting needs to be parsed from the JSON string."""

        pass
        raise NotImplementedError(
            "For the setting '{}' a custom implementation for parsing from string '{}' to value is necessary!".format(
                inspect.stack()[0][3], string))

    @property
    def name(self):
        return self.settings_entry.name

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @abstractmethod
    def provide_settings_declaration(self) -> SettingsEntry:
        """Returns a SettingsEntry object with data about the setting to store."""

        raise NotImplementedError("The setting '{}' is not implemented!".format(inspect.stack()[0][3]))


class AbstractUserEditableSetting(AbstractNonUserEditableSetting):
    """
        A class for all settings which are stored in the settings.json
        **and** which **are** editable by the user via the preference dialog.
    """

    def __init__(self):
        super().__init__()
        self.ui: Ui_Dialog = None

    def error_messages(self) -> List[str]:
        """Error messages in case the user needs to be hinted."""

        return []

    def transform_to_custom_value(self, string: str) -> Any:
        return super().transform_to_custom_value(string)

    def bind_preference(self, ui: Ui_Dialog) -> None:
        """
        This method binds the Ui_Dialog to this preference object.
        In all abstract methods the self.ui is never None.

        :param ui: The Ui_Dialog on which the UI components for this setting are located.

        """

        self.ui = ui

    @abstractmethod
    def setup(self, update_function) -> None:
        """Inserts the current value in the the UI component."""

        raise NotImplementedError("This method '{}' is not implemented!".format(inspect.stack()[0][3]))

    @abstractmethod
    def is_valid(self) -> bool:
        """
        Checks whether it is acceptable to store this setting.

        :return: **True** if this setting is valid to store.
        :return: **False** else.
        """

        raise NotImplementedError("This method '{}' is not implemented!".format(inspect.stack()[0][3]))

    @abstractmethod
    def has_changed(self) -> bool:
        """
        Checks whether this setting has changed.

        :return: **True** if this setting has changed.
        :return: **False** else.
        """

        raise NotImplementedError("This method '{}' is not implemented!".format(inspect.stack()[0][3]))

    @abstractmethod
    def take_over(self):
        """Will assign the Ui components input as this setting's value."""

        raise NotImplementedError("This method '{}' is not implemented!".format(inspect.stack()[0][3]))
