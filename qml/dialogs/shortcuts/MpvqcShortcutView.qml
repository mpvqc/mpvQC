/*
mpvQC

Copyright (C) 2024 mpvQC developers

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

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

import shared

ColumnLayout {
    id: root

    spacing: 0

    TextField {
        id: _textField

        Layout.fillWidth: true
        Layout.topMargin: 10
        Layout.bottomMargin: 20

        focus: true
        selectByMouse: true
        placeholderText: "Search"
        horizontalAlignment: Text.AlignLeft

        onTextChanged: {
            _listView.filterQuery = _textField.text.trim().toLowerCase();
        }
    }

    ListView {
        id: _listView

        readonly property int spaceBetweenItemAndScrollbar: 4
        readonly property int scrollBarSpace: _scrollBar.width + spaceBetweenItemAndScrollbar
        readonly property int scrollBarSpaceLeft2Right: LayoutMirroring.enabled ? 0 : scrollBarSpace
        readonly property int scrollBarSpaceRight2Left: LayoutMirroring.enabled ? scrollBarSpace : 0

        property string filterQuery: ""
        property int itemWidth: -1

        Layout.fillWidth: true
        Layout.fillHeight: true

        spacing: 10
        clip: true
        boundsBehavior: Flickable.StopAtBounds

        model: _filterModel

        ScrollBar.vertical: ScrollBar {
            id: _scrollBar

            readonly property bool isShown: _listView.contentHeight > _listView.height
            readonly property int visibleWidth: isShown ? width : 0

            policy: isShown ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff
        }

        onCountChanged: {
            if (itemWidth < 0 && count > 0) {
                itemWidth = itemAtIndex(0).width;
            }
        }

        onFilterQueryChanged: {
            _filterModel.update();
        }

        section {
            property: "category"

            delegate: MpvqcHeader {
                required property string section

                text: section
                width: _listView.itemWidth
            }
        }

        MpvqcShortcutFilterModel {
            id: _filterModel

            filterAcceptsItem: item => {
                const query = _listView.filterQuery;
                if (!query) {
                    return true;
                }

                if (item.label.toLowerCase().includes(query)) {
                    return true;
                }

                if (item.category.toLowerCase().includes(query)) {
                    return true;
                }

                const buttons = [item.button1, item.button2, item.button3].filter(Boolean).map(text => text.toLowerCase());

                if (item.isSeparateShortcut) {
                    return buttons.some(text => text.includes(query));
                }

                return buttons.join("+").includes(query);
            }

            model: MpvqcShortcutModel {}

            delegate: MpvqcShortcut {
                required property var model

                shortcutLabel: model.label
                shortcutButton1: model.button1
                shortcutButton1Icon: model.button1Icon
                shortcutButton2: model.button2
                shortcutButton2Icon: model.button2Icon
                shortcutButton3: model.button3
                shortcutButton3Icon: model.button3Icon
                isMultiShortcut: model.isSeparateShortcut
                scrollBarPadding: _listView.scrollBarSpace

                width: parent ? parent.width - _listView.scrollBarSpaceLeft2Right : 0
                rightMargin: _listView.scrollBarSpaceRight2Left
            }
        }
    }
}
