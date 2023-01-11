// noinspection JSUnusedGlobalSymbols

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


const asynchronous = false


/**
 * @param url {QUrl}
 * @return {string}
 */
function read(url) {
    let content = ''
    const request = new XMLHttpRequest()
    request.open("GET", url, asynchronous)
    request.onreadystatechange = () => {
        if (request.readyState === XMLHttpRequest.DONE) {
            content = request.responseText
        }
    }
    request.onerror = () => console.log(`Error reading from url: ${ url }`)
    request.send()
    return content
}