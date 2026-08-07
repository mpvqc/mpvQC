// PROTOTYPE - Variant B "Digest + questions": one compact card up top states everything that
// will happen (resolved concerns, skipped files); each open question keeps a full section card
// below, appearance-dialog style. Facts read, questions act. Replaces the rejected dense form.

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

    readonly property int selectedSubtitleCount: root.subtitleChoices.filter(c => c).length
    readonly property int _sectionSpacing: 12

    function toggleSubtitle(index: int): void {
        const next = root.subtitleChoices.slice();
        next[index] = !next[index];
        root.subtitleChoices = next;
    }

    function toggleAllSubtitles(): void {
        const all = root.selectedSubtitleCount === root.plan.subtitles.candidates.length;
        root.subtitleChoices = root.plan.subtitles.candidates.map(() => !all);
    }

    title: root.closeOnly ? "Import Error" : "Confirm Import"
    modal: false
    visible: true
    closePolicy: Popup.NoAutoClose
    standardButtons: Dialog.NoButton
    contentWidth: MpvqcConstants.mediumDialogContentWidth
    contentHeight: MpvqcConstants.mediumDialogContentHeight

    contentItem: SectionScroll {
        sectionSpacing: root._sectionSpacing

            SectionCard {
                contentSpacing: 10
                visible: root.plan.commentCount > 0 || root.plan.video.load !== ""
                    || root.plan.subtitles.load.length > 0 || root.plan.rejectedDocuments.length > 0

                Layout.fillWidth: true
                Layout.topMargin: root._sectionSpacing

                SummaryRow {
                    visible: root.plan.commentCount > 0
                    icon: MpvqcIcons.comment
                    text: root.plan.commentCount + " comments will be imported"

                    Layout.fillWidth: true
                }

                SummaryRow {
                    visible: root.plan.video.resolved && root.plan.video.load !== ""
                    icon: MpvqcIcons.movie
                    text: root.plan.video.load
                    fullPath: "/mnt/media/QC/Episode 03/" + root.plan.video.load
                    trailing: "will be loaded"

                    Layout.fillWidth: true
                }

                Repeater {
                    model: root.plan.subtitles.load

                    delegate: SummaryRow {
                        required property string modelData

                        icon: MpvqcIcons.subtitles
                        text: modelData
                        fullPath: "/mnt/media/QC/Episode 03/" + modelData
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
                        fullPath: "/mnt/media/QC/Episode 03/" + modelData.filename
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

            SectionCard {
                title: "Your current comments"
                visible: !root.plan.session.resolved

                Layout.fillWidth: true

                Label {
                    text: "You already have comments in this session."
                    verticalAlignment: Text.AlignVCenter

                    Layout.fillWidth: true
                    Layout.minimumHeight: 32
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

                Label {
                    text: "Which video should be loaded?"
                    verticalAlignment: Text.AlignVCenter

                    Layout.fillWidth: true
                    Layout.minimumHeight: 32
                }

                Repeater {
                    model: root.plan.video.candidates

                    delegate: OptionRow {
                        required property int index
                        required property var modelData

                        selected: root.videoChoice === index
                        text: modelData.name
                        fullPath: "/mnt/media/QC/Episode 03/" + modelData.name
                        fromDocument: modelData.fromDocument
                        fromSubtitle: modelData.fromSubtitle

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

                RowLayout {
                    spacing: 8

                    Layout.fillWidth: true
                    Layout.minimumHeight: 32

                    Label {
                        text: "Which subtitles should be loaded?"
                        wrapMode: Text.Wrap

                        Layout.fillWidth: true
                    }

                    SelectAllCheckBox {
                        visible: root.plan.subtitles.candidates.length > 1
                        checkedCount: root.selectedSubtitleCount
                        totalCount: root.plan.subtitles.candidates.length

                        onToggleAllRequested: root.toggleAllSubtitles()
                    }
                }

                Repeater {
                    model: root.plan.subtitles.candidates

                    delegate: CheckRow {
                        required property int index
                        required property string modelData

                        isChecked: root.subtitleChoices[index] === true
                        text: modelData
                        fullPath: "/mnt/media/QC/Episode 03/" + modelData

                        Layout.fillWidth: true

                        onToggleRequested: root.toggleSubtitle(index)
                    }
                }
            }
    }

    footer: PrototypeFooter {
        primaryLabel: root.closeOnly ? "Close" : "Confirm import"
        showCancel: !root.closeOnly
    }
}
