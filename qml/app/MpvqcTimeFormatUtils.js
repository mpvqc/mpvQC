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


/**
 * https://stackoverflow.com/a/6313008/8596346
 * @param secs {number}
 * @return {string}
 */
function formatTimeToString(secs) {
    const sec_num = Math.max(0, parseInt(secs, 10))
    let hours = Math.floor(sec_num / 3600)
    let minutes = Math.floor((sec_num - (hours * 3600)) / 60)
    let seconds = sec_num - (hours * 3600) - (minutes * 60)
    if (hours < 10) hours = `0${ hours }`
    if (minutes < 10) minutes = `0${ minutes }`
    if (seconds < 10) seconds = `0${ seconds }`
    return `${ hours }:${ minutes }:${ seconds }`
}


/**
 *
 * @param secs
 * @return {string}
 */
function formatTimeToStringShort(secs) {
    if (secs >= 3600) throw `Seconds '${ secs }' is greater than or equals 3600`
    const sec_num = Math.max(0, parseInt(secs, 10))
    let minutes = Math.floor(sec_num / 60)
    let seconds = sec_num - (minutes * 60)
    if (minutes < 10) minutes = `0${ minutes }`
    if (seconds < 10) seconds = `0${ seconds }`
    return `${ minutes }:${ seconds }`
}


/**
 * https://thewebdev.info/2021/05/23/how-to-convert-hhmmss-time-string-to-seconds-only-in-javascript/
 * @param timeString {string}
 * @returns {number}
 */
function extractSecondsFrom(timeString) {
    const [hours, minutes, seconds] = timeString.split(':')
    return (+hours) * 60 * 60 + (+minutes) * 60 + (+seconds)
}
