#!/usr/bin/env python3

# Copyright (C) 2016 Frechdachs <frechdachs@rekt.cc>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

try:
    from mpv import MPV  # https://github.com/jaseg/python-mpv
except ImportError:
    pass
try:
    from mpv_python_ipc import MpvProcess  # https://github.com/siikamiika/mpv-python-ipc
except ImportError:
    pass
from PyQt5.QtCore import Qt, QObject, QTimer, QEvent, QPoint
from PyQt5.QtGui import (QStandardItemModel, QStandardItem, QCursor, QIcon,
                        QFont, QColor, QPalette, QFontDatabase, QFontMetrics,
                        QTextOption)
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget,
                            QAbstractItemView, QTableView, QStyledItemDelegate,
                            QVBoxLayout, QHBoxLayout, QDialog, QMessageBox,
                            QLabel, QLineEdit, QTextEdit, QTextBrowser,
                            QPushButton, QTabWidget, QGroupBox, QSpinBox,
                            QSplitter, QDesktopWidget, QFileDialog, QMenu,
                            QAction, QActionGroup, QStyleFactory, QFrame)
import sys
from os import path, mkdir, remove
import platform
import datetime
from zipfile import ZipFile, ZIP_DEFLATED
from operator import itemgetter
from traceback import format_exception
from functools import partial
from random import randint
import gettext
import locale
import requests  # https://github.com/kennethreitz/requests


# If this global variable is set to 'True', mpv will be used
# in a slave-mode-kinda way instead of libmpv
mpvslave = False


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        topmenubar = self.menuBar()

        newaction = QAction(_("New QC Document"), self)
        newaction.setShortcut("Ctrl+N")
        openaction = QAction(_("Open QC Document..."), self)
        openaction.setShortcut("Ctrl+O")
        saveaction = QAction(_("Save QC Document"), self)
        saveaction.setShortcut("Ctrl+S")
        saveasaction = QAction(_("Save QC Document as..."), self)
        saveasaction.setShortcut("Ctrl+Shift+S")
        closeaction = QAction(_("Exit"), self)
        closeaction.setShortcut("Ctrl+Q")
        videoopenaction = QAction(_("Open Video File..."), self)
        videoopenaction.setShortcut("Ctrl+Shift+O")
        videoresizeaction = QAction(_("Resize Video to its Original Resolution"), self)
        videoresizeaction.setShortcut("Ctrl+R")
        nicknameaction = QAction(_("Nickname..."), self)
        commenttypeaction = QAction(_("Comment Types..."), self)
        autosaveintervalaction = QAction(_("Autosave Interval..."), self)
        inputconfaction = QAction(_("Edit input.conf..."), self)
        mpvconfaction = QAction(_("Edit mpv.conf..."), self)
        restoreaction = QAction(_("Restore Default Configuration"), self)
        englishaction = QAction(_("English"), self)
        englishaction.setCheckable(True)
        germanaction = QAction(_("German"), self)
        germanaction.setCheckable(True)
        languageactiongroup = QActionGroup(self)
        languageactiongroup.addAction(englishaction)
        languageactiongroup.addAction(germanaction)
        if language == "de":
            germanaction.setChecked(True)
        else:
            englishaction.setChecked(True)
        updateaction = QAction(_("Check for Updates..."), self)
        aboutqtaction = QAction(_("About Qt"), self)
        aboutaction = QAction(_("About {}").format(v.split(" ")[0]), self)

        newaction.triggered.connect(newQcFile)
        openaction.triggered.connect(openQcFile)
        saveaction.triggered.connect(saveQcFile)
        saveasaction.triggered.connect(saveQcFileAs)
        closeaction.triggered.connect(self.closeEvent)
        videoopenaction.triggered.connect(openVideoFile)
        videoresizeaction.triggered.connect(resizeVideo)
        nicknameaction.triggered.connect(openOptionsDialogNickname)
        commenttypeaction.triggered.connect(openOptionsDialogCommentTypes)
        autosaveintervalaction.triggered.connect(openOptionsDialogAutosaveInterval)
        inputconfaction.triggered.connect(openInputConfOptionDialog)
        mpvconfaction.triggered.connect(openMpvConfOptionDialog)
        restoreaction.triggered.connect(restoreDefaultConfiguration)
        englishaction.triggered.connect(partial(setOption, "language", "en"))
        germanaction.triggered.connect(partial(setOption, "language", "de"))
        updateaction.triggered.connect(checkForUpdates)
        aboutqtaction.triggered.connect(QApplication.instance().aboutQt)
        aboutaction.triggered.connect(openAboutDialog)

        filemenu = topmenubar.addMenu(_("File"))
        filemenu.addAction(newaction)
        filemenu.addAction(openaction)
        filemenu.addAction(saveaction)
        filemenu.addAction(saveasaction)
        filemenu.addSeparator()
        filemenu.addAction(closeaction)
        videomenu = topmenubar.addMenu(_("Video"))
        videomenu.addAction(videoopenaction)
        videomenu.addSeparator()
        videomenu.addAction(videoresizeaction)

        optionsmenu = topmenubar.addMenu(_("Options"))
        optionsmenu.addAction(nicknameaction)
        optionsmenu.addAction(commenttypeaction)
        optionsmenu.addAction(autosaveintervalaction)
        languagemenu = optionsmenu.addMenu(_("Language"))
        languagemenu.addAction(englishaction)
        languagemenu.addAction(germanaction)
        optionsmenu.addSeparator()
        optionsmenu.addAction(inputconfaction)
        optionsmenu.addAction(mpvconfaction)
        optionsmenu.addSeparator()
        optionsmenu.addAction(restoreaction)

        helpmenu = topmenubar.addMenu(_("Help"))
        helpmenu.addAction(updateaction)
        helpmenu.addSeparator()
        helpmenu.addAction(aboutqtaction)
        helpmenu.addAction(aboutaction)

        self.mpvwindow = MpvWindow(self)
        self.mpvwindow.addAction(newaction)
        self.mpvwindow.addAction(openaction)
        self.mpvwindow.addAction(saveaction)
        self.mpvwindow.addAction(saveasaction)
        self.mpvwindow.addAction(closeaction)
        self.mpvwindow.addAction(videoopenaction)
        self.mpvwindow.addAction(videoresizeaction)

        self.setAcceptDrops(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenu)

    def closeEvent(self, event=None):
        if event:
            event.ignore()
        if mpvslave:
            try:
                setPause()
            except OSError:
                pass
            if self.isFullScreen():
                cycleFullscreen()
            if not currentstatesaved and WarningMessageBox(
                                        self,
                                        _("Warning"),
                                        _("Do you really want to quit without saving?"),
                                        question=True,
                                        ).exec_() != 0:
                return
            self.mpvwindow.close()
            try:
                mp.commandv("quit")
            except OSError:
                pass
        else:
            setPause()
            if self.isFullScreen():
                cycleFullscreen()
            if not currentstatesaved and WarningMessageBox(
                                        self,
                                        _("Warning"),
                                        _("Do you really want to quit without saving?"),
                                        question=True,
                                        ).exec_() != 0:
                return
            mp.terminate()
        sys.exit()

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        filename = event.mimeData().urls()[0].toLocalFile()
        if not path.isfile(filename):
            return
        if mainwindow.mpvwindow.geometry().contains(event.pos()):
            openVideoFile(filename)
        else:
            openQcFile(filename)

    def contextMenu(self, pos=None):
        setPause()
        exitFullscreen()
        contextmenu = QMenu()
        for x in commenttypeoptions:
            contextmenu.addAction(x).triggered.connect(partial(newComment, x))
        m_pos = QCursor.pos()
        # Fixes following: Qt puts the context menu in a place
        # where double clicking would trigger the fist menu option
        # instead of just calling the menu a second time
        # or ignoring the second press
        m_pos = QPoint(m_pos.x()+1, m_pos.y())
        contextmenu.exec_(m_pos)


class MpvWindow(QFrame):

    def __init__(self, parent=None):
        super(MpvWindow, self).__init__(parent)
        # Make the frame black, so that the video frame
        # is distinguishable from the rest when no
        # video is loaded yet
        self.setStyleSheet("background-color:black;")
        self.setMouseTracking(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenu)
        self.cursortimer = QTimer(self)
        self.cursortimer.setSingleShot(True)
        self.cursortimer.timeout.connect(hideCursor)

    def contextMenu(self, pos=None):
        setPause()
        exitFullscreen()
        contextmenu = QMenu()
        for x in commenttypeoptions:
            contextmenu.addAction(x).triggered.connect(partial(newComment, x))
        m_pos = QCursor.pos()
        # Fixes following: Qt puts the context menu in a place
        # where double clicking would trigger the fist menu option
        # instead of just calling the menu a second time
        # or ignoring the second press
        m_pos = QPoint(m_pos.x()+1, m_pos.y())
        contextmenu.exec_(m_pos)


class MainWindowEventFilter(QObject):

    def eventFilter(self, receiver, event):
        def commandGenerator(keymodifiers, keystring, modrequired=False, ischar=False):
            shift = None
            ctrl = None
            alt = None
            if keymodifiers & Qt.SHIFT:
                shift = "shift"
            if keymodifiers & Qt.CTRL:
                ctrl = "ctrl"
            if keymodifiers & Qt.ALT:
                alt = "alt"
            if modrequired and not (shift or ctrl or alt):
                return None
            if ischar:
                alphanumerics = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÀÁÂÃÇÉÈÊËÍÌÎÏÑÓÒÔÕÚÙÛÝŸ"
                if not keystring in alphanumerics and sys.platform.startswith("win32"):
                    ctrl = None
                    alt = None
                if not shift and keystring in alphanumerics:
                    keystring = keystring.lower()
                shift = None
            keystring = "+".join([x for x in [shift, ctrl, alt, keystring] if x])
            return ("keypress", keystring)

        keymappings = {Qt.Key_PageUp: ("PGUP",),
                       Qt.Key_PageDown: ("PGDWN",),
                       Qt.Key_Play: ("PLAY",),
                       Qt.Key_Pause: ("PAUSE",),
                       Qt.Key_Stop: ("STOP",),
                       Qt.Key_Forward: ("FORWARD",),
                       Qt.Key_Back: ("REWIND",),
                       Qt.Key_MediaPlay: ("PLAY",),
                       Qt.Key_MediaStop: ("STOP",),
                       Qt.Key_MediaNext: ("NEXT",),
                       Qt.Key_MediaPrevious: ("PREV",),
                       Qt.Key_MediaPause: ("PAUSE",),
                       Qt.Key_MediaTogglePlayPause: ("PLAYPAUSE",),
                       Qt.Key_Home: ("HOME",),
                       Qt.Key_End: ("END",),
                       Qt.Key_Escape: ("ESC",),
                       Qt.Key_Left: ("LEFT",),
                       Qt.Key_Right: ("RIGHT",),
                       Qt.Key_Up: ("UP", True),
                       Qt.Key_Down: ("DOWN", True),
                       }

        if event.type() == QEvent.Resize:
                afterResize()
                return True
        elif event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.MiddleButton:
                mp.command("keypress", "MOUSE_BTN1")
                return True
            elif event.button() == Qt.BackButton:
                mp.command("keypress", "MOUSE_BTN5")
                return True
            elif event.button() == Qt.ForwardButton:
                mp.command("keypress", "MOUSE_BTN6")
                return True
        elif event.type() == QEvent.MouseButtonDblClick:
            if event.button() == Qt.MiddleButton:
                mp.command("keypress", "MOUSE_BTN1")
                return True
            elif event.button() == Qt.BackButton:
                mp.command("keypress", "MOUSE_BTN5")
                return True
            elif event.button() == Qt.ForwardButton:
                mp.command("keypress", "MOUSE_BTN6")
                return True
        elif event.type() == QEvent.KeyPress:
            pressedkey = event.key()
            keymodifiers = int(app.keyboardModifiers())
            if pressedkey == Qt.Key_F and keymodifiers == Qt.NoModifier:
                cycleFullscreen()
                return True
            elif pressedkey == Qt.Key_E and keymodifiers == Qt.NoModifier:
                receiver.contextMenu()
                return True
            elif pressedkey == Qt.Key_Escape and keymodifiers == Qt.NoModifier:
                exitFullscreen()
                return True
            elif pressedkey in keymappings:
                command = commandGenerator(keymodifiers, *keymappings[pressedkey])
                if command:
                    mp.command(*command)
                    return True
            elif pressedkey != 0:  # Sending a null character results in an exception
                try:
                    keystring = chr(pressedkey)
                except ValueError:  # Key is unhandled and is no char
                    pass
                else:
                    command = commandGenerator(keymodifiers, keystring, ischar=True)
                    mp.command(*command)
                    return True
        return super(MainWindowEventFilter, self).eventFilter(receiver, event)


