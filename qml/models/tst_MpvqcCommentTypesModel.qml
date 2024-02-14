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

import QtQuick
import QtTest


TestCase {
    name: 'MpvqcCommentTypesModel'

    Item { id: _item }

    property string commentType: 'anyOtherValue'
    property MpvqcCommentTypesModel model: undefined

    function init() {
        if (model) model.destroy()
        model = Qt.createQmlObject('import models; MpvqcCommentTypesModel {}', _item)
    }

    function test_items_data() {
        return [ { tag: 'Spelling' }, { tag: 'Punctuation' } ]
    }

    function test_items(data): void {
        const types = model.items()
        verify(types.includes(data.tag))
    }

    function test_add(): void {
        model.clear()
        model.add(commentType)

        compare(model.count, 1)
        compare(model.get(0).type, commentType)
    }

    function test_replace(): void {
        model.replace(0, commentType)
        compare(model.get(0).type, commentType)
    }

    function test_obtain(): void {
        const item = model.obtain(0)
        compare(item, 'Translation')
    }

    function test_copy(): void {
        model.remove(1, model.count - 2)
        compare(model.count, 2)

        const copy = model.copy(_item)

        compare(model.get(0).type, copy.get(0).type)
        compare(model.get(1).type, copy.get(1).type)
    }

    function test_replaceWith() {
        const one = 'my', two = 'custom', three = 'elements'
        const items = [one, two, three]

        model.replaceWith(items)

        compare(model.count, items.length)
        compare(model.get(0).type, one)
        compare(model.get(1).type, two)
        compare(model.get(2).type, three)
    }

    function test_reset() {
        model.clear()
        compare(model.count, 0)

        model.reset(_item)

        compare(model.obtain(0), 'Translation')
        compare(model.obtain(model.count - 1), 'Note')
    }

}
