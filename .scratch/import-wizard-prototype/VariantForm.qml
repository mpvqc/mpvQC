// PROTOTYPE - Variant B "Form": one dense section card, classic desktop form. Label column left,
// values and inline controls right. Everything visible at once, nothing to click through.
// Replaces the rejected accordion checklist (too smartphone-like).

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
    property int videoComboIndex: 0
    property var subtitleChoices: root.plan.subtitles.candidates.map(() => true)

    readonly property bool closeOnly: root.plan.commentCount === 0
        && root.plan.video.load === "" && root.plan.video.candidates.length === 0
        && root.plan.subtitles.load.length === 0 && root.plan.subtitles.candidates.length === 0

    readonly property int _labelColumnWidth: 100

    function toggleSubtitle(index: int): void {
        const next = root.subtitleChoices.slice();
        next[index] = !next[index];
        root.subtitleChoices = next;
    }

    component FormGroup: RowLayout {
        property alias label: _groupLabel.text
        default property alias content: _groupContent.data

        spacing: 16

        Label {
            id: _groupLabel

            font.weight: Font.DemiBold

            Layout.preferredWidth: root._labelColumnWidth
            Layout.alignment: Qt.AlignTop
            Layout.topMargin: 2
        }

        ColumnLayout {
            id: _groupContent

            spacing: 6

            Layout.fillWidth: true
        }
    }

    title: root.closeOnly ? "Import Error" : "Confirm Import"
    modal: false
    visible: true
    closePolicy: Popup.NoAutoClose
    standardButtons: Dialog.NoButton
    contentWidth: MpvqcConstants.mediumDialogContentWidth
    contentHeight: MpvqcConstants.smallDialogContentHeight

    contentItem: ScrollView {
        id: _scroll

        contentWidth: availableWidth
        contentHeight: _card.implicitHeight + 24

        SectionCard {
            id: _card

            width: _scroll.availableWidth
            y: 12
            contentSpacing: 14

            FormGroup {
                label: "Comments"
                visible: root.plan.commentCount > 0

                Layout.fillWidth: true

                Label {
                    text: root.plan.commentCount + " comments from " + root.plan.acceptedDocuments.join(", ")
                    wrapMode: Text.Wrap

                    Layout.fillWidth: true
                }

                RowLayout {
                    visible: !root.plan.session.resolved
                    spacing: 16

                    RadioButton {
                        checked: !root.replaceComments
                        text: "Add to current"

                        onClicked: root.replaceComments = false
                    }

                    RadioButton {
                        checked: root.replaceComments
                        text: "Start fresh"

                        onClicked: root.replaceComments = true
                    }

                    Item {
                        Layout.fillWidth: true
                    }
                }
            }

            FormGroup {
                label: "Video"
                visible: !root.plan.video.resolved || root.plan.video.load !== ""

                Layout.fillWidth: true

                Label {
                    visible: root.plan.video.resolved
                    text: root.plan.video.load + " will be loaded"

                    Layout.fillWidth: true
                }

                ComboBox {
                    visible: !root.plan.video.resolved
                    model: root.plan.video.candidates.concat(["Skip video"])
                    currentIndex: root.videoComboIndex

                    Layout.fillWidth: true

                    onActivated: index => root.videoComboIndex = index
                }
            }

            FormGroup {
                label: "Subtitles"
                visible: !root.plan.subtitles.resolved || root.plan.subtitles.load.length > 0

                Layout.fillWidth: true

                Repeater {
                    model: root.plan.subtitles.load

                    delegate: Label {
                        required property string modelData

                        text: modelData + " will be loaded"

                        Layout.fillWidth: true
                    }
                }

                Repeater {
                    model: root.plan.subtitles.candidates

                    delegate: CheckBox {
                        id: _subtitleCheck

                        required property int index
                        required property string modelData

                        text: modelData

                        onClicked: root.toggleSubtitle(index)

                        Binding {
                            target: _subtitleCheck
                            property: "checked"
                            value: root.subtitleChoices[_subtitleCheck.index] === true
                        }
                    }
                }
            }

            FormGroup {
                label: "Not imported"
                visible: root.plan.rejectedDocuments.length > 0

                Layout.fillWidth: true

                Repeater {
                    model: root.plan.rejectedDocuments

                    delegate: RowLayout {
                        required property var modelData

                        spacing: 8

                        MpvqcIconLabel {
                            iconColor: MpvqcAppearance.palette.error
                            icon.source: MpvqcIcons.error
                            icon.width: 16
                            icon.height: 16

                            Layout.preferredWidth: 16
                            Layout.preferredHeight: 16
                        }

                        Label {
                            text: modelData.filename
                        }

                        Label {
                            text: modelData.reason
                            color: MpvqcAppearance.palette.hint
                            elide: Text.ElideRight

                            Layout.fillWidth: true
                        }
                    }
                }
            }

            Label {
                visible: root.closeOnly
                text: "Nothing can be imported."
                color: MpvqcAppearance.palette.hint

                Layout.alignment: Qt.AlignHCenter
            }
        }
    }

    footer: PrototypeFooter {
        primaryLabel: root.closeOnly ? "Close" : "Confirm import"
        showCancel: !root.closeOnly
    }
}