class MpvWindowEventFilter(QObject):

    def eventFilter(self, receiver, event):
        if event.type() == QEvent.MouseMove:
            mainwindowgeo = mainwindow.geometry()
            centralwidgetgeo = (
                                mainwindow
                                .centralWidget()
                                .geometry()
                                )
            if not mainwindow.isFullScreen():
                pos_x = (
                    -mainwindowgeo.x()
                    -centralwidgetgeo.x()
                    +QCursor.pos().x()
                    )
                pos_y = (
                    -mainwindowgeo.y()
                    -centralwidgetgeo.y()
                    +QCursor.pos().y()
                    )
            else:
                pos_x = event.pos().x()
                pos_y = event.pos().y()
            try:
                mp.command("mouse", pos_x, pos_y)
            except OSError:  # Stop the spamming of error messages while moving mouse if mpv (in slave mode) crashed
                print("mpv probably crashed. Please restart the application.")
            if mainwindow.isFullScreen():
                showCursor()
            return True
        elif event.type() == QEvent.MouseButtonPress:
            receiver.setFocus()  # If a comment line is currently being edited, then a click on the video area
                                 # should close the editor, which is implicitly done by removing keyboard focus
            commentlistview.setFocus()
            if event.button() == Qt.LeftButton:
                mp.command("keydown", "MOUSE_BTN0")
            if event.button() == Qt.MiddleButton:
                mp.command("keypress", "MOUSE_BTN1")
            if event.button() == Qt.BackButton:
                mp.command("keypress", "MOUSE_BTN5")
            if event.button() == Qt.ForwardButton:
                mp.command("keypress", "MOUSE_BTN6")
            return True
        elif event.type() == QEvent.MouseButtonRelease:
            if event.button() == Qt.LeftButton:
                mp.command("keyup", "MOUSE_BTN0")
            return True
        elif event.type() == QEvent.MouseButtonDblClick:
            if event.button() == Qt.LeftButton:
                cycleFullscreen()
                mp.command("keypress", "MOUSE_BTN0")
                return True
            elif event.button() == Qt.MiddleButton:
                mp.command("keypress", "MOUSE_BTN1")
                return True
            elif event.button() == Qt.BackButton:
                mp.command("keypress", "MOUSE_BTN5")
                return True
            elif event.button() == Qt.ForwardButton:
                mp.command("keypress", "MOUSE_BTN6")
                return True
        elif event.type() == QEvent.Wheel:
            xdelta = event.angleDelta().x()
            ydelta = event.angleDelta().y()
            if xdelta == 0 and ydelta != 0:
                if ydelta > 0:
                    mp.command("keypress", "MOUSE_BTN3")
                else:
                    mp.command("keypress", "MOUSE_BTN4")
                return True
        return super(MpvWindowEventFilter, self).eventFilter(receiver, event)


class RegularTextEdit(QTextEdit):

    def __init__(self, parent=None):
        super(RegularTextEdit, self).__init__(parent)
        self.setAcceptRichText(False)
        self.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont))

    def mousePressEvent(self, event):
        """ Disable stupid dragging feature """
        if event.button() == Qt.LeftButton:
            newcursor = self.cursorForPosition(event.pos())
            self.setTextCursor(newcursor)
            event.accept()
        super(RegularTextEdit, self).mousePressEvent(event)


class OptionsDialog(QDialog):

    def __init__(self, parent, labeltext, entrytext, buttontext, option):
        super(OptionsDialog, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setWindowFlags(self.windowFlags()&~Qt.WindowContextHelpButtonHint)
        self.option = option
        self.layout = QVBoxLayout()
        self.label = QLabel(labeltext)
        self.entry = QLineEdit(entrytext)
        self.entry.setAlignment(Qt.AlignCenter)
        entrytextwidth = self.entry.fontMetrics().width(entrytext)
        self.entry.setMinimumWidth(entrytextwidth+10)
        self.button = QPushButton(buttontext)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.entry)
        self.layout.addWidget(self.button)
        self.layout.setAlignment(self.label, Qt.AlignHCenter)
        self.layout.setAlignment(self.entry, Qt.AlignHCenter)
        self.layout.setAlignment(self.button, Qt.AlignHCenter)
        self.button.clicked.connect(self.accept)
        self.entry.returnPressed.connect(self.accept)
        self.setLayout(self.layout)

    def accept(self):
        entrytext = self.entry.text().strip()
        if entrytext:
            setOption(self.option, entrytext)
        self.done(1)


