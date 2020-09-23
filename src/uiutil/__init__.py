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


import src.uiutil._dialogs as dialogs
from ._delegates import CommentTimeDelegate, CommentTypeDelegate, CommentNoteDelegate, TIME_FORMAT
from ._dialogs import _SUPPORTED_SUB_FILES as SUPPORTED_SUB_FILES
from ._searchutils import SearchResult
from ._utils import SpecialCharacterValidator, KEY_MAPPINGS, command_generator, replace_special_characters
