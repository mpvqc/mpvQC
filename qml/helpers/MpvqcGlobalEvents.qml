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


QtObject {

    property int commentCount: 0
    property int selectedCommentIndex: 0

    signal commentsChanged()
    signal commentsResetRequested()
    signal customPlayerCommandRequested(string command)
    signal focusShiftToTableRequested()
    signal editSelectedCommentRequested()
    signal newCommentRequested(string commentType)
    signal newCommentMenuRequested()
    signal videoPauseRequested()
    signal videoPositionRequested(int seconds)

    function notifyCommentsChanged() {
        commentsChanged()
    }

    function requestCommentsReset() {
        commentsResetRequested()
    }

    function requestCustomPlayerCommand(command) {
        customPlayerCommandRequested(command)
    }

    function requestEditSelectedComment() {
        editSelectedCommentRequested()
    }

    function requestFocusShiftToTable() {
        focusShiftToTableRequested()
    }

    function requestNewComment(commentType) {
        newCommentRequested(commentType)
    }

    function requestNewCommentMenu() {
        newCommentMenuRequested()
    }

    function requestVideoPause() {
        videoPauseRequested()
    }

    function requestVideoPosition(seconds) {
        videoPositionRequested(seconds)
    }

}
