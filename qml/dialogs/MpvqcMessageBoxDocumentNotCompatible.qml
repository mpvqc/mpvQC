/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

import shared


MpvqcMessageBox {
    id: root

    readonly property var mpvqcFileSystemHelperPyObject: mpvqcApplication.mpvqcFileSystemHelperPyObject

    function renderErroneous(documents: list<url>): string {
        root.customTitle = documents.length === 1
            ? qsTranslate("MessageBoxes", "Document Not Compatible")
            : qsTranslate("MessageBoxes", "Documents Not Compatible")
        root.customText = documents
            .map(documentUrl => mpvqcFileSystemHelperPyObject.url_to_absolute_path(documentUrl))
            .join('\n\n')
    }

}
