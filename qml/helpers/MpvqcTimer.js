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


function Timer() {
    return Qt.createQmlObject("import QtQuick; Timer {}", appWindow);
}


/**
 * Runs an action in the next loop execution
 * @param action {function}
 */
function scheduleOnce(action) {
    return scheduleOnceAfter(0, action)
}


/**
 * Runs an action after the specified delay
 * @param delay {number}
 * @param action {function}
 */
function scheduleOnceAfter(delay, action) {
    const timer = new Timer();
    timer.interval = delay;
    timer.repeat = false;
    timer.triggered.connect(action);
    timer.triggered.connect(timer.destroy);
    timer.start();
}
