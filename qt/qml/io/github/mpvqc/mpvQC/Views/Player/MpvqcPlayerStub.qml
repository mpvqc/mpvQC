// SPDX-FileCopyrightText: mpvQC developers
//
// SPDX-License-Identifier: GPL-3.0-or-later

import QtQuick

Item {
    // Stand-in for the real mpv player used by QML tests. The native FBO requires a real GL surface
    // and cannot be re-instantiated cleanly between tests, so MpvqcPlayerView swaps it out via the
    // `mpvqcTestMode` context property in our test setup.
}
