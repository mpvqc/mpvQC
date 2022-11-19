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



import QtQuick 2.0
import QtTest


TestCase {
    name: "MpvqcCommentTypeReverseTranslator"
    optional: true
    property var testObject: MpvqcCommentTypeReverseTranslator

    function test_en_US() {
        Qt.uiLanguage = 'en_US'
        compare(MpvqcCommentTypeReverseTranslator.lookup('Punctuation'), 'Punctuation')
    }

    // Deactivated because we don't compile translations for tests at the moment
    // function test_de_DE() {
    //     Qt.uiLanguage = 'de_DE'
    //     compare(MpvqcCommentTypeReverseTranslator.lookup('Interpunktion'), 'Punctuation')
    // }

}
