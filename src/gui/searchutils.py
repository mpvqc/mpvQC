# Copyright (C) 2016-2018 Frechdachs <frechdachs@rekt.cc>
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

from PyQt5.QtCore import pyqtSignal, QModelIndex, QCoreApplication, QEvent, QObject

_translate = QCoreApplication.translate


class SearchResult(QObject):
    # Signal which is emitted after highlight_result() is called.
    highlight = pyqtSignal(QModelIndex)
    highlight_change_request = pyqtSignal(str)

    def __init__(self, query: str, match: QModelIndex or None, actual_result: int, total_results: int):
        super().__init__()
        self.__valid_query = bool(query)
        self.__match = match
        self.__actual_result = actual_result
        self.__total_results = total_results

    def highlight_result(self) -> None:
        if self.__match and self.__match.isValid():
            self.highlight.emit(self.__match)

        self.highlight_changed()

    def highlight_changed(self):
        if self.__valid_query:
            if self.__match:
                if self.__total_results == 1:
                    new_text = _translate("SearchForm", "{0} comment").format(1)
                else:
                    new_text = _translate("SearchForm", "{0} of {1} comments") \
                        .format(self.__actual_result, self.__total_results)
            else:
                new_text = _translate("SearchForm", "Phrase not found")
        else:
            new_text = ""

        self.highlight_change_request.emit(new_text)
