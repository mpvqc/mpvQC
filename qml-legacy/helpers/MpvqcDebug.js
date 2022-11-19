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


class Element {

    constructor(item) {
        this.properties = {}
        this.functions = {}
        this._investigate(item)
    }

    _investigate(item) {
        // Based on: https://raymii.org/s/snippets/Log_all_Item_properties_and_functions_in_Qml.html
        for (const element in item) {
            if (typeof item[element] == "function") {
                this.functions[element] = item[element]
            } else {
                this.properties[element] = item[element]
            }
        }
    }
}


const replacer = null
const spaces = 2


function investigate(item) {
    return JSON.stringify(new Element(item), replacer, spaces)
}
