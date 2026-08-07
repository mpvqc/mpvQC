// PROTOTYPE - Variant E "Side rail": a wide dialog that spends width instead of height. Open
// questions sit as section cards on the left; a slim always-visible plan rail on the right shows
// what will happen, updating live as answers change.

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

    readonly property bool anyQuestion: !root.plan.session.resolved
        || !root.plan.video.resolved || !root.plan.subtitles.resolved

    readonly property string _chosenVideo: root.plan.video.resolved ? root.plan.video.load
        : root.videoChoice === -1 ? "" : root.plan.video.candidates[root.videoChoice]
    readonly property int _subtitleCount: root.plan.subtitles.resolved
        ? root.plan.subtitles.load.length
        : root.subtitleChoices.filter(c => c).length

    readonly property int _sectionSpacing: 12

    function toggleSubtitle(index: int): void {
        const next = root.subtitleChoices.slice();
        next[index] = !next[index];
        root.subtitleChoices = next;
    }

    title: root.closeOnly ? "Import Error" : "Confirm Import"
    modal: false
    visible: true
    closePolicy: Popup.NoAutoClose
    standardButtons: Dialog.NoButton
    contentWidth: 700
    contentHeight: MpvqcConstants.smallDialogContentHeight

    contentItem: RowLayout {
        spacing: 16

        ScrollView {
            id: _scroll

            contentWidth: availableWidth
            contentHeight: _questions.implicitHeight

            Layout.fillWidth: true
            Layout.fillHeight: true

            ColumnLayout {
                id: _questions

                width: _scroll.availableWidth
                spacing: root._sectionSpacing

                Label {
                    visible: !root.anyQuestion
                    text: root.closeOnly ? "Nothing can be imported." : "Nothing to decide."
                    color: MpvqcAppearance.palette.hint

                    Layout.topMargin: root._sectionSpacing
                    Layout.alignment: Qt.AlignHCenter
                }

                SectionCard {
                    title: "Comments"
                    visible: !root.plan.session.resolved

                    Layout.fillWidth: true
                    Layout.topMargin: root._sectionSpacing

                    Label {
                        text: "You already have comments in this session."
                        color: MpvqcAppearance.palette.hint

                        Layout.fillWidth: true
                    }

                    OptionRow {
                        selected: !root.replaceComments
                        text: "Add to your current comments"

                        Layout.fillWidth: true

                        onClicked: root.replaceComments = false
                    }

                    OptionRow {
                        selected: root.replaceComments
                        text: "Start fresh with the new comments"

                        Layout.fillWidth: true

                        onClicked: root.replaceComments = true
                    }
                }

                SectionCard {
                    title: "Video"
                    visible: !root.plan.video.resolved

                    Layout.fillWidth: true
                    Layout.topMargin: root.plan.session.resolved ? root._sectionSpacing : 0

                    Label {
                        text: "Which video should be loaded?"
                        color: MpvqcAppearance.palette.hint

                        Layout.fillWidth: true
                    }

                    Repeater {
                        model: root.plan.video.candidates

                        delegate: OptionRow {
                            required property int index
                            required property string modelData

                            selected: root.videoChoice === index
                            text: modelData

                            Layout.fillWidth: true

                            onClicked: root.videoChoice = index
                        }
                    }

                    OptionRow {
                        selected: root.videoChoice === -1
                        text: "Skip video"

                        Layout.fillWidth: true

                        onClicked: root.videoChoice = -1
                    }
                }

                SectionCard {
                    title: "Subtitles"
                    visible: !root.plan.subtitles.resolved

                    Layout.fillWidth: true
                    Layout.bottomMargin: root._sectionSpacing

                    Label {
                        text: "Which subtitles should be loaded?"
                        color: MpvqcAppearance.palette.hint

                        Layout.fillWidth: true
                    }

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

        SectionCard {
            title: "Plan"
            contentSpacing: 10

            Layout.preferredWidth: 230
            Layout.alignment: Qt.AlignTop
            Layout.topMargin: root._sectionSpacing

            SummaryRow {
                visible: root.plan.commentCount > 0
                icon: MpvqcIcons.comment
                text: root.plan.commentCount + " comments"
                subText: root.plan.session.resolved ? ""
                    : root.replaceComments ? "replacing current" : "added to current"

                Layout.fillWidth: true
            }

            SummaryRow {
                visible: root._chosenVideo !== ""
                icon: MpvqcIcons.movie
                text: root._chosenVideo

                Layout.fillWidth: true
            }

            SummaryRow {
                visible: root._subtitleCount > 0
                icon: MpvqcIcons.subtitles
                text: root._subtitleCount + " subtitle files"

                Layout.fillWidth: true
            }

            Repeater {
                model: root.plan.rejectedDocuments

                delegate: SummaryRow {
                    required property var modelData

                    icon: MpvqcIcons.error
                    iconColor: MpvqcAppearance.palette.error
                    text: modelData.filename
                    subText: modelData.reason

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
