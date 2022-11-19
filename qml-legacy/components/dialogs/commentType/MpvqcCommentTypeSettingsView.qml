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
import QtQuick.Controls
import helpers
import settings
import "MpvqcCommentTypeUtils.js" as Utils


Column {

    ToolButton {
        text: qsTranslate("CommentTypeSettings", "Add")
        icon.source: "qrc:/data/icons/add_black_24dp.svg"
        width: parent.width

        onClicked: {
            createAddCommentTypeDialog()
        }

        function createAddCommentTypeDialog() {
            const url = 'qrc:/qml/components/shared/MpvqcInputDialog.qml'
            const component = Qt.createComponent(url)
            const dialog = component.createObject(appWindow)
            dialog.validate = (commentType) => validateCommentType(commentType, listView.model.items())
            dialog.headerLabel = qsTranslate("CommentTypeSettings", "New Comment Type:")
            dialog.inputReceived.connect((commentType) => { dialog.close(); add(commentType) })
            dialog.open()
        }

        function add(commentType) {
            const commentTypeTranslation = MpvqcCommentTypeReverseTranslator.lookup(commentType)
            listView.model.add(commentTypeTranslation)
        }
    }


    Rectangle { color: "transparent"; height: 24; width: 10 }

    Rectangle {
        width: parent.width
        height: listView.height
        color: "transparent"

        ListView {
            id: listView
            height: 310
            model: MpvqcSettings.commentTypes.copy(appWindow)
            spacing: 0
            clip: true
            reuseItems: true
            boundsBehavior: Flickable.StopAtBounds
            anchors.left: parent.left
            anchors.right: parent.right

            ScrollBar.vertical: ScrollBar {
                id: scrollBar
                policy: isShown ? ScrollBar.AlwaysOn : ScrollBar.AlwaysOff
                stepSize: 0.033
                readonly property var isShown: listView.contentHeight > listView.height
                readonly property var visibleWidth: isShown ? width : 0
            }

            delegate: MpvqcCommentTypeDelegate {
                backgroundColor: listView.currentIndex === index ? Material.accent : "transparent"
                commentType: qsTranslate("CommentTypes", model.type)
                listViewParent: listView.parent
                listViewHeight: listView.height
                spacerWidth: scrollBar.visibleWidth

                anchors {
                    left: parent.left
                    right: parent.right
                }

                ListView.onAdd: {
                    MpvqcTimer.scheduleOnceAfter(0, function() {
                        listView.currentIndex = index
                        listView.positionViewAtIndex(index, ListView.Center)
                    })
                }

                onDeletePressed: {
                    listView.model.remove(index, 1)
                }

                onEditPressed: {
                    createEditCommentTypeDialog()
                }

                function createEditCommentTypeDialog() {
                    const commentTypeTranslation = MpvqcCommentTypeReverseTranslator.lookup(commentType)
                    const commentTypes = Utils.remove(listView.model.items(), commentTypeTranslation, commentType)

                    const url = 'qrc:/qml/components/shared/MpvqcInputDialog.qml'
                    const component = Qt.createComponent(url)
                    const dialog = component.createObject(appWindow)
                    dialog.validate = (commentType) => validateCommentType(commentType, commentTypes)
                    dialog.headerLabel = qsTranslate("CommentTypeSettings", "Edit Comment Type:")
                    dialog.text = commentType
                    dialog.inputReceived.connect((commentType) => { dialog.close(); edit(commentType) })
                    dialog.open()
                }

                function edit(commentType) {
                    const commentTypeTranslation = MpvqcCommentTypeReverseTranslator.lookup(commentType)
                    listView.model.edit(index, commentTypeTranslation)
                }

                onMoved: (sourceIndex, targetIndex) => {
                    listView.model.move(sourceIndex, targetIndex, 1)
                    listView.positionViewAtIndex(targetIndex, ListView.Center)
                }

                onSelected: {
                    listView.currentIndex = index
                }
            }
        }

    }

    function save() {
        MpvqcSettings.commentTypes.replaceWith(listView.model.asString())
        MpvqcCommentTypeWidthCalculator.calculateMaxWidth()
    }

    function reset() {
        const qmlParent = appWindow
        listView.model.reset(qmlParent)
    }

    function validateCommentType(text, existingCommentTypes) {
        if (Utils.commentTypeIncludedOrExists(text, existingCommentTypes)) {
            return qsTranslate("CommentTypeSettings", "Comment type already exists")
        } else if (Utils.includesForbiddenCharacters(text)) {
            return qsTranslate("CommentTypeSettings", "Square brackets are not allowed")
        }
    }

}
