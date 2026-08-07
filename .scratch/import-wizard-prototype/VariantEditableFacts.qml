// PROTOTYPE - Variant F "Editable facts": one digest card where every row states the plan and is
// also the control. Clicking a row opens its options in place: a menu for exclusive choices, a
// checkable popup for subtitles. Known risk: options hide behind a click.

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import io.github.mpvqc.mpvQC.Components
import io.github.mpvqc.mpvQC.Utility

MpvqcDialog {
    id: root

    required property var plan

    property bool replaceComments: false
    property int videoChoice: 0
    property var subtitleChoices: root.plan.subtitles.candidates.map(() => true)

    readonly property bool closeOnly: root.plan.commentCount === 0
        && root.plan.video.load === "" && root.plan.video.candidates.length === 0
        && root.plan.subtitles.load.length === 0 && root.plan.subtitles.candidates.length === 0

    readonly property string _chosenVideo: root.plan.video.resolved ? root.plan.video.load
        : root.videoChoice === -1 ? "" : root.plan.video.candidates[root.videoChoice]
    readonly property int _subtitleCount: root.plan.subtitles.resolved
        ? root.plan.subtitles.load.length
        : root.subtitleChoices.filter(c => c).length

    function toggleSubtitle(index: int): void {
        const next = root.subtitleChoices.slice();
        next[index] = !next[index];
        root.subtitleChoices = next;
    }

    component FactRow: ItemDelegate {
        id: _factRow

        property url factIcon
        property string trailing: ""

        readonly property int iconSize: 20

        verticalPadding: 10
        horizontalPadding: 14

        background: Rectangle {
            radius: height / 2
            color: _factRow.hovered ? Qt.alpha(MpvqcAppearance.palette.foreground, 0.08) : "transparent"

            Behavior on color {
                ColorAnimation {
                    duration: 150
                }
            }
        }

        contentItem: RowLayout {
            spacing: 12

            MpvqcIconLabel {
                iconColor: MpvqcAppearance.palette.foreground
                icon.source: _factRow.factIcon
                icon.width: _factRow.iconSize
                icon.height: _factRow.iconSize

                Layout.preferredWidth: _factRow.iconSize
                Layout.preferredHeight: _factRow.iconSize
            }

            Label {
                text: _factRow.text
                horizontalAlignment: Text.AlignLeft
                elide: Text.ElideMiddle

                Layout.fillWidth: true
            }

            Label {
                visible: _factRow.trailing !== ""
                text: _factRow.trailing
                color: MpvqcAppearance.palette.hint
            }

            MpvqcIconLabel {
                iconColor: MpvqcAppearance.palette.hint
                icon.source: MpvqcIcons.arrowDropDown
                icon.width: _factRow.iconSize
                icon.height: _factRow.iconSize

                Layout.preferredWidth: _factRow.iconSize
                Layout.preferredHeight: _factRow.iconSize
            }
        }
    }

    title: root.closeOnly ? "Import Error" : "Confirm Import"
    modal: false
    visible: true
    closePolicy: Popup.NoAutoClose
    standardButtons: Dialog.NoButton
    contentWidth: MpvqcConstants.mediumDialogContentWidth
    contentHeight: _content.implicitHeight + 24

    contentItem: ColumnLayout {
        id: _content

        SectionCard {
            contentSpacing: 4

            Layout.fillWidth: true
            Layout.topMargin: 12

            FactRow {
                visible: root.plan.commentCount > 0 && !root.plan.session.resolved
                factIcon: MpvqcIcons.comment
                text: root.plan.commentCount + " comments"
                trailing: root.replaceComments ? "replacing current" : "adding to current"

                Layout.fillWidth: true

                onClicked: _sessionMenu.popup()

                Menu {
                    id: _sessionMenu

                    MenuItem {
                        checkable: true
                        checked: !root.replaceComments
                        text: "Add to your current comments"

                        onTriggered: root.replaceComments = false
                    }

                    MenuItem {
                        checkable: true
                        checked: root.replaceComments
                        text: "Start fresh with the new comments"

                        onTriggered: root.replaceComments = true
                    }
                }
            }

            SummaryRow {
                visible: root.plan.commentCount > 0 && root.plan.session.resolved
                icon: MpvqcIcons.comment
                text: root.plan.commentCount + " comments will be imported"

                Layout.fillWidth: true
            }

            FactRow {
                visible: !root.plan.video.resolved
                factIcon: MpvqcIcons.movie
                text: root._chosenVideo === "" ? "No video" : root._chosenVideo
                trailing: root._chosenVideo === "" ? "" : "will be loaded"

                Layout.fillWidth: true

                onClicked: _videoMenu.popup()

                Menu {
                    id: _videoMenu

                    Instantiator {
                        model: root.plan.video.candidates

                        delegate: MenuItem {
                            required property int index
                            required property string modelData

                            checkable: true
                            checked: root.videoChoice === index
                            text: modelData

                            onTriggered: root.videoChoice = index
                        }

                        onObjectAdded: (index, object) => _videoMenu.insertItem(index, object)
                        onObjectRemoved: (index, object) => _videoMenu.removeItem(object)
                    }

                    MenuItem {
                        checkable: true
                        checked: root.videoChoice === -1
                        text: "Skip video"

                        onTriggered: root.videoChoice = -1
                    }
                }
            }

            SummaryRow {
                visible: root.plan.video.resolved && root.plan.video.load !== ""
                icon: MpvqcIcons.movie
                text: root.plan.video.load
                trailing: "will be loaded"

                Layout.fillWidth: true
            }

            FactRow {
                id: _subtitlesRow

                visible: !root.plan.subtitles.resolved
                factIcon: MpvqcIcons.subtitles
                text: root._subtitleCount + " of " + root.plan.subtitles.candidates.length + " subtitles"
                trailing: root._subtitleCount > 0 ? "will be loaded" : ""

                Layout.fillWidth: true

                onClicked: _subtitlesPopup.open()

                Popup {
                    id: _subtitlesPopup

                    y: _subtitlesRow.height
                    width: 320
                    padding: 8

                    contentItem: ColumnLayout {
                        spacing: 0

                        Repeater {
                            model: root.plan.subtitles.candidates

                            delegate: CheckRow {
                                required property int index
                                required property string modelData

                                isChecked: root.subtitleChoices[index] === true
                                text: modelData

                                Layout.fillWidth: true

                                onToggleRequested: root.toggleSubtitle(index)
                            }
                        }
                    }
                }
            }

            Repeater {
                model: root.plan.subtitles.load

                delegate: SummaryRow {
                    required property string modelData

                    icon: MpvqcIcons.subtitles
                    text: modelData
                    trailing: "will be loaded"

                    Layout.fillWidth: true
                }
            }

            Repeater {
                model: root.plan.rejectedDocuments

                delegate: SummaryRow {
                    required property var modelData

                    icon: MpvqcIcons.error
                    iconColor: MpvqcAppearance.palette.error
                    text: modelData.filename
                    subText: modelData.reason
                    trailing: "skipped"

                    Layout.fillWidth: true
                }
            }

            Label {
                visible: root.closeOnly
                text: "Nothing can be imported."
                color: MpvqcAppearance.palette.hint

                Layout.fillWidth: true
            }
        }
    }

    footer: PrototypeFooter {
        primaryLabel: root.closeOnly ? "Close" : "Confirm import"
        showCancel: !root.closeOnly
    }
}