class TextEditOptionDialog(QDialog):

    def __init__(self, parent, relativeconfpath):
        super(TextEditOptionDialog, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setWindowFlags(self.windowFlags()&~Qt.WindowContextHelpButtonHint)
        self.conf = path.join(programlocation, relativeconfpath)
        with open(self.conf, "r", encoding="utf-8") as configfile:
            config = configfile.read()
        self.resize(640, 480)
        self.layout = QVBoxLayout()
        self.editor = RegularTextEdit()
        self.button = QPushButton(_("OK"))
        self.editor.setPlainText(config)
        self.editor.setWordWrapMode(QTextOption.NoWrap)
        self.layout.addWidget(self.editor)
        self.layout.addWidget(self.button)
        self.layout.setAlignment(self.button, Qt.AlignHCenter)
        self.button.clicked.connect(self.accept)
        self.setLayout(self.layout)

    def accept(self):
        with open(self.conf, "w", encoding="utf-8") as configfile:
            config = self.editor.toPlainText()
            configfile.write(config)
        self.done(1)


class AboutDialog(QDialog):

    def __init__(self, parent):
        super(AboutDialog, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setWindowFlags(self.windowFlags()&~Qt.WindowContextHelpButtonHint)
        self.resize(300, 300)
        self.layout = QVBoxLayout()
        self.tabwidget = QTabWidget()
        self.button = QPushButton(_("OK"))
        self.button.clicked.connect(self.accept)

        self.about = QTextBrowser()
        self.about.setOpenExternalLinks(True)
        self.about.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        self.about.setHtml(_("<h1 style='text-align:center;'>{} - {}</h1><p><b>{}</b> is a free, open source and <b>libmpv</b> based application for the quick and easy creation of quality control reports of video files.</p><p>Copyright © 2016 Frechdachs<br>&lt;frechdachs@rekt.cc&gt;</p><p><a href='https://mpvqc.rekt.cc/'>https://mpvqc.rekt.cc/</a></p>").format(v, platform.architecture()[0], v.split(" ")[0]))

        self.credits = QTextBrowser()
        self.credits.setTextInteractionFlags(Qt.NoTextInteraction)
        self.credits.setHtml("<p>mpv<br>GPLv2+ &lt;mpv.io&gt;</p><p>libmpv build<br>GPLv3 &lt;lachs0r&gt;</p><p>python-mpv<br>AGPLv3 &lt;jaseg&gt;</p><p>PyQt5<br>GPLv3 &lt;Riverbank Computing Limited&gt;</p><p>Qt5<br>LGPLv3 &lt;The Qt Company Ltd and other contributors&gt;</p><p>Requests<br>Apache Version 2 &lt;Kenneth Reitz&gt;</p>")

        self.license = QTextBrowser()
        self.license.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.license.setHtml("""<p style='text-align:center;'>GNU GENERAL PUBLIC LICENSE<br>Version 3, 29 June 2007</p><p>Copyright (C) 2007 Free Software Foundation, Inc. &lt;http://fsf.org/&gt;<br>Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed.</p><p style='text-align:center;'>Preamble</p><p>The GNU General Public License is a free, copyleft license for software and other kinds of works.</p><p>The licenses for most software and other practical works are designed to take away your freedom to share and change the works.  By contrast, the GNU General Public License is intended to guarantee your freedom to share and change all versions of a program--to make sure it remains free software for all its users.  We, the Free Software Foundation, use the GNU General Public License for most of our software; it applies also to any other work released this way by its authors.  You can apply it to your programs, too.</p><p>When we speak of free software, we are referring to freedom, not price.<br>Our General Public Licenses are designed to make sure that you have the freedom to distribute copies of free software (and charge for them if you wish), that you receive source code or can get it if you want it, that you can change the software or use pieces of it in new free programs, and that you know you can do these things.</p><p>To protect your rights, we need to prevent others from denying you these rights or asking you to surrender the rights.  Therefore, you have certain responsibilities if you distribute copies of the software, or if you modify it: responsibilities to respect the freedom of others.</p><p>For example, if you distribute copies of such a program, whether gratis or for a fee, you must pass on to the recipients the same freedoms that you received.  You must make sure that they, too, receive or can get the source code.  And you must show them these terms so they know their rights.</p><p>Developers that use the GNU GPL protect your rights with two steps: (1) assert copyright on the software, and (2) offer you this License giving you legal permission to copy, distribute and/or modify it.</p><p>For the developers' and authors' protection, the GPL clearly explains that there is no warranty for this free software.  For both users' and authors' sake, the GPL requires that modified versions be marked as changed, so that their problems will not be attributed erroneously to authors of previous versions.</p><p>Some devices are designed to deny users access to install or run modified versions of the software inside them, although the manufacturer can do so.  This is fundamentally incompatible with the aim of protecting users' freedom to change the software.  The systematic pattern of such abuse occurs in the area of products for individuals to use, which is precisely where it is most unacceptable.  Therefore, we have designed this version of the GPL to prohibit the practice for those products.  If such problems arise substantially in other domains, we stand ready to extend this provision to those domains in future versions of the GPL, as needed to protect the freedom of users.</p><p>Finally, every program is threatened constantly by software patents. States should not allow patents to restrict development and use of software on general-purpose computers, but in those that do, we wish to avoid the special danger that patents applied to a free program could make it effectively proprietary.  To prevent this, the GPL assures that patents cannot be used to render the program non-free.</p><p>The precise terms and conditions for copying, distribution and modification follow.</p><p style='text-align:center;'>TERMS AND CONDITIONS</p><p>0. Definitions.</p><p>"This License" refers to version 3 of the GNU General Public License.</p><p>"Copyright" also means copyright-like laws that apply to other kinds of works, such as semiconductor masks.</p><p>"The Program" refers to any copyrightable work licensed under this License.  Each licensee is addressed as "you".  "Licensees" and "recipients" may be individuals or organizations.</p><p>To "modify" a work means to copy from or adapt all or part of the work in a fashion requiring copyright permission, other than the making of an exact copy.  The resulting work is called a "modified version" of the earlier work or a work "based on" the earlier work.</p><p>A "covered work" means either the unmodified Program or a work based on the Program.</p><p>To "propagate" a work means to do anything with it that, without permission, would make you directly or secondarily liable for infringement under applicable copyright law, except executing it on a computer or modifying a private copy.  Propagation includes copying, distribution (with or without modification), making available to the public, and in some countries other activities as well.</p><p>To "convey" a work means any kind of propagation that enables other parties to make or receive copies.  Mere interaction with a user through a computer network, with no transfer of a copy, is not conveying.</p><p>An interactive user interface displays "Appropriate Legal Notices" to the extent that it includes a convenient and prominently visible feature that (1) displays an appropriate copyright notice, and (2) tells the user that there is no warranty for the work (except to the extent that warranties are provided), that licensees may convey the work under this License, and how to view a copy of this License.  If the interface presents a list of user commands or options, such as a menu, a prominent item in the list meets this criterion.</p><p>1. Source Code.</p><p>The "source code" for a work means the preferred form of the work for making modifications to it.  "Object code" means any non-source form of a work.</p><p>A "Standard Interface" means an interface that either is an official standard defined by a recognized standards body, or, in the case of interfaces specified for a particular programming language, one that is widely used among developers working in that language.</p><p>The "System Libraries" of an executable work include anything, other than the work as a whole, that (a) is included in the normal form of packaging a Major Component, but which is not part of that Major Component, and (b) serves only to enable use of the work with that Major Component, or to implement a Standard Interface for which an implementation is available to the public in source code form.  A "Major Component", in this context, means a major essential component (kernel, window system, and so on) of the specific operating system (if any) on which the executable work runs, or a compiler used to produce the work, or an object code interpreter used to run it.</p><p>The "Corresponding Source" for a work in object code form means all the source code needed to generate, install, and (for an executable work) run the object code and to modify the work, including scripts to control those activities.  However, it does not include the work's System Libraries, or general-purpose tools or generally available free programs which are used unmodified in performing those activities but which are not part of the work.  For example, Corresponding Source includes interface definition files associated with source files for the work, and the source code for shared libraries and dynamically linked subprograms that the work is specifically designed to require, such as by intimate data communication or control flow between those subprograms and other parts of the work.</p><p>The Corresponding Source need not include anything that users can regenerate automatically from other parts of the Corresponding Source.</p><p>The Corresponding Source for a work in source code form is that same work.</p><p>2. Basic Permissions.</p><p>All rights granted under this License are granted for the term of copyright on the Program, and are irrevocable provided the stated conditions are met.  This License explicitly affirms your unlimited permission to run the unmodified Program.  The output from running a covered work is covered by this License only if the output, given its content, constitutes a covered work.  This License acknowledges your rights of fair use or other equivalent, as provided by copyright law.</p><p>You may make, run and propagate covered works that you do not convey, without conditions so long as your license otherwise remains in force.  You may convey covered works to others for the sole purpose of having them make modifications exclusively for you, or provide you with facilities for running those works, provided that you comply with the terms of this License in conveying all material for which you do not control copyright.  Those thus making or running the covered works for you must do so exclusively on your behalf, under your direction and control, on terms that prohibit them from making any copies of your copyrighted material outside their relationship with you.</p><p>Conveying under any other circumstances is permitted solely under the conditions stated below.  Sublicensing is not allowed; section 10 makes it unnecessary.</p><p>3. Protecting Users' Legal Rights From Anti-Circumvention Law.</p><p>No covered work shall be deemed part of an effective technological measure under any applicable law fulfilling obligations under article 11 of the WIPO copyright treaty adopted on 20 December 1996, or similar laws prohibiting or restricting circumvention of such measures.</p><p>When you convey a covered work, you waive any legal power to forbid circumvention of technological measures to the extent such circumvention is effected by exercising rights under this License with respect to the covered work, and you disclaim any intention to limit operation or modification of the work as a means of enforcing, against the work's users, your or third parties' legal rights to forbid circumvention of technological measures.</p><p>4. Conveying Verbatim Copies.</p><p>You may convey verbatim copies of the Program's source code as you receive it, in any medium, provided that you conspicuously and appropriately publish on each copy an appropriate copyright notice; keep intact all notices stating that this License and any non-permissive terms added in accord with section 7 apply to the code; keep intact all notices of the absence of any warranty; and give all recipients a copy of this License along with the Program.</p><p>You may charge any price or no price for each copy that you convey, and you may offer support or warranty protection for a fee.</p><p>5. Conveying Modified Source Versions.</p></p>You may convey a work based on the Program, or the modifications to produce it from the Program, in the form of source code under the terms of section 4, provided that you also meet all of these conditions:</p><p style='margin-left:20px;'>a) The work must carry prominent notices stating that you modified it, and giving a relevant date.</p><p style='margin-left:20px;'>b) The work must carry prominent notices stating that it is released under this License and any conditions added under section 7.  This requirement modifies the requirement in section 4 to "keep intact all notices".</p><p style='margin-left:20px;'>c) You must license the entire work, as a whole, under this License to anyone who comes into possession of a copy.  This License will therefore apply, along with any applicable section 7 additional terms, to the whole of the work, and all its parts, regardless of how they are packaged.  This License gives no permission to license the work in any other way, but it does not invalidate such permission if you have separately received it.</p><p style='margin-left:20px;'>d) If the work has interactive user interfaces, each must display Appropriate Legal Notices; however, if the Program has interactive interfaces that do not display Appropriate Legal Notices, your work need not make them do so.</p><p>A compilation of a covered work with other separate and independent works, which are not by their nature extensions of the covered work, and which are not combined with it such as to form a larger program, in or on a volume of a storage or distribution medium, is called an "aggregate" if the compilation and its resulting copyright are not used to limit the access or legal rights of the compilation's users beyond what the individual works permit.  Inclusion of a covered work in an aggregate does not cause this License to apply to the other parts of the aggregate.</p><p>6. Conveying Non-Source Forms.</p><p>You may convey a covered work in object code form under the terms of sections 4 and 5, provided that you also convey the machine-readable Corresponding Source under the terms of this License, in one of these ways:</p><p style='margin-left:20px;'>a) Convey the object code in, or embodied in, a physical product (including a physical distribution medium), accompanied by the Corresponding Source fixed on a durable physical medium customarily used for software interchange.</p><p style='margin-left:20px;'>b) Convey the object code in, or embodied in, a physical product (including a physical distribution medium), accompanied by a written offer, valid for at least three years and valid for as long as you offer spare parts or customer support for that product model, to give anyone who possesses the object code either (1) a copy of the Corresponding Source for all the software in the product that is covered by this License, on a durable physical medium customarily used for software interchange, for a price no more than your reasonable cost of physically performing this conveying of source, or (2) access to copy the Corresponding Source from a network server at no charge.</p><p style='margin-left:20px;'>c) Convey individual copies of the object code with a copy of the written offer to provide the Corresponding Source.  This alternative is allowed only occasionally and noncommercially, and only if you received the object code with such an offer, in accord with subsection 6b.</p><p style='margin-left:20px;'>d) Convey the object code by offering access from a designated place (gratis or for a charge), and offer equivalent access to the Corresponding Source in the same way through the same place at no further charge.  You need not require recipients to copy the Corresponding Source along with the object code.  If the place to copy the object code is a network server, the Corresponding Source may be on a different server (operated by you or a third party) that supports equivalent copying facilities, provided you maintain clear directions next to the object code saying where to find the Corresponding Source.  Regardless of what server hosts the Corresponding Source, you remain obligated to ensure that it is available for as long as needed to satisfy these requirements.</p><p style='margin-left:20px;'>e) Convey the object code using peer-to-peer transmission, provided you inform other peers where the object code and Corresponding Source of the work are being offered to the general public at no charge under subsection 6d.</p><p>A separable portion of the object code, whose source code is excluded from the Corresponding Source as a System Library, need not be included in conveying the object code work.</p><p>A "User Product" is either (1) a "consumer product", which means any tangible personal property which is normally used for personal, family, or household purposes, or (2) anything designed or sold for incorporation into a dwelling.  In determining whether a product is a consumer product, doubtful cases shall be resolved in favor of coverage.  For a particular product received by a particular user, "normally used" refers to a typical or common use of that class of product, regardless of the status of the particular user or of the way in which the particular user actually uses, or expects or is expected to use, the product.  A product is a consumer product regardless of whether the product has substantial commercial, industrial or non-consumer uses, unless such uses represent the only significant mode of use of the product.</p><p>"Installation Information" for a User Product means any methods, procedures, authorization keys, or other information required to install and execute modified versions of a covered work in that User Product from a modified version of its Corresponding Source.  The information must suffice to ensure that the continued functioning of the modified object code is in no case prevented or interfered with solely because modification has been made.</p><p>If you convey an object code work under this section in, or with, or specifically for use in, a User Product, and the conveying occurs as part of a transaction in which the right of possession and use of the User Product is transferred to the recipient in perpetuity or for a fixed term (regardless of how the transaction is characterized), the Corresponding Source conveyed under this section must be accompanied by the Installation Information.  But this requirement does not apply if neither you nor any third party retains the ability to install modified object code on the User Product (for example, the work has been installed in ROM).</p><p>The requirement to provide Installation Information does not include a requirement to continue to provide support service, warranty, or updates for a work that has been modified or installed by the recipient, or for the User Product in which it has been modified or installed.  Access to a network may be denied when the modification itself materially and adversely affects the operation of the network or violates the rules and protocols for communication across the network.</p><p>Corresponding Source conveyed, and Installation Information provided, in accord with this section must be in a format that is publicly documented (and with an implementation available to the public in source code form), and must require no special password or key for unpacking, reading or copying.</p><p>7. Additional Terms.</p><p>"Additional permissions" are terms that supplement the terms of this License by making exceptions from one or more of its conditions. Additional permissions that are applicable to the entire Program shall be treated as though they were included in this License, to the extent that they are valid under applicable law.  If additional permissions apply only to part of the Program, that part may be used separately under those permissions, but the entire Program remains governed by this License without regard to the additional permissions.</p><p>When you convey a copy of a covered work, you may at your option remove any additional permissions from that copy, or from any part of it.  (Additional permissions may be written to require their own removal in certain cases when you modify the work.)  You may place additional permissions on material, added by you to a covered work, for which you have or can give appropriate copyright permission.</p><p>Notwithstanding any other provision of this License, for material you add to a covered work, you may (if authorized by the copyright holders of that material) supplement the terms of this License with terms:</p><p style='margin-left:20px;'>a) Disclaiming warranty or limiting liability differently from the terms of sections 15 and 16 of this License; or</p><p style='margin-left:20px;'>b) Requiring preservation of specified reasonable legal notices or author attributions in that material or in the Appropriate Legal Notices displayed by works containing it; or</p><p style='margin-left:20px;'>c) Prohibiting misrepresentation of the origin of that material, or requiring that modified versions of such material be marked in reasonable ways as different from the original version; or</p><p style='margin-left:20px;'>d) Limiting the use for publicity purposes of names of licensors or authors of the material; or</p><p style='margin-left:20px;'>e) Declining to grant rights under trademark law for use of some trade names, trademarks, or service marks; or</p><p style='margin-left:20px;'>f) Requiring indemnification of licensors and authors of that material by anyone who conveys the material (or modified versions of it) with contractual assumptions of liability to the recipient, for any liability that these contractual assumptions directly impose on those licensors and authors.</p><p>All other non-permissive additional terms are considered "further restrictions" within the meaning of section 10.  If the Program as you received it, or any part of it, contains a notice stating that it is governed by this License along with a term that is a further restriction, you may remove that term.  If a license document contains a further restriction but permits relicensing or conveying under this License, you may add to a covered work material governed by the terms of that license document, provided that the further restriction does not survive such relicensing or conveying.</p><p>If you add terms to a covered work in accord with this section, you must place, in the relevant source files, a statement of the additional terms that apply to those files, or a notice indicating where to find the applicable terms.</p><p>Additional terms, permissive or non-permissive, may be stated in the form of a separately written license, or stated as exceptions; the above requirements apply either way.</p><p>8. Termination.</p><p>You may not propagate or modify a covered work except as expressly provided under this License.  Any attempt otherwise to propagate or modify it is void, and will automatically terminate your rights under this License (including any patent licenses granted under the third paragraph of section 11).</p><p>However, if you cease all violation of this License, then your license from a particular copyright holder is reinstated (a) provisionally, unless and until the copyright holder explicitly and finally terminates your license, and (b) permanently, if the copyright holder fails to notify you of the violation by some reasonable means prior to 60 days after the cessation.</p><p>Moreover, your license from a particular copyright holder is reinstated permanently if the copyright holder notifies you of the violation by some reasonable means, this is the first time you have received notice of violation of this License (for any work) from that copyright holder, and you cure the violation prior to 30 days after your receipt of the notice.</p><p>Termination of your rights under this section does not terminate the licenses of parties who have received copies or rights from you under this License.  If your rights have been terminated and not permanently reinstated, you do not qualify to receive new licenses for the same material under section 10.</p><p>9. Acceptance Not Required for Having Copies.</p><p>You are not required to accept this License in order to receive or run a copy of the Program.  Ancillary propagation of a covered work occurring solely as a consequence of using peer-to-peer transmission to receive a copy likewise does not require acceptance.  However, nothing other than this License grants you permission to propagate or modify any covered work.  These actions infringe copyright if you do not accept this License.  Therefore, by modifying or propagating a covered work, you indicate your acceptance of this License to do so.</p><p>10. Automatic Licensing of Downstream Recipients.</p><p>Each time you convey a covered work, the recipient automatically receives a license from the original licensors, to run, modify and propagate that work, subject to this License.  You are not responsible for enforcing compliance by third parties with this License.</p><p>An "entity transaction" is a transaction transferring control of an organization, or substantially all assets of one, or subdividing an organization, or merging organizations.  If propagation of a covered work results from an entity transaction, each party to that transaction who receives a copy of the work also receives whatever licenses to the work the party's predecessor in interest had or could give under the previous paragraph, plus a right to possession of the Corresponding Source of the work from the predecessor in interest, if the predecessor has it or can get it with reasonable efforts.</p><p>You may not impose any further restrictions on the exercise of the rights granted or affirmed under this License.  For example, you may not impose a license fee, royalty, or other charge for exercise of rights granted under this License, and you may not initiate litigation (including a cross-claim or counterclaim in a lawsuit) alleging that any patent claim is infringed by making, using, selling, offering for sale, or importing the Program or any portion of it.</p><p>11. Patents.</p><p>A "contributor" is a copyright holder who authorizes use under this License of the Program or a work on which the Program is based.  The work thus licensed is called the contributor's "contributor version".</p><p>A contributor's "essential patent claims" are all patent claims owned or controlled by the contributor, whether already acquired or hereafter acquired, that would be infringed by some manner, permitted by this License, of making, using, or selling its contributor version, but do not include claims that would be infringed only as a consequence of further modification of the contributor version.  For purposes of this definition, "control" includes the right to grant patent sublicenses in a manner consistent with the requirements of this License.</p><p>Each contributor grants you a non-exclusive, worldwide, royalty-free patent license under the contributor's essential patent claims, to make, use, sell, offer for sale, import and otherwise run, modify and propagate the contents of its contributor version.</p><p>In the following three paragraphs, a "patent license" is any express agreement or commitment, however denominated, not to enforce a patent (such as an express permission to practice a patent or covenant not to sue for patent infringement).  To "grant" such a patent license to a party means to make such an agreement or commitment not to enforce a patent against the party.</p><p>If you convey a covered work, knowingly relying on a patent license, and the Corresponding Source of the work is not available for anyone to copy, free of charge and under the terms of this License, through a publicly available network server or other readily accessible means, then you must either (1) cause the Corresponding Source to be so available, or (2) arrange to deprive yourself of the benefit of the patent license for this particular work, or (3) arrange, in a manner consistent with the requirements of this License, to extend the patent license to downstream recipients.  "Knowingly relying" means you have actual knowledge that, but for the patent license, your conveying the covered work in a country, or your recipient's use of the covered work in a country, would infringe one or more identifiable patents in that country that you have reason to believe are valid.</p><p>If, pursuant to or in connection with a single transaction or arrangement, you convey, or propagate by procuring conveyance of, a covered work, and grant a patent license to some of the parties receiving the covered work authorizing them to use, propagate, modify or convey a specific copy of the covered work, then the patent license you grant is automatically extended to all recipients of the covered work and works based on it.</p><p>A patent license is "discriminatory" if it does not include within the scope of its coverage, prohibits the exercise of, or is conditioned on the non-exercise of one or more of the rights that are specifically granted under this License.  You may not convey a covered work if you are a party to an arrangement with a third party that is in the business of distributing software, under which you make payment to the third party based on the extent of your activity of conveying the work, and under which the third party grants, to any of the parties who would receive the covered work from you, a discriminatory patent license (a) in connection with copies of the covered work conveyed by you (or copies made from those copies), or (b) primarily for and in connection with specific products or compilations that contain the covered work, unless you entered into that arrangement, or that patent license was granted, prior to 28 March 2007.</p><p>Nothing in this License shall be construed as excluding or limiting any implied license or other defenses to infringement that may otherwise be available to you under applicable patent law.</p><p>12. No Surrender of Others' Freedom.</p><p>If conditions are imposed on you (whether by court order, agreement or otherwise) that contradict the conditions of this License, they do not excuse you from the conditions of this License.  If you cannot convey a covered work so as to satisfy simultaneously your obligations under this License and any other pertinent obligations, then as a consequence you may not convey it at all.  For example, if you agree to terms that obligate you to collect a royalty for further conveying from those to whom you convey the Program, the only way you could satisfy both those terms and this License would be to refrain entirely from conveying the Program.</p><p>13. Use with the GNU Affero General Public License.</p><p>Notwithstanding any other provision of this License, you have permission to link or combine any covered work with a work licensed under version 3 of the GNU Affero General Public License into a single combined work, and to convey the resulting work.  The terms of this License will continue to apply to the part which is the covered work, but the special requirements of the GNU Affero General Public License, section 13, concerning interaction through a network will apply to the combination as such.</p><p>14. Revised Versions of this License.</p><p>The Free Software Foundation may publish revised and/or new versions of the GNU General Public License from time to time.  Such new versions will be similar in spirit to the present version, but may differ in detail to address new problems or concerns.</p><p>Each version is given a distinguishing version number.  If the Program specifies that a certain numbered version of the GNU General Public License "or any later version" applies to it, you have the option of following the terms and conditions either of that numbered version or of any later version published by the Free Software Foundation.  If the Program does not specify a version number of the GNU General Public License, you may choose any version ever published by the Free Software Foundation.</p><p>If the Program specifies that a proxy can decide which future versions of the GNU General Public License can be used, that proxy's public statement of acceptance of a version permanently authorizes you to choose that version for the Program.</p><p>Later license versions may give you additional or different permissions.  However, no additional obligations are imposed on any author or copyright holder as a result of your choosing to follow a later version.</p><p>15. Disclaimer of Warranty.</p><p>THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.</p><p>16. Limitation of Liability.</p><p>IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS), EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.</p><p>17. Interpretation of Sections 15 and 16.</p><p>If the disclaimer of warranty and limitation of liability provided above cannot be given local legal effect according to their terms, reviewing courts shall apply local law that most closely approximates an absolute waiver of all civil liability in connection with the Program, unless a warranty or assumption of liability accompanies a copy of the Program in return for a fee.</p><p style='text-align:center;'>END OF TERMS AND CONDITIONS</p><p style='text-align:center;'>How to Apply These Terms to Your New Programs</p><p>If you develop a new program, and you want it to be of the greatest possible use to the public, the best way to achieve this is to make it free software which everyone can redistribute and change under these terms.</p><p>To do so, attach the following notices to the program.  It is safest to attach them to the start of each source file to most effectively state the exclusion of warranty; and each file should have at least the "copyright" line and a pointer to where the full notice is found.</p><p style='margin-left:20px;'>&lt;one line to give the program's name and a brief idea of what it does.&gt;<br>Copyright (C) &lt;year&gt;  &lt;name of author&gt;</p><p style='margin-left:20px;'>This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.</p><p style='margin-left:20px;'>This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.</p><p style='margin-left:20px;'>You should have received a copy of the GNU General Public License along with this program.  If not, see &lt;http://www.gnu.org/licenses/&gt;.</p><p>Also add information on how to contact you by electronic and paper mail.</p><p>If the program does terminal interaction, make it output a short notice like this when it starts in an interactive mode:</p><p style='margin-left:20px;'>&lt;program&gt;  Copyright (C) &lt;year&gt;  &lt;name of author&gt;<br>This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'. This is free software, and you are welcome to redistribute it under certain conditions; type `show c' for details.</p><p>The hypothetical commands `show w' and `show c' should show the appropriate parts of the General Public License.  Of course, your program's commands might be different; for a GUI interface, you would use an "about box".</p><p>You should also get your employer (if you work as a programmer) or school, if any, to sign a "copyright disclaimer" for the program, if necessary. For more information on this, and how to apply and follow the GNU GPL, see &lt;http://www.gnu.org/licenses/&gt;.</p><p>The GNU General Public License does not permit incorporating your program into proprietary programs.  If your program is a subroutine library, you may consider it more useful to permit linking proprietary applications with the library.  If this is what you want to do, use the GNU Lesser General Public License instead of this License.  But first, please read &lt;http://www.gnu.org/philosophy/why-not-lgpl.html&gt;.</p>""")

        self.tabwidget.addTab(self.about, _("About"))
        self.tabwidget.addTab(self.credits, _("Credits"))
        self.tabwidget.addTab(self.license, _("License"))
        self.layout.addWidget(self.tabwidget)
        self.layout.addWidget(self.button)
        self.layout.setAlignment(self.button, Qt.AlignRight)
        self.setLayout(self.layout)

    def accept(self):
        self.done(1)


class CheckForUpdatesMessageBox(QMessageBox):

    def __init__(self, parent):
        super(CheckForUpdatesMessageBox, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.addButton(_("OK"), QMessageBox.AcceptRole)
        try:
            r = requests.get("https://mpvqc.rekt.cc/download/latest.txt", timeout=5)
            if v.split(" ")[-1] != r.text.split("\n")[0].strip():
                self.setText(
                        _("There is a new version of {} available ({}).<br>"
                        "Visit <a href='https://mpvqc.rekt.cc/'>"
                        "https://mpvqc.rekt.cc/</a> to download it.")
                        .format(v.split(" ")[0], r.text.strip())
                        )
            else:
                self.setText(
                            _("You are already using the most "
                            "recent version of {}. {}").format(v.split(" ")[0], "👌")
                            )
        except requests.exceptions.ConnectionError:
            self.setText(_("A connection to the server could not be established."))
        except requests.exceptions.Timeout:
            self.setText(_("The server did not respond quickly enough."))


class WarningMessageBox(QMessageBox):

    def __init__(self, parent, title, message, question=False):
        super(WarningMessageBox, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setIcon(QMessageBox.Warning)
        self.setWindowTitle(title)
        self.setText(message)
        if question:
            self.addButton(_("Yes"), QMessageBox.YesRole)
            self.addButton(_("No"), QMessageBox.NoRole)
        else:
            self.addButton(_("OK"), QMessageBox.AcceptRole)


class InformationMessageBox(QMessageBox):

    def __init__(self, parent, title, message):
        super(InformationMessageBox, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setIcon(QMessageBox.Information)
        self.setWindowTitle(title)
        self.setText(message)
        self.addButton(_("OK"), QMessageBox.AcceptRole)


class QuestionMessageBox(QMessageBox):

    def __init__(self, parent, title, message):
        super(QuestionMessageBox, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setIcon(QMessageBox.Question)
        self.setWindowTitle(title)
        self.setText(message)
        self.addButton(_("Yes"), QMessageBox.YesRole)
        self.addButton(_("No"), QMessageBox.NoRole)


class TimestampDialog(QDialog):

    def __init__(self, parent, index):
        super(TimestampDialog, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setWindowFlags(self.windowFlags()&~Qt.WindowContextHelpButtonHint)
        self.index = index
        self.timestampdialoglayout = QVBoxLayout()
        self.groupboxlayout = QHBoxLayout()
        self.layout_h = QHBoxLayout()
        self.layout_h.setContentsMargins(1, 1, 1, 1)
        self.layout_m = QHBoxLayout()
        self.layout_m.setContentsMargins(1, 1, 1, 1)
        self.layout_s = QHBoxLayout()
        self.layout_s.setContentsMargins(1, 1, 1, 1)
        self.groupbox_h = QGroupBox(_("Hours"), self)
        self.groupbox_m = QGroupBox(_("Minutes"), self)
        self.groupbox_s = QGroupBox(_("Seconds"), self)
        self.spinbox_h = QSpinBox(self)
        self.spinbox_h.setMinimum(0)
        self.spinbox_h.setMaximum(99)
        self.spinbox_m = QSpinBox(self)
        self.spinbox_m.setMinimum(0)
        self.spinbox_m.setMaximum(59)
        self.spinbox_s = QSpinBox(self)
        self.spinbox_s.setMinimum(0)
        self.spinbox_s.setMaximum(59)
        self.layout_h.addWidget(self.spinbox_h)
        self.layout_m.addWidget(self.spinbox_m)
        self.layout_s.addWidget(self.spinbox_s)
        self.groupbox_h.setLayout(self.layout_h)
        self.groupbox_m.setLayout(self.layout_m)
        self.groupbox_s.setLayout(self.layout_s)
        self.groupboxlayout.addWidget(self.groupbox_h)
        self.groupboxlayout.addWidget(self.groupbox_m)
        self.groupboxlayout.addWidget(self.groupbox_s)
        self.acceptbutton = QPushButton(_("OK"), self)
        self.acceptbutton.clicked.connect(self.clickedAcceptButton)
        self.timestampdialoglayout.addLayout(self.groupboxlayout)
        self.timestampdialoglayout.addWidget(self.acceptbutton)
        self.timestampdialoglayout.setAlignment(self.groupboxlayout, Qt.AlignHCenter)
        self.timestampdialoglayout.setAlignment(self.acceptbutton, Qt.AlignHCenter)
        self.setLayout(self.timestampdialoglayout)
        timestamp = commentmodel.item(commentlistview.selectedIndexes()[0].row(), 0).text()
        str_h, str_m, str_s = timestamp.split(":")
        self.spinbox_h.setValue(int(str_h))
        self.spinbox_m.setValue(int(str_m))
        self.spinbox_s.setValue(int(str_s))

    def clickedAcceptButton(self):
        h = self.spinbox_h.value()
        m = self.spinbox_m.value()
        s = self.spinbox_s.value()
        commentmodel.item(
                        self.index.row(),
                        self.index.column(),
                        ).setText(standardizeTimestamp(":".join([str(h), str(m), str(s)])))
        sortCommentListView(self.index.row())
        resizeCommentListViewToContents()
        self.done(1)


class CommentTypeDialog(QDialog):

    def __init__(self, parent, index):
        super(CommentTypeDialog, self).__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self.setWindowFlags(self.windowFlags()&~Qt.WindowContextHelpButtonHint)
        self.index = index
        self.commenttypedialoglayout = QVBoxLayout()
        self.commenttypedialoglayout.setContentsMargins(0, 0, 0, 0)
        self.commenttypebuttons = []
        for x in commenttypeoptions:
            self.button = QPushButton(x, self)
            self.button.setFlat(True)
            self.commenttypebuttons.append(self.button)
        for i in range(len(self.commenttypebuttons)):
            self.commenttypebuttons[i].clicked.connect(partial(self.clickedDialogButton, i))
        for x in self.commenttypebuttons:
            self.commenttypedialoglayout.addWidget(x)
        self.setLayout(self.commenttypedialoglayout)

    def clickedDialogButton(self, value):
        commentmodel.item(self.index.row(), self.index.column()).setText(commenttypeoptions[value])
        resizeCommentListViewToContents()
        self.done(1)


class CommentTextEdit(QTextEdit):

    def __init__(self, parent=None):
        super(CommentTextEdit, self).__init__(parent)
        self.document().contentsChanged.connect(self.sizeChange)
        self.setAcceptRichText(False)
        self.updatedgeometry = False

    def sizeChange(self):
        newheight = self.document().size().height()+2
        self.resize(self.width(), newheight)
        # Do not resize smaller than the initial size
        if newheight >= self.minimumHeight()-2 and self.updatedgeometry:
            commentlistview.setRowHeight(commentlistview.selectionModel().selectedRows()[0].row(), newheight-2)
        if (self.updatedgeometry
                and not commentmodel.rowCount()-1 == commentlistview.selectionModel().selectedRows()[0].row()):
            commentlistview.scrollTo(
                        commentmodel.item(
                                commentlistview.selectionModel().selectedRows()[0].row(),
                                2,
                                ).index()
                        )
        elif (self.updatedgeometry
                and not commentmodel.rowCount()-1 == 0
                and commentmodel.rowCount()-1 == commentlistview.selectionModel().selectedRows()[0].row()):
            commentlistview.scrollTo(
                        commentmodel.item(
                                commentlistview.selectionModel().selectedRows()[0].row()-1,
                                2,
                                ).index(),
                        QAbstractItemView.PositionAtBottom,
                        )
            commentlistview.scrollTo(
                        commentmodel.item(
                                commentlistview.selectionModel().selectedRows()[0].row(),
                                2,
                                ).index()
                        )

    def showEvent(self, event):
        """ Needed, because during creation document().size() seems to be unreliable """
        self.sizeChange()
        event.ignore()

    def mousePressEvent(self, event):
        """ Disable stupid dragging feature """
        if event.button() == Qt.LeftButton:
            newcursor = self.cursorForPosition(event.pos())
            self.setTextCursor(newcursor)
            event.accept()
        super(CommentTextEdit, self).mousePressEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            commentlistview.delegate.commitData.emit(self)
            commentlistview.delegate.closeEditor.emit(self)
            event.accept()
        else:
            super(CommentTextEdit, self).keyPressEvent(event)


class CommentListViewDelegate(QStyledItemDelegate):

    def createEditor(self, parent, option, index):
        data = index.model().itemFromIndex(index)
        if isinstance(data, QStandardItem):
            editor = CommentTextEdit(parent)
            editor.document().setDocumentMargin(0)
            editor.setStyleSheet("QTextEdit {padding-right:1;}")
            return editor
        else:
            return super(CommentListViewDelegate, self).createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        data = index.model().itemFromIndex(index)
        if isinstance(data, QStandardItem):
            text = index.model().data(index, Qt.EditRole)
            editor.setPlainText(text)
            editor.selectAll()
        else:
            super(CommentListViewDelegate, self).setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        data = index.model().itemFromIndex(index)
        if isinstance(data, QStandardItem):
            text = editor.toPlainText().strip()
            model.setData(index, text, Qt.EditRole)
            resizeCommentListViewToContents()
        else:
            super(CommentListViewDelegate, self).setModelData(editor, model, index)

    def updateEditorGeometry(self, editor, option, index):
        data = index.model().itemFromIndex(index)
        if isinstance(data, QStandardItem):
            editor.setGeometry(option.rect.x()+3-1, option.rect.y()-1, option.rect.width()-3, option.rect.height()+2)
            editor.setMaximumWidth(option.rect.width()-3)
            editor.setMinimumHeight(option.rect.height()+2)
            # Dont resize CommentListView if the editor contains more than 1 line of text
            if editor.document().size().height()/QFontMetrics(editor.document().defaultFont()).lineSpacing() == 1:
                # Needed because sometimes after adding a new comment, already existing comments
                # that span over several lines get resized wrong vertically
                # Only needed at the beginning after inserting a new comment, that's why this is disabled
                # if the editor contains more than 1 line of text
                # Otherwise it would break resizing behaviour
                resizeCommentListViewToContents()
            editor.updatedgeometry = True
            commentlistview.scrollTo(
                        commentmodel.item(
                                commentlistview.selectionModel().selectedRows()[0].row(),
                                2,
                                ).index()
                        )
        else:
            super(CommentListViewDelegate, self).updateEditorGeometry(editor, option, index)


class CommentListView(QTableView):

    def __init__(self, parent=None):
        super(CommentListView, self).__init__(parent)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.delegate = CommentListViewDelegate()
        self.setItemDelegate(self.delegate)
        self.setShowGrid(False)
        self.verticalHeader().hide()
        self.horizontalHeader().hide()
        self.setAlternatingRowColors(True)
        self.setWordWrap(True)
        self.pressed.connect(clickedOnCommentListView)
        self.doubleClicked.connect(doubleClickedOnCommentListView)
        self.horizontalHeader().setStretchLastSection(True)
        self.setEditTriggers(QAbstractItemView.DoubleClicked)
        # Remember the scroll position, because to go to fullscreen,
        # this Widget has to be hidden which loses the scroll position,
        # it has to be set again manually after leaving fullscreen
        self.scrollposition = 0

    def keyPressEvent(self, event):
        pressedkey = event.key()
        if ((pressedkey == Qt.Key_Up or pressedkey == Qt.Key_Down)
                and int(app.keyboardModifiers()) == Qt.NoModifier):
            super(CommentListView, self).keyPressEvent(event)
        elif pressedkey == Qt.Key_Delete:
            deleteSelection()
            event.accept()
        elif pressedkey == Qt.Key_Enter or pressedkey == Qt.Key_Return:
            editSelection()
            event.accept()
        elif pressedkey == Qt.Key_C and int(app.keyboardModifiers()) == Qt.CTRL:
            copySelection()
            event.accept()
        else:
            event.ignore()

    def mousePressEvent(self, event):
        """ Ignore some mouse buttons to get them forwarded to mpv """
        pressedbutton = event.button()
        if pressedbutton == Qt.MiddleButton:
            event.ignore()
        elif pressedbutton == Qt.BackButton:
            event.ignore()
        elif pressedbutton == Qt.ForwardButton:
            event.ignore()
        else:
            super(CommentListView, self).mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        """ Ignore some mouse buttons to get them forwarded to mpv """
        pressedbutton = event.button()
        if pressedbutton == Qt.MiddleButton:
            event.ignore()
        elif pressedbutton == Qt.BackButton:
            event.ignore()
        elif pressedbutton == Qt.ForwardButton:
            event.ignore()
        else:
            super(CommentListView, self).mouseDoubleClickEvent(event)


class InvalidTimestampError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidCommentLineError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def checkMpvConf():
    mpvconf = path.join(programlocation, "mpv.conf")
    inputconf = path.join(programlocation, "input.conf")
    if not path.isfile(mpvconf):
        with open(mpvconf, "w", encoding="utf-8") as configfile:
            configfile.write(
"""#########
# Video #
#########

# Slightly modified HQ preset, uses Spline36 for scaling
# Debanding is disabled beacause we don't want to alter the video while doing quality control
vo=opengl-hq:deband=no

# Potentially higher quality video output, might be too demanding for old or low end hardware
#vo=opengl-hq:deband=no:scale=ewa_lanczossharp:cscale=ewa_lanczossoft:dscale=lanczos:scale-antiring=0.7:cscale-antiring=0.7:dscale-antiring=0.7:scaler-resizes-only

# Low quality settings, should work on almost every system (Only use this if you have to!)
#vo=opengl


#############
# Subtitles #
#############

# This makes sure that the current subtitle line is loaded after seeking
demuxer-mkv-subtitle-preroll


###########
# OSC/OSD #
###########

# Very slim On Screen Controller that consists of only a seekbar
script-opts=osc-minmousemove=1,osc-hidetimeout=200,osc-layout=slimbox

# Same as the previous one except it is positioned at the top
# (Use this if you don't want the OSC to occasionally cover the subtitles)
#script-opts=osc-minmousemove=1,osc-hidetimeout=200,osc-layout=slimbox,osc-valign=-0.8

# Bigger On Screen Controller with many buttons
#script-opts=osc-minmousemove=1,osc-hidetimeout=200,osc-layout=box

# Same as the previous one except it is positioned at the top
# (Use this if you don't want the OSC to occasionally cover the subtitles)
#script-opts=osc-minmousemove=1,osc-hidetimeout=200,osc-layout=box,osc-valign=-0.8


###############
# Screenshots #
###############

screenshot-format=png
screenshot-high-bit-depth=no
screenshot-directory=./Screenshots
""")
    if not path.isfile(inputconf):
        with open(inputconf, "w", encoding="utf-8") as configfile:
            configfile.write(
"""############################################
# The following keys are reserved by mpvQC #
# Changing them here will have no effect   #
############################################

e ignore
f ignore
UP ignore
DOWN ignore
ctrl+s ignore
ctrl+S ignore
ctrl+n ignore
ctrl+o ignore
ctrl+q ignore
ctrl+O ignore
ctrl+r ignore
MOUSE_BTN2 ignore    # Right mouse click

##################################################
# The following keys can be bound to anything    #
# This is not a comprehensive list of all keys   #
# There are many more, like a, A, @, ö, é, î ... #
# Please never bind 'quit' to any key!           #
##################################################

SPACE cycle pause
LEFT no-osd seek -2 relative+exact
RIGHT no-osd seek 2 relative+exact
shift+LEFT osd-bar seek -5 relative+keyframes
shift+RIGHT osd-bar seek 5 relative+keyframes
ctrl+LEFT no-osd sub-seek -1
ctrl+RIGHT no-osd sub-seek 1

MOUSE_BTN0 cycle pause       # Left click on mouse
MOUSE_BTN3 add volume 2      # Mouse wheel up
MOUSE_BTN4 add volume -2     # Mouse wheel down
MOUSE_BTN5 add chapter -1    # Backward button on mouse
MOUSE_BTN6 add chapter 1     # Forward button on mouse

p cycle pause
. frame-step
, frame-back-step
9 add volume -2
0 add volume 2
m cycle mute
j cycle sub
J cycle sub down
SHARP cycle audio        # SHARP assigns the # key
l ab_loop
s screenshot subtitles
S screenshot window

# This burns in subtitles (i.e. always render them at video resolution)
b vf toggle sub

# This displays statistics of the currently played file
i show_text "${osd-ass-cc/0}{\\\\fs11}{\\\\fnSource Sans Pro}{\\\\bord1}{\\\\3c&H262626&}{\\\\alpha&H11}\\\\N{\\\\b1}File:{\\\\b0}\\\\h\\\\h${osd-ass-cc/1}${filename}${osd-ass-cc/0}\\\\N\\\\h\\\\h\\\\h\\\\h\\\\h{\\\\b1}${?media-title:Title:\\\\h\\\\h}{\\\\b0}${osd-ass-cc/1}${?media-title:${media-title}}${osd-ass-cc/0}${?chapter:\\\\N\\\\h\\\\h\\\\h\\\\h\\\\h}{\\\\b1}${?chapter:Chapter:\\\\h\\\\h}{\\\\b0}${osd-ass-cc/1}${?chapter:${chapter}}${osd-ass-cc/0}${?cache-used:\\\\N\\\\h\\\\h\\\\h\\\\h\\\\h}{\\\\b1}${?cache-used:Cache:\\\\h\\\\h}{\\\\b0}${?cache-used:${cache-used}\\\\h\\\\h+${demuxer-cache-duration} sec}\\\\N\\\\N{\\\\b1}Video:{\\\\b0}\\\\h\\\\h${video-codec}\\\\N\\\\h\\\\h\\\\h\\\\h\\\\h{\\\\b1}A-V:{\\\\b0}\\\\h\\\\h${avsync}\\\\N\\\\h\\\\h\\\\h\\\\h\\\\h{\\\\b1}Dropped:{\\\\b0}\\\\h\\\\h${drop-frame-count}\\\\h\\\\h\\\\h\\\\h\\\\h{\\\\b1}VO:{\\\\b0}\\\\h\\\\h${vo-drop-frame-count}\\\\N\\\\h\\\\h\\\\h\\\\h\\\\h{\\\\b1}FPS:{\\\\b0}\\\\h\\\\h${fps} (specified)\\\\h\\\\h${estimated-vf-fps} (estimated)\\\\N\\\\h\\\\h\\\\h\\\\h\\\\h{\\\\b1}Native Resolution:{\\\\b0}\\\\h\\\\h${video-params/w} x ${video-params/h}\\\\N\\\\h\\\\h\\\\h\\\\h\\\\h{\\\\b1}Window Scale:{\\\\b0}\\\\h\\\\h${window-scale}\\\\N\\\\h\\\\h\\\\h\\\\h\\\\h{\\\\b1}Aspect Ratio:{\\\\b0}\\\\h\\\\h${video-params/aspect}\\\\N\\\\h\\\\h\\\\h\\\\h\\\\h{\\\\b1}Pixel format:{\\\\b0}\\\\h\\\\h${video-params/pixelformat}\\\\N\\\\h\\\\h\\\\h\\\\h\\\\h{\\\\b1}Colormatrix:{\\\\b0}\\\\h\\\\h${video-params/colormatrix}\\\\N\\\\h\\\\h\\\\h\\\\h\\\\h{\\\\b1}Primaries:{\\\\b0}\\\\h\\\\h${video-params/primaries}\\\\N\\\\h\\\\h\\\\h\\\\h\\\\h{\\\\b1}Levels:{\\\\b0}\\\\h\\\\h${video-params/colorlevels}${?packet-video-bitrate:${!=packet-video-bitrate==0:\\\\N\\\\h\\\\h\\\\h\\\\h\\\\h}}{\\\\b1}${?packet-video-bitrate:${!=packet-video-bitrate==0:Bitrate:\\\\h\\\\h}}{\\\\b0}${?packet-video-bitrate:${!=packet-video-bitrate==0:${packet-video-bitrate} kbps}}\\\\N\\\\N{\\\\b1}Audio:{\\\\b0}\\\\h\\\\h${audio-codec}\\\\N\\\\h\\\\h\\\\h\\\\h\\\\h{\\\\b1}Sample Rate:{\\\\b0}\\\\h\\\\h${audio-params/samplerate}\\\\N\\\\h\\\\h\\\\h\\\\h\\\\h{\\\\b1}Channels:{\\\\b0}\\\\h\\\\h${audio-params/channel-count}${?packet-audio-bitrate:${!=packet-audio-bitrate==0:\\\\N\\\\h\\\\h\\\\h\\\\h\\\\h}}{\\\\b1}${?packet-audio-bitrate:${!=packet-audio-bitrate==0:Bitrate:\\\\h\\\\h}}{\\\\b0}${?packet-audio-bitrate:${!=packet-audio-bitrate==0:${packet-audio-bitrate} kbps}}" 3000
""")


def readOptionsFile():
    global qcauthor
    global commenttypeoptions
    global autosaveinterval
    global optionsfile
    global language
    if path.isfile(optionsfile):
        with open(optionsfile, "r", encoding="utf-8") as of:
            optionsfilecontents = of.readlines()
            for line in optionsfilecontents:
                if line.upper().startswith("AUTHOR"):
                    qcauthor = "=".join(line.split("=")[1:]).strip()
                if line.upper().startswith("TYPES"):
                    commenttypeoptions = "".join(
                                                line.strip()
                                                .split("=")[1:]
                                                ).strip(" ,").split(",")
                if line.upper().startswith("AUTOSAVEINTERVAL"):
                    try:
                        autosaveinterval = float(
                                            "=".join(line.split("=")[1:])
                                            .strip().replace(",", ".")
                                            )
                    except ValueError:
                        pass
                if line.upper().startswith("LANGUAGE"):
                    language = "=".join(line.split("=")[1:]).strip()
    else:
        with open(optionsfile, "w", encoding="utf-8") as of:
            of.write("")


def restoreDefaultConfiguration():
    if WarningMessageBox(
                mainwindow,
                _("Warning"),
                _("Do you really want to restore the default configuration? (Your changes will be lost.)"),
                question=True,
                ).exec_() != 0:
        return
    remove(optionsfile)
    remove(path.join(programlocation, "mpv.conf"))
    remove(path.join(programlocation, "input.conf"))
    readOptionsFile()
    checkMpvConf()
    InformationMessageBox(
                    mainwindow,
                    _("Information"),
                    _("The changes will only take effect after restarting the program."),
                    ).exec_()


def writeOptionToFile(option, value):
    global optionsfile
    readOptionsFile()
    with open(optionsfile, "r", encoding="utf-8") as of:
        optionsfilecontents = of.readlines()
    with open(optionsfile, "w", encoding="utf-8") as of:
        found = False
        previousline = ""
        for line in optionsfilecontents:
            if line.upper().startswith(option):
                found = True
                of.write("{}={}\n".format(option, value))
            else:
                of.write(line)
            previousline = line
        if not found:
            optionline = "{}={}\n".format(option, value)
            if not previousline.endswith("\n") and not previousline == "":
                optionline = "\n"+optionline
            of.write(optionline)


def setOption(option, value):
    global qcauthor
    global commenttypeoptions
    global autosaveinterval
    global optionsfile
    if option == "nickname":
        writeOptionToFile("AUTHOR", value)
        qcauthor = value
    if option == "commenttypes":
        writeOptionToFile("TYPES", ",".join(x.strip() for x in value.split(",") if x.strip()))
        commenttypeoptions.clear()
        commenttypeoptions.extend(x.strip() for x in value.split(",") if x.strip())
    if option == "autosaveinterval":
        try:
            value = float(value.replace(",", "."))
        except ValueError:
            return
        writeOptionToFile("AUTOSAVEINTERVAL", str(value))
        autosaveinterval = value
        if value > 0:
            autosavetimer.start(int(60000*value))
        else:
            autosavetimer.stop()
    if option == "language":
        writeOptionToFile("LANGUAGE", value)
        InformationMessageBox(
                        mainwindow,
                        _("Information"),
                        _("The changes will only take effect after restarting the program."),
                        ).exec_()


def openOptionsDialogNickname():
    OptionsDialog(
            mainwindow,
            _("Set nickname"),
            qcauthor,
            _("OK"),
            "nickname",
            ).exec_()


def openOptionsDialogCommentTypes():
    OptionsDialog(
            mainwindow,
            _("Set comment types (comma separated list)"),
            ",".join(commenttypeoptions),
            _("OK"),
            "commenttypes",
            ).exec_()


def openOptionsDialogAutosaveInterval():
    OptionsDialog(
            mainwindow,
            _("Set autosave interval in minutes (0 to deactivate)"),
            str(autosaveinterval),
            _("OK"),
            "autosaveinterval",
            ).exec_()


def openMpvConfOptionDialog():
    TextEditOptionDialog(mainwindow, "mpv.conf").exec_()


def openInputConfOptionDialog():
    TextEditOptionDialog(mainwindow, "input.conf").exec_()


def openAboutDialog():
    AboutDialog(mainwindow).exec_()


def checkForUpdates():
    CheckForUpdatesMessageBox(mainwindow).exec_()


def checkTimestamp(timestamp):
    splittedtimestamp = timestamp.split(":")
    if not len(splittedtimestamp) == 3:
        return False
    if len(splittedtimestamp[2]) > 2 or len(splittedtimestamp[1]) > 2:
        return False
    try:
        for x in splittedtimestamp:
            int(x)
    except (NameError, ValueError):
        return False
    if int(splittedtimestamp[2]) > 59 or int(splittedtimestamp[1]) > 59:
        return False
    return True


def standardizeTimestamp(timestamp):
    splittedtimestamp = timestamp.split(":")
    for i in range(len(splittedtimestamp)):
        while splittedtimestamp[i].startswith("0"):
            splittedtimestamp[i] = splittedtimestamp[i][1:]
    for i in range(len(splittedtimestamp)):
        while len(splittedtimestamp[i]) < 2:
            splittedtimestamp[i] = "0"+splittedtimestamp[i]
    return ":".join(splittedtimestamp)


def secondsToTimestamp(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    str_s = "0"+str(s) if len(str(s))==1 else str(s)
    str_m = "0"+str(m) if len(str(m))==1 else str(m)
    str_h = "0"+str(h) if len(str(h))==1 else str(h)
    return ":".join([str_h, str_m, str_s])


def timestampToSeconds(timestamp):
    str_h, str_m, str_s = timestamp.split(":")
    return int(str_s) + int(str_m)*60 + int(str_h)*60*60


def newComment(commenttype):
    currentvideofile = mp.get_property("path") if mpvslave else mp.path
    if currentvideofile:
        currentposition = int(mp.get_property("time-pos").split(".")[0]) if mpvslave else int(mp.time_pos)
    else:
        currentposition = 0
    newentry = (currentposition, commenttype, "")
    commentslist = getCommentListViewContents(seconds=True)
    commentslist.append(newentry)
    commentslist = sorted(commentslist, key=itemgetter(0))
    newindex = commentslist.index(newentry)
    writeCommentListViewContents(commentslist, seconds=True)
    newmodelindex = commentmodel.item(newindex, 2).index()
    commentlistview.scrollTo(newmodelindex)
    commentlistview.setCurrentIndex(newmodelindex)
    commentlistview.edit(newmodelindex)


def deleteSelection():
    if commentListViewIsEmpty():
        return
    commentmodel.removeRows(
                    commentlistview.selectionModel().selectedRows()[0].row(),
                    1,
                    )


def editSelection():
    if commentListViewIsEmpty():
        return
    commentlistview.edit(
                    commentmodel.item(
                            commentlistview.selectionModel().selectedRows()[0].row(),
                            2,
                            ).index()
                    )


def copySelection():
    if commentListViewIsEmpty():
        return
    selectedrow = commentlistview.selectionModel().selectedRows()[0].row()
    timestamp = commentmodel.item(selectedrow, 0).text()
    commenttype = commentmodel.item(selectedrow, 1).text()
    comment = commentmodel.item(selectedrow, 2).text()
    app.clipboard().setText("[{}] [{}] {}".format(timestamp, commenttype, comment))


def commentDataChanged():
    global currentstatesaved
    currentstatesaved = False


def clickedOnCommentListView(index):
    if (index.column() == 0
            and QApplication.mouseButtons() == Qt.LeftButton):
        try:
            timestamp = commentmodel.item(index.row(), 0).text()
            seconds = timestampToSeconds(timestamp)
            mp.command("seek", seconds, "absolute+exact")
        except SystemError:
            pass


def doubleClickedOnCommentListView(index):
    if (index.column() == 0
            and QApplication.mouseButtons() == Qt.LeftButton):
        TimestampDialog(mainwindow, index).exec_()
    if (index.column() == 1
            and QApplication.mouseButtons() == Qt.LeftButton):
        CommentTypeDialog(mainwindow, index).exec_()


def resizeCommentListViewToContents():
    commentlistview.resizeColumnToContents(0)
    commentlistview.resizeColumnToContents(1)
    commentlistview.resizeRowsToContents()


def commentListViewIsEmpty():
    currentsize = commentmodel.rowCount()
    if currentsize == 0:
        return True
    return False


def getCommentListViewContents(seconds=False):
    currentsize = commentmodel.rowCount()
    commentslist = []
    for i in range(currentsize):
        timedata = commentmodel.item(i, 0).text()
        if seconds:
            timedata = timestampToSeconds(timedata)
        commentslist.append((
                            timedata,
                            commentmodel.item(i, 1).text(),
                            commentmodel.item(i, 2).text(),
                            ))
    return commentslist


def writeCommentListViewContents(comments, seconds=False):
    commentmodel.clear()
    for comment in comments:
        if not seconds:
            timestamp = QStandardItem(comment[0])
        else:
            timestamp = QStandardItem(secondsToTimestamp(comment[0]))
        timestamp.setEditable(False)
        timestamp.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
        commenttype = QStandardItem(comment[1])
        commenttype.setEditable(False)
        commenttype.setTextAlignment(Qt.AlignCenter)
        commentmodel.appendRow([timestamp, commenttype, QStandardItem(comment[2])])
    resizeCommentListViewToContents()


def sortCommentListView(index=None):
    comments = getCommentListViewContents(seconds=True)
    sortedcomments = sorted(comments, key=itemgetter(0))
    index = sortedcomments.index(comments[index if index else 0])
    writeCommentListViewContents(sortedcomments, seconds=True)
    currentmodelindex = commentmodel.item(index, 2).index()
    commentlistview.setCurrentIndex(currentmodelindex)
    commentlistview.scrollTo(
                        commentmodel.item(
                                commentlistview.selectionModel().selectedRows()[0].row(),
                                2,
                                ).index()
                        )


def newQcFile():
    global currentqcfile
    global currentstatesaved
    exitFullscreen()
    if not currentstatesaved and WarningMessageBox(
                            mainwindow,
                            _("Warning"),
                            _("Do you really want to create a new QC document without saving the old one?"),
                            question=True,
                            ).exec_() != 0:
        return
    commentmodel.clear()
    currentqcfile = None
    currentstatesaved = True


def openQcFile(filename=None):
    global currentqcfile
    global currentstatesaved
    exitFullscreen()
    if not currentstatesaved and WarningMessageBox(
                            mainwindow,
                            _("Warning"),
                            _("Do you really want to open a new QC document without saving the old one?"),
                            question=True,
                            ).exec_() != 0:
        return
    if not filename:
        filename = QFileDialog.getOpenFileName(
                                    mainwindow,
                                    _("Open QC document"),
                                    "",
                                    _("QC documents (*.txt *.qcr);;All files (*.*)"),
                                    )[0]
    if not filename:
        return
    try:
        with open(filename, "r", encoding="utf-8") as qcfile:
            videofile = None
            comments = []
            datafound = False
            qclines = qcfile.readlines()
            for line in qclines:
                if datafound and line.startswith("["):
                    rawdata = line.strip().split("]")
                    if len(rawdata) < 3:
                        raise InvalidCommentLineError(line.strip("\n"))
                    timestampdata = rawdata[0].strip("[ ")
                    if not checkTimestamp(timestampdata):
                        raise InvalidTimestampError(timestampdata)
                    commenttypedata = rawdata[1].strip("[ ")
                    commentdata = "]".join(rawdata[2:]).strip()
                    comments.append((timestampdata, commenttypedata, commentdata))
                if line.startswith("[DATA]"):
                    datafound = True
                if line.startswith("path: "):
                    videofile = " ".join(line.strip().split(" ")[1:])
        if not datafound:
            WarningMessageBox(mainwindow, _("Warning"), _("Not a valid QC document!")).exec_()
        elif not comments:
            WarningMessageBox(mainwindow, _("Warning"), _("The QC document contains no comments!")).exec_()
        else:
            writeCommentListViewContents(comments)
            currentmodelindex = commentmodel.item(0, 2).index()
            commentlistview.setCurrentIndex(currentmodelindex)
            currentqcfile = filename
            currentstatesaved = True
            if videofile and QuestionMessageBox(
                                        mainwindow,
                                        _("Open Video?"),
                                        _("Do you want to open the associated video file?"),
                                        ).exec_() == 0:
                openVideoFile(filename=videofile)
    except UnicodeDecodeError:
        WarningMessageBox(mainwindow, _("Warning"), _("Not a valid QC document!")).exec_()
    except InvalidTimestampError as e:
        WarningMessageBox(
                mainwindow,
                _("Warning"),
                _("Invalid Timestamp found: {}\nThe only allowed "
                "format is: 'hh:mm:ss'\n'mm' and 'ss' have to be "
                "lower than 60.\n\nPlease correct the document "
                "before trying to open it again.").format(e),
                ).exec_()
    except InvalidCommentLineError as e:
        WarningMessageBox(
                mainwindow,
                _("Warning"),
                _("Invalid comment line found: {}\nThe only allowed "
                "format is: '[hh:mm:ss] [comment type] comment'\n\n"
                "Please correct the document before trying to "
                "open it again.").format(e),
                ).exec_()


def openVideoFile(filename=None):
    exitFullscreen()
    if not filename:
        filename = QFileDialog.getOpenFileName(
                            mainwindow,
                            _("Open video file"),
                            "",
                            _("Video files (*.mkv *.mp4);;All files (*.*)"),
                            )[0]
    if not filename:
        return
    if path.isfile(filename):
        mp.command("loadfile", filename, "replace")
        setPause(False)


def saveQcFile():
    if not currentqcfile:
        saveQcFileAs()
        return
    writeQcFile(currentqcfile)


def saveQcFileAs():
    exitFullscreen()
    currentvideofile = mp.get_property("path") if mpvslave else mp.path
    if currentvideofile and not currentqcfile:
        basename = path.basename(currentvideofile)
        basename = "[QC]_{}_{}".format(path.splitext(basename)[0], qcauthor)
        dirname = path.dirname(currentvideofile)
        filename = QFileDialog.getSaveFileName(
                                    mainwindow,
                                    _("Save QC document"),
                                    path.join(dirname, basename),
                                    _("QC documents (*.txt *.qcr)"),
                                    )[0]
    elif currentqcfile:
        filename = QFileDialog.getSaveFileName(
                                mainwindow,
                                _("Save QC document"),
                                currentqcfile,
                                _("QC documents (*.txt *.qcr)"),
                                )[0]
    else:
        basename = "[QC]_UNNAMED_{}".format(qcauthor)
        filename = QFileDialog.getSaveFileName(
                                mainwindow,
                                _("Save QC document"),
                                basename,
                                _("QC documents (*.txt *.qcr)"),
                                )[0]
    if not filename:
        return
    writeQcFile(filename)


def writeQcFile(filename=None, autosave=False):
    global currentstatesaved
    global currentqcfile
    comments = getCommentListViewContents()
    datetimetoday = str(datetime.datetime.today())
    datetoday = ".".join(datetimetoday.split(" ")[0].split("-")[::-1])
    timetoday = datetimetoday.split(" ")[1].split(".")[0]
    qcfilecontents = []
    qcfilecontents.extend([
                        "[FILE]\n",
                        "date: {} {}\n".format(datetoday, timetoday),
                        "generator: {}\n".format(v),
                        ])
    currentvideofile = mp.get_property("path") if mpvslave else mp.path
    if currentvideofile:
        qcfilecontents.append("path: {}\n".format(currentvideofile))
    qcfilecontents.extend([
                        "\n",
                        "[DATA]\n",
                        ])
    for x in comments:
        qcfilecontents.append("[{}] [{}] {}\n".format(x[0], x[1], x[2].strip()))
    qcfilecontents.append("# total lines: {}".format(len(comments)))
    if not autosave:
        with open(filename, "w", encoding="utf-8") as qcfile:
            qcfile.writelines(qcfilecontents)
        currentqcfile = filename
        currentstatesaved = True
    else:
        if not path.isdir(path.join(programlocation, "autosave")):
            mkdir(path.join(programlocation, "autosave"))
        zipname = "{}.zip".format("-".join(datetimetoday.split("-")[:2]))
        if path.isfile(path.join(programlocation, "autosave", zipname)):
            autosavezip = ZipFile(
                            path.join(programlocation, "autosave", zipname),
                            "a",
                            compression=ZIP_DEFLATED
                            )
        else:
            autosavezip = ZipFile(
                            path.join(programlocation, "autosave", zipname),
                            "w",
                            compression=ZIP_DEFLATED
                            )
        try:
            filename = "{}.{}".format(
                                datetimetoday.replace(":", "-").replace(" ", "_"),
                                path.basename(currentqcfile) if currentqcfile else "UNNAMED.txt"
                                )
            qcfilestring = "".join(qcfilecontents)
            # 'writestr' does not automatically use Windows line breaks on a Windows machine
            # So they have to be set explicitly
            if sys.platform.startswith("win32"):
                qcfilestring = qcfilestring.replace("\n", "\r\n")
            autosavezip.writestr(filename, qcfilestring)
        finally:
            autosavezip.close()


def cycleFullscreen():
    if not mainwindow.isFullScreen():
        commentlistview.scrollposition = commentlistview.verticalScrollBar().value()
        mainlayout.addWidget(mainwindow.mpvwindow)
        mainwindowsplitter.setVisible(False)
        mainwindow.menuBar().setVisible(False)
        mainwindow.showFullScreen()
        # Needed because if the video is paused, mpv won't repaint
        # the display until something else happens, like triggering
        # the osd via mouse movement
        # TODO: Find a better way to do this
        mp.command("mouse", 0, 0)
        showCursor()
    else:
        mainwindow.showNormal()
        mainwindowsplitter.insertWidget(0, mainwindow.mpvwindow)
        mainwindowsplitter.setVisible(True)
        mainwindow.menuBar().setVisible(True)
        commentlistview.verticalScrollBar().setValue(commentlistview.scrollposition)
        # Needed because if the video is paused, mpv won't repaint
        # the display until something else happens, like triggering
        # the osd via mouse movement
        # TODO: Find a better way to do this
        mp.command("mouse", 3, 3)
        showCursor()


def exitFullscreen():
    if mainwindow.isFullScreen():
        cycleFullscreen()


def setPause(value=True):
    if mpvslave:
        mp.set_property("pause", "yes" if value else "no")
    else:
        mp.pause = value


def showCursor():
    while app.overrideCursor():
        app.restoreOverrideCursor()
    mainwindow.mpvwindow.cursortimer.start(1000)


def hideCursor():
    if mainwindow.isFullScreen():
        app.setOverrideCursor(QCursor(Qt.BlankCursor))


def afterResize():
    resizeCommentListViewToContents()
    try:
        # Needed because if the video is paused, mpv won't repaint
        # the display until something else happens, like triggering
        # the osd via mouse movement
        # TODO: Find a better way to do this
        mp.command("mouse", 0, randint(0, 20))
    except NameError:
        # At the beginning the mpvwindow is resized
        # before mpv is started
        pass


def resizeVideo(width=None, height=None):
    if mainwindow.isFullScreen() or mainwindow.isMaximized():
        return
    try:
        size_x = width or int(mp.get_property("width") if mpvslave else mp.width)
        size_y = height or int(mp.get_property("height") if mpvslave else mp.height)
    except TypeError:
        return
    additionalheight = (
                        mainwindow.geometry().height()
                        -mainwindow.mpvwindow.geometry().height()
                        )
    mainwindow.resize(size_x, size_y+additionalheight)
    afterResize()


def autosave():
    if not commentListViewIsEmpty():
        try:
            writeQcFile(autosave=True)
        except PermissionError:
            # This error happens when the saves.zip is opened
            # with 7-Zip, but not with WinRAR
            pass
            # TODO: Maybe show a warning


def exceptHook(exceptiontype, exceptionvalue, tracebackobject):
    QMessageBox.critical(
            mainwindow,
            "Critical",
            "An error occurred!\n{}\n{}\n{}".format(
                                                exceptiontype,
                                                exceptionvalue,
                                                format_exception(
                                                            exceptiontype,
                                                            exceptionvalue,
                                                            tracebackobject
                                                            )
                                                )
            )


v = "mpvQC 0.3.0"

commenttypeoptions = None
qcauthor = "QC"
autosaveinterval = 2.5

currentqcfile = None
currentstatesaved = True

if getattr(sys, "frozen", False):
    programlocation = sys._MEIPASS
else:
    programlocation = path.dirname(path.realpath(__file__))

optionsfile = path.join(programlocation, "mpvQC.conf")

language = None

readOptionsFile()

systemlanguage = locale.getdefaultlocale()[0]

if language:
    if language == "de":
        gettext.translation("mpvQC", localedir="locale", languages=["de"]).install()
    else:
        _ = lambda s: s
elif systemlanguage.startswith("de"):
    gettext.translation("mpvQC", localedir="locale", languages=["de"]).install()
    language = "de"
else:
    _ = lambda s: s

commenttypeoptions = [
                _("Spelling"),
                _("Punctuation"),
                _("Translation"),
                _("Phrasing"),
                _("Timing"),
                _("Typeset"),
                _("Note"),
                ] if not commenttypeoptions else commenttypeoptions


sys.excepthook = exceptHook

app = QApplication(sys.argv)
locale.setlocale(locale.LC_NUMERIC, "C")

# Don't use the Fusion theme on Linux
# to let the user use his GTK+ theme instead
if not sys.platform.startswith("linux"):
    QApplication.setStyle(QStyleFactory.create("Fusion"))
    # Disable theme if a file called 'disable-dark-palette' is present
    if not path.isfile(path.join(programlocation, "disable-dark-palette")):
        darkpalette = QPalette()  # https://gist.github.com/QuantumCD/6245215
        darkpalette.setColor(QPalette.Window, QColor(53, 53, 53))
        darkpalette.setColor(QPalette.WindowText, Qt.white)
        darkpalette.setColor(QPalette.Base, QColor(25, 25, 25))
        darkpalette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        darkpalette.setColor(QPalette.ToolTipBase, Qt.white)
        darkpalette.setColor(QPalette.ToolTipText, Qt.white)
        darkpalette.setColor(QPalette.Text, Qt.white)
        darkpalette.setColor(QPalette.Light, Qt.transparent)  # text shadow color of the disabled options in context menu
        darkpalette.setColor(QPalette.Disabled, QPalette.Text, Qt.gray)
        darkpalette.setColor(QPalette.Button, QColor(53, 53, 53))
        darkpalette.setColor(QPalette.ButtonText, Qt.white)
        darkpalette.setColor(QPalette.BrightText, Qt.red)
        darkpalette.setColor(QPalette.Link, QColor(42, 130, 218))
        darkpalette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        darkpalette.setColor(QPalette.HighlightedText, Qt.black)
        app.setPalette(darkpalette)
        app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
    font = QFont()
    font.setFamily(font.defaultFamily())
    app.setFont(font)

mainwindow = MainWindow()

mainlayout = QVBoxLayout()
mainlayout.setContentsMargins(0, 0, 0, 0)

commentlistview = CommentListView()
commentmodel = QStandardItemModel(commentlistview)
commentmodel.itemChanged.connect(commentDataChanged)
commentmodel.rowsInserted.connect(commentDataChanged)
commentmodel.rowsRemoved.connect(commentDataChanged)
commentlistview.setModel(commentmodel)

mainwindowsplitter = QSplitter(mainwindow.centralWidget())
mainwindowsplitter.setOrientation(Qt.Vertical)
mainwindowsplitter.addWidget(mainwindow.mpvwindow)
mainwindowsplitter.addWidget(commentlistview)
mainwindowsplitter.setStretchFactor(0, 2)
mainwindowsplitter.setStretchFactor(1, 0)
mainwindowsplitter.splitterMoved.connect(afterResize)
mainlayout.addWidget(mainwindowsplitter)
mainwindow.centralWidget().setLayout(mainlayout)

mainwindow.show()


# Resize mainwindow and mpv to make the video take exactly 66.6%
# of the available space on the screen (= 720p on a 1080p screen)
size_x = int(QDesktopWidget().screenGeometry(mainwindow).width() * (2/3))
size_y = int(QDesktopWidget().screenGeometry(mainwindow).width()/16*9 * (2/3))
# I have no idea why it has to be called
# two times to work this time
resizeVideo(size_x, size_y)
resizeVideo(size_x, size_y)

# Move mainwidow to center
deskrect = QDesktopWidget().screenGeometry(
                                QDesktopWidget().screenNumber(QCursor.pos())
                                )
desk_x = deskrect.width()
desk_y = deskrect.height()
main_x = mainwindow.width()
main_y = mainwindow.height()
mainwindow.move(
            desk_x / 2 - main_x / 2 + deskrect.left(),
            desk_y / 2 - main_y / 2 + deskrect.top(),
            )
mainwindowgeo = mainwindow.geometry()
centralwidgetgeo = mainwindow.centralWidget().geometry()

mainwindoweventfilter = MainWindowEventFilter()
mainwindow.installEventFilter(mainwindoweventfilter)
mpvwindoweventfilter = MpvWindowEventFilter()
mainwindow.mpvwindow.installEventFilter(mpvwindoweventfilter)

# Create config files for mpv if they are not present
checkMpvConf()

if mpvslave:
    mp = MpvProcess([
            "--wid={}".format(int(mainwindow.mpvwindow.winId())),
            "--keep-open",
            "--osc=yes",
            "--cursor-autohide=no",
            "--input-cursor=no",
            "--input-default-bindings=no",
            "--config-dir={}".format(programlocation),
            ])
    mp.command = mp.commandv
else:
    mp = MPV(
            wid=str(int(mainwindow.mpvwindow.winId())),
            keep_open="yes",
            idle="yes",
            osc="yes",
            cursor_autohide="no",
            input_cursor="no",
            input_default_bindings="no",
            config="yes",
            config_dir=programlocation,
            )

autosavetimer = QTimer()
autosavetimer.timeout.connect(autosave)
if autosaveinterval > 0:
    autosavetimer.start(int(60000*autosaveinterval))


mainwindow.setWindowTitle(v)
app.setWindowIcon(QIcon(path.join(programlocation, "icon.ico")))
app.exec_()
