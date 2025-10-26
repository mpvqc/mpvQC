// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls.Material
import QtQuick.Layouts

import "../components"

MpvqcDialog {
    id: root

    required property string videosJson
    required property string subtitlesJson

    readonly property var viewModel: MpvqcImportConfirmationDialogViewModel {
        videosJson: root.videosJson
        subtitlesJson: root.subtitlesJson
    }

    readonly property var dimensions: QtObject {
        readonly property int columnSpacing: 10
        readonly property int sectionSpacing: 20
        readonly property int rowSpacing: 10
        readonly property int listSpacing: 0
        readonly property int iconSize: 24
        readonly property int contentTopMargin: 10
        readonly property int noMargin: 0
        readonly property int itemVerticalPadding: 12
        readonly property int itemHorizontalPadding: 15
    }

    signal importConfirmed(selectedVideoPath: string, selectedSubtitlePaths: list<string>)

    contentWidth: 500

    //: Dialog title for confirming which videos and subtitles to import
    title: qsTranslate("ImportConfirmationDialog", "Confirm Import")
    standardButtons: Dialog.Ok
    closePolicy: Popup.NoAutoClose

    onAccepted: {
        const selected = root.viewModel.getSelectedItems();
        importConfirmed(selected.video, selected.subtitles);
    }

    onRejected: importConfirmed("", [])

    contentItem: ColumnLayout {
        spacing: root.dimensions.columnSpacing

        MpvqcHeader {
            //: Section header for video selection list
            text: qsTranslate("ImportConfirmationDialog", "Videos")
            visible: root.viewModel.showHeaders

            Layout.fillWidth: true
            Layout.topMargin: root.dimensions.contentTopMargin
        }

        ListView {
            id: _videoListView

            Layout.fillWidth: true
            Layout.topMargin: root.viewModel.showHeaders ? root.dimensions.noMargin : root.dimensions.contentTopMargin
            Layout.preferredHeight: contentHeight

            model: root.viewModel.videosWithSkipOption

            visible: root.viewModel.hasVideos
            spacing: root.dimensions.listSpacing
            interactive: false

            delegate: ItemDelegate {
                id: _delegate

                required property var modelData
                required property int index

                //: Option to import without selecting any video
                readonly property string skipVideoText: qsTranslate("ImportConfirmationDialog", "Skip video")

                width: _videoListView.width
                topPadding: root.dimensions.itemVerticalPadding
                bottomPadding: root.dimensions.itemVerticalPadding
                leftPadding: root.dimensions.itemHorizontalPadding
                rightPadding: root.dimensions.itemHorizontalPadding

                onPressed: root.viewModel.selectVideo(index)

                contentItem: RowLayout {
                    spacing: root.dimensions.rowSpacing

                    MpvqcIconLabel {
                        icon.source: index === root.viewModel.selectedVideoIndex ? "qrc:/data/icons/select_check_box_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg" : "qrc:/data/icons/select_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
                        icon {
                            width: root.dimensions.iconSize
                            height: root.dimensions.iconSize
                        }
                    }

                    Label {
                        Layout.fillWidth: true

                        text: _delegate.modelData.isNoVideo ? _delegate.skipVideoText : _delegate.modelData.filename
                        font.italic: _delegate.modelData.isNoVideo ?? false
                        elide: Text.ElideLeft
                        wrapMode: Label.Wrap
                        horizontalAlignment: Text.AlignLeft
                    }

                    MpvqcIconLabel {
                        visible: _delegate.modelData.fromDocument
                        //: Tooltip indicating the video file was referenced in one of the imported documents
                        toolTipText: qsTranslate("ImportConfirmationDialog", "From QC document")

                        icon {
                            width: root.dimensions.iconSize
                            height: root.dimensions.iconSize
                            source: "qrc:/data/icons/description_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
                        }

                        opacity: 0.3
                    }

                    MpvqcIconLabel {
                        visible: _delegate.modelData.fromSubtitle
                        //: Tooltip indicating the video file was referenced in one of the imported subtitles
                        toolTipText: qsTranslate("ImportConfirmationDialog", "From subtitle")

                        icon {
                            width: root.dimensions.iconSize
                            height: root.dimensions.iconSize
                            source: "qrc:/data/icons/subtitles_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
                        }

                        opacity: 0.3
                    }
                }
            }
        }

        RowLayout {
            visible: root.viewModel.showHeaders

            Layout.fillWidth: true
            Layout.topMargin: root.viewModel.hasVideos ? root.dimensions.sectionSpacing : root.dimensions.contentTopMargin

            MpvqcHeader {
                Layout.fillWidth: true

                //: Section header for subtitle selection list
                text: qsTranslate("ImportConfirmationDialog", "Subtitles")
            }

            Button {
                //: Button to select all subtitles in the list
                text: qsTranslate("ImportConfirmationDialog", "Select All")
                visible: root.viewModel.showSubtitleBatchSelectionControls
                flat: true

                Material.foreground: Material.accent

                onPressed: root.viewModel.selectAllSubtitles()
            }

            Button {
                //: Button to deselect all subtitles in the list
                text: qsTranslate("ImportConfirmationDialog", "Deselect All")
                visible: root.viewModel.showSubtitleBatchSelectionControls
                flat: true

                Material.foreground: Material.accent

                onPressed: root.viewModel.deselectAllSubtitles()
            }
        }

        ListView {
            id: _subtitleListView

            Layout.fillWidth: true
            Layout.preferredHeight: contentHeight

            model: root.viewModel.subtitles

            visible: root.viewModel.hasSubtitles
            spacing: root.dimensions.listSpacing
            interactive: false

            delegate: ItemDelegate {
                id: _subtitleDelegate

                required property var modelData
                required property int index

                width: _subtitleListView.width
                checked: modelData.checked
                topPadding: root.dimensions.itemVerticalPadding
                bottomPadding: root.dimensions.itemVerticalPadding
                leftPadding: root.dimensions.itemHorizontalPadding
                rightPadding: root.dimensions.itemHorizontalPadding

                onPressed: root.viewModel.toggleSubtitle(index)

                contentItem: RowLayout {
                    spacing: root.dimensions.rowSpacing

                    MpvqcIconLabel {
                        icon.source: _subtitleDelegate.checked ? "qrc:/data/icons/select_check_box_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg" : "qrc:/data/icons/select_24dp_1F1F1F_FILL0_wght400_GRAD0_opsz24.svg"
                        icon {
                            width: root.dimensions.iconSize
                            height: root.dimensions.iconSize
                        }
                    }

                    Label {
                        Layout.fillWidth: true

                        text: _subtitleDelegate.modelData.filename
                        elide: Text.ElideLeft
                        wrapMode: Label.Wrap
                        horizontalAlignment: Text.AlignLeft
                    }
                }
            }
        }
    }

    Connections {
        target: root.viewModel

        function onModelChanged(): void {
            _subtitleListView.model = root.viewModel.subtitles;
        }
    }
}
