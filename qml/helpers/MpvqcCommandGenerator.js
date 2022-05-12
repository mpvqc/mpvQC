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

const ALPHANUMERICS = '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÀÁÂÃÇÉÈÊËÍÌÎÏÑÓÒÔÕÚÙÛÝŸ'

const SPECIAL_KEYS = new Map([
    [Qt.Key_PageUp, 'PGUP'],
    [Qt.Key_PageDown, 'PGDWN'],
    [Qt.Key_Play, 'PLAY'],
    [Qt.Key_Pause, 'PAUSE'],
    [Qt.Key_Stop, 'STOP'],
    [Qt.Key_Forward, 'FORWARD'],
    [Qt.Key_Back, 'REWIND'],
    [Qt.Key_MediaPlay, 'PLAY'],
    [Qt.Key_MediaStop, 'STOP'],
    [Qt.Key_MediaNext, 'NEXT'],
    [Qt.Key_MediaPrevious, 'PREV'],
    [Qt.Key_MediaPause, 'PAUSE'],
    [Qt.Key_MediaTogglePlayPause, 'PLAYPAUSE'],
    [Qt.Key_Home, 'HOME'],
    [Qt.Key_End, 'END'],
    [Qt.Key_Escape, 'ESC'],
    [Qt.Key_Left, 'LEFT'],
    [Qt.Key_Right, 'RIGHT'],
    [Qt.Key_Up, 'UP'],
    [Qt.Key_Down, 'DOWN'],
    [Qt.Key_Backspace, 'BACKSPACE'],
    [Qt.Key_Return, 'ENTER'],
    [Qt.Key_Enter, 'ENTER'],
    [Qt.Key_Space, 'SPACE'],
])


class KeyPress {

    constructor(event) {
        this.key = event.key
        this.text = event.text
        this.modifiers = this._extractModifiers(event)
    }

    /**
     * @param event {QQuickKeyEvent}
     * @return {[string, string, string]}
     */
    _extractModifiers(event) {
        const modifiers = event.modifiers
        const shift = modifiers & Qt.ShiftModifier ? "shift" : ""
        const ctrl = modifiers & Qt.ControlModifier ? "ctrl" : ""
        const alt = modifiers & Qt.AltModifier ? "alt" : ""
        return [shift, ctrl, alt]
    }

    isSpecialKey() {
        return SPECIAL_KEYS.has(this.key)
    }

    generateSpecialCommand() {
        const text = SPECIAL_KEYS.get(this.key)
        return this._composeCommand(this.modifiers, text)
    }

    /**
     * @param modifier {Array<string>}
     * @param text {string | null}
     * @return {string}
     */
    _composeCommand(modifier, text) {
        return [...modifier, text]
            .filter(value => value != null && value !== '')
            .join('+')
    }

    generateNormalCommand() {
        if (this._isInvalidKey())
            return null
        if (this._isOnlyModifiers())
            return null
        return this._generate();
    }

    _isInvalidKey() {
        return this.key === 0
    }

    _isOnlyModifiers() {
        return this.text === ''
    }

    _generate() {
        let [shift, ctrl, alt] = this.modifiers
        let text = String.fromCharCode(this.key)
        if (this._isNotAlphanumeric(text)) {
            ctrl = null
            alt = null
        }
        if (!shift && this._isAlphanumeric(text))
            text = text.toLowerCase()
        return this._composeCommand([ctrl, alt], text)
    }

    _isNotAlphanumeric(text) {
        return !this._isAlphanumeric(text)
    }

    _isAlphanumeric(text) {
        return ALPHANUMERICS.includes(text)
    }
}


// noinspection JSUnusedGlobalSymbols
function generateFrom(event) {
    const keyPress = new KeyPress(event)
    if (keyPress.isSpecialKey())
        return keyPress.generateSpecialCommand()
    return keyPress.generateNormalCommand()
}
