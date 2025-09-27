// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

import pyobjects

import "../../shared"
import "../../models"

MpvqcDialog {
    id: root

    title: qsTranslate("ShortcutsDialog", "Keyboard Shortcuts")

    contentWidth: 500
    contentHeight: MpvqcShortcutDialogController.dialogHeight

    contentItem: ColumnLayout {
        spacing: 0

        TextField {
            Layout.fillWidth: true
            Layout.topMargin: 10
            Layout.bottomMargin: 20

            focus: true
            selectByMouse: true
            placeholderText: "Search"
            horizontalAlignment: Text.AlignLeft

            onTextChanged: {
                _listView.filterQuery = text.trim().toLowerCase();
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
                    font.pointSize: 14
                    horizontalAlignment: Text.AlignHCenter
                }
            }

            DelegateModel {
                id: _filterModel

                groups: DelegateModelGroup {
                    id: _visibleItems

                    name: "visible"
                    includeByDefault: false
                }

                filterOnGroup: "visible"

                function update(): void {
                    if (items.count > 0) {
                        items.setGroups(0, items.count, "items");
                    }

                    const visible = [];
                    for (let i = 0; i < items.count; ++i) {
                        const item = items.get(i);
                        if (filterAcceptsItem(item.model)) {
                            visible.push(item);
                        }
                    }

                    for (let i = 0; i < visible.length; ++i) {
                        const item = visible[i];
                        item.inVisible = true;
                        if (item.visibleIndex !== i) {
                            _visibleItems.move(item.visibleIndex, i, 1);
                        }
                    }
                }

                function filterAcceptsItem(item): bool {
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

                model: MpvqcShortcutsModel {}

                delegate: ShortcutRow {
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

                Component.onCompleted: {
                    update();
                }
            }
        }
    }

    component ShortcutRow: RowLayout {
        id: _shortcutRow

        property alias shortcutLabel: _descriptionLabel.text

        property alias shortcutButton1: _button1.text
        property alias shortcutButton1Icon: _button1.icon.source

        property alias shortcutButton2: _button2.text
        property alias shortcutButton2Icon: _button2.icon.source

        property alias shortcutButton3: _button3.text
        property alias shortcutButton3Icon: _button3.icon.source

        property bool isMultiShortcut: false
        property int rightMargin: 0
        property int scrollBarPadding: 0

        Label {
            id: _descriptionLabel

            wrapMode: Text.WordWrap
            horizontalAlignment: Text.AlignLeft

            Layout.maximumWidth: _shortcutRow.width - _buttonsLayout.width - _shortcutRow.scrollBarPadding
        }

        Rectangle {
            color: "transparent"
            Layout.fillWidth: true
        }

        RowLayout {
            id: _buttonsLayout

            spacing: 4

            ShortcutButton {
                id: _button1
            }

            Label {
                text: _shortcutRow.isMultiShortcut ? "/" : "+"
                visible: _button2.hasContent
                verticalAlignment: Text.AlignVCenter

                Layout.preferredHeight: _button2.hasContent ? parent.height : 0
                Layout.preferredWidth: _button2.hasContent ? implicitWidth : 0
            }

            ShortcutButton {
                id: _button2
            }

            Label {
                text: "+"

                visible: _button3.hasContent
                verticalAlignment: Text.AlignVCenter

                Layout.preferredHeight: _button3.hasContent ? parent.height : 0
                Layout.preferredWidth: _button3.hasContent ? implicitWidth : 0
            }

            ShortcutButton {
                id: _button3
            }
        }

        Rectangle {
            color: "transparent"
            Layout.preferredWidth: _shortcutRow.rightMargin
        }
    }

    component ShortcutButton: Button {
        readonly property bool hasContent: text || icon.source.toString()

        enabled: false
        visible: hasContent
        height: hasContent ? implicitHeight : 0
        width: hasContent ? implicitWidth : 0
    }
}
