/*
mpvQC

Copyright (C) 2022 mpvQC developers

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


// Based on: https://raymii.org/s/snippets/Log_all_Item_properties_and_functions_in_Qml.html


/**
 * Extracts all properties from item
 */
function obtainPropertiesOf(item) {
    const properties = []
    for (const p in item)
        if (typeof item[p] != "function")
            properties.push(`${p}: ${item[p]}`)
    return properties
}


/**
 * Extracts all functions from item
 */
function obtainFunctionsOf(item) {
    const functions = [];
    for (const f in item)
        if (typeof item[f] == "function")
            functions.push(`${f}: ${item[f]}`)
    return functions
}


/**
 * Logs all properties and functions from an item to the console
 */
function log(item) {
    console.log("Properties:")
    for (const prop of obtainPropertiesOf(item)) {
        console.log(" * ", prop)
    }
    console.log("Functions:")
    for (const func of obtainFunctionsOf(item)) {
        console.log(" - ", func)
    }
}
