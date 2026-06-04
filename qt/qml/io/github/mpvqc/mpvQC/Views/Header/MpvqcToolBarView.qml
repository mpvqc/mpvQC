// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls

import io.github.mpvqc.mpvQC.Python
import io.github.mpvqc.mpvQC.Utility

Item {
    id: root

    readonly property MpvqcToolBarViewModel viewModel: MpvqcToolBarViewModel {}

    readonly property int buttonPadding: 6
    readonly property int buttonSize: height - root.buttonPadding
    readonly property int itemSpacing: 2
    readonly property int groupSepWidth: 8
    readonly property int animationDuration: 50

    readonly property bool anyButtonVisible: root.viewModel.frameStepActive || root.viewModel.subtitleActive || root.viewModel.audioActive

    width: _row.width

    component MpvqcToolBarSlot: Item {
        id: _slot

        required property int leadingPx
        required property bool active

        default property alias _content: _container.data

        readonly property int naturalWidth: leadingPx + contentWidth

        property int contentWidth: root.buttonSize
        property bool visualActive: false
        property int delay: 0

        width: visualActive ? naturalWidth : 0
        height: root.buttonSize
        opacity: visualActive ? 1 : 0
        visible: visualActive || width > 0
        clip: true

        onActiveChanged: _stagger.schedule(_slot)

        Item {
            id: _container

            anchors.right: parent.right
            width: _slot.contentWidth
            height: root.buttonSize
        }

        Behavior on width {
            SequentialAnimation {
                PauseAnimation {
                    duration: _slot.delay
                }
                NumberAnimation {
                    duration: root.animationDuration
                }
            }
        }

        Behavior on opacity {
            SequentialAnimation {
                PauseAnimation {
                    duration: _slot.delay
                }
                NumberAnimation {
                    duration: root.animationDuration
                }
            }
        }
    }

    QtObject {
        id: _stagger

        property list<MpvqcToolBarSlot> pending: []

        function schedule(slot: MpvqcToolBarSlot): void {
            pending.push(slot);
            Qt.callLater(flush);
        }

        function flush(): void {
            const pendingSet = new Set(pending);
            pending = [];

            const ordered = [];
            for (const child of _row.children) {
                if (pendingSet.has(child))
                    ordered.push(child);
            }

            const activating = ordered.filter(s => s.active && !s.visualActive);
            const deactivating = ordered.filter(s => !s.active && s.visualActive).reverse();

            activating.forEach((slot, i) => {
                slot.delay = i * root.animationDuration;
                slot.visualActive = true;
            });
            deactivating.forEach((slot, i) => {
                slot.delay = i * root.animationDuration;
                slot.visualActive = false;
            });
        }
    }

    Row {
        id: _row

        anchors.verticalCenter: parent.verticalCenter
        spacing: 0

        MpvqcToolBarSlot {
            leadingPx: 0
            contentWidth: _separator.implicitWidth
            active: root.anyButtonVisible

            ToolSeparator {
                id: _separator
                anchors.verticalCenter: parent.verticalCenter
                height: 32
            }
        }

        MpvqcToolBarSlot {
            leadingPx: 0
            active: root.viewModel.frameStepActive

            MpvqcToolBarButton {
                size: root.buttonSize
                iconSource: LayoutMirroring.enabled ? MpvqcIcons.lastPage : MpvqcIcons.firstPage
                toolTipText: {
                    if (LayoutMirroring.enabled) {
                        //: Tooltip for 'Frame Step Forward', %1 will be the default shortcut button identifier
                        return qsTranslate("ToolBar", "Frame Step Forward (%1)").arg(" . ");
                    } else {
                        //: Tooltip for 'Frame Step Backward', %1 will be the default shortcut button identifier
                        return qsTranslate("ToolBar", "Frame Step Backward (%1)").arg(" , ");
                    }
                }
                onPressed: {
                    if (LayoutMirroring.enabled) {
                        root.viewModel.requestFrameStepForward();
                    } else {
                        root.viewModel.requestFrameStepBackward();
                    }
                }
            }
        }

        MpvqcToolBarSlot {
            leadingPx: root.itemSpacing
            active: root.viewModel.frameStepActive

            MpvqcToolBarButton {
                size: root.buttonSize
                iconSource: LayoutMirroring.enabled ? MpvqcIcons.firstPage : MpvqcIcons.lastPage
                toolTipText: {
                    if (LayoutMirroring.enabled) {
                        //: Tooltip for 'Frame Step Backward', %1 will be the default shortcut button identifier
                        return qsTranslate("ToolBar", "Frame Step Backward (%1)").arg(" , ");
                    } else {
                        //: Tooltip for 'Frame Step Forward', %1 will be the default shortcut button identifier
                        return qsTranslate("ToolBar", "Frame Step Forward (%1)").arg(" . ");
                    }
                }
                onPressed: {
                    if (LayoutMirroring.enabled) {
                        root.viewModel.requestFrameStepBackward();
                    } else {
                        root.viewModel.requestFrameStepForward();
                    }
                }
            }
        }

        MpvqcToolBarSlot {
            leadingPx: root.itemSpacing
            contentWidth: root.groupSepWidth
            active: root.viewModel.subtitleActive || root.viewModel.audioActive
        }

        MpvqcToolBarSlot {
            leadingPx: root.itemSpacing
            active: root.viewModel.subtitleActive

            MpvqcToolBarButton {
                size: root.buttonSize
                iconSource: MpvqcIcons.subtitles
                //: Tooltip for 'Cycle Subtitle Track', %1 will be the default shortcut button identifier
                toolTipText: qsTranslate("ToolBar", "Cycle Subtitle Track (%1)").arg("J")
                onPressed: root.viewModel.requestCycleSubtitleTrack()
            }
        }

        MpvqcToolBarSlot {
            leadingPx: root.itemSpacing
            active: root.viewModel.audioActive

            MpvqcToolBarButton {
                size: root.buttonSize
                iconSource: MpvqcIcons.musicNote
                //: Tooltip for 'Cycle Audio Track', %1 will be the default shortcut button identifier
                toolTipText: qsTranslate("ToolBar", "Cycle Audio Track (%1)").arg("#")
                onPressed: root.viewModel.requestCycleAudioTrack()
            }
        }
    }
}
