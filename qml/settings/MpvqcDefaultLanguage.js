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


/**
 * Uses the system language and checks if a translation exists in our model
 * @returns {string} the abbrev attribute as found in the models.MpvqcLanguageModel or "en" as fallback
 */
function getDefault(parent) {
    const defaultLanguages = Qt.locale().uiLanguages
    const model = Qt.createQmlObject('import models; MpvqcLanguageModel {}', parent)
    for (let i = 0, count = model.count; i < count; i++) {
        const abbrev = model.get(i).abbrev
        if (defaultLanguages.includes(abbrev)) {
            model.destroy()
            return abbrev
        }
    }
    model.destroy()
    return "en_US"
}
