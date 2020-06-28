# -*- coding:utf-8 -*-

#  This file is part of Qnotero.
#
#      Qnotero is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      Qnotero is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with Qnotero.  If not, see <https://www.gnu.org/licenses/>.
#      Copyright (c) 2019 E. Albiter

#

import sys
import os
from libqnotero.qt import QtGui, QtCore
from libqnotero.qt.QtGui import QMainWindow, QDesktopWidget, QMessageBox, QMenu
from libqnotero.qt.QtCore import QSettings, QCoreApplication, QObject, QEvent
from libqnotero.sysTray import SysTray
from libqnotero.config import saveConfig, restoreConfig, getConfig
from libqnotero.qnoteroItemDelegate import QnoteroItemDelegate
from libqnotero.qnoteroItem import QnoteroItem
from libqnotero.uiloader import UiLoader
from libzotero.libzotero import LibZotero


class Qnotero(QMainWindow, UiLoader):
    """The main class of the Qnotero GUI"""

    version = '2.3.0'

    def __init__(self, app=None, systray=True, debug=False, reset=False, parent=None):

        """
		Constructor.

		Keyword arguments:
		systray		--	Enables the system tray icon (default=True)
		debug		--	Enable debugging output (default=False)
		reset		--	Reset preferences (default=False)
		parent		--	Parent QWidget (default=None)
		"""

        QMainWindow.__init__(self, parent)
        self.app = app
        self.loadUi('qnotero')
        if not reset:
            self.restoreState()
        self.debug = debug
        self.reInit()
        self.noResults()
        if systray:
            self.sysTray = SysTray(self)
            self.sysTray.show()
            self.minimizeOnClose = True
        else:
            self.minimizeOnClose = False
        if getConfig(u"firstRun") or not os.path.exists(getConfig('zoteroPath')):
            self.preferences(firstRun=True)
        if getConfig(u"autoUpdateCheck"):
            self.updateCheck()

    def close(self):

        """Exits the program."""

        self.minimizeOnClose = False
        QMainWindow.close(self)

    def closeEvent(self, e):

        """
		Close or minimze to tray, depending on when the function is called

		Arguments:
		e -- a QCloseEvent
		"""

        if self.minimizeOnClose and not e.spontaneous():
            self.popDown()
            e.ignore()
            print(u'qnotero.closeEvent(): Hiding to system tray')
        else:
            e.accept()
            if self.listener is not None:
                self.listener.alive = False
            print(u'qnotero.closeEvent(): Exiting Qnotero, bye...')
            sys.exit()

    def hideNoteHint(self):

        """Hide the note available message"""

        self.ui.labelNoteAvailable.hide()

    def openNote(self):

        """Open the active note"""

        self.activeNote.open()

    def noResults(self, query=None):

        """
		Displays the no results message

		Keyword arguments:
		query -- a query (default=None)
		"""

        if query is not None:
            self.showResultMsg(u"No results for %s" % query)
        else:
            self.showResultMsg(u"Please enter a search term")
        self.ui.textAbstract.setText(None)

    def popDown(self):

        """Minimize to the tray"""

        if self.minimizeOnClose:
            self.hide()
        else:
            self.close()

    def popUp(self):

        """Popup from the tray"""

        # Reposition the window
        # TODO: Add code to identify the screen to show the main window
        r = QDesktopWidget().availableGeometry()
        s = self.size()
        pos = getConfig(u"pos")
        if pos == u"Top right":
            x = r.left() + r.width() - s.width() - 10
            y = r.top()
        elif pos == u"Top left":
            x = r.left() + 10
            y = r.top()
        elif pos == u"Bottom right":
            x = r.left() + r.width() - s.width() - 10
            y = r.top() + r.height() - s.height()
        elif pos == u"Bottom left":
            x = r.left() + 10
            y = r.top() + r.height() - s.height()
        else:
            x = r.left() + r.width() / 2 - s.width() / 2
            y = r.top() + r.height() / 2 - s.height() / 2
        self.move(x, y)

        # Show it
        self.show()
        QCoreApplication.processEvents()
        self.raise_()
        self.activateWindow()

        # Focus the search box
        self.ui.lineEditQuery.selectAll()
        self.ui.lineEditQuery.setFocus()

    def preferences(self, firstRun=False):

        """
		Show the preferences dialog

		Keyword arguments:
		firstRun -- indicates if the first run message should be shown
					(default=False)
		"""

        from libqnotero.preferences import Preferences
        Preferences(self, firstRun=firstRun).exec_()

    def previewNote(self, note):

        """
		Show the note preview

		Arguments:
		note -- the Note to preview
		"""

        self.activeNote = note
        self.ui.labelNote.setText(note.preview)
        self.hideNoteHint()
        self.ui.widgetNote.show()
        self.ui.listWidgetResults.hide()

    def reInit(self):

        """Re-inits the parts of the GUI that can be changed at runtime."""

        self.setTheme()
        self.setupUi()
        self.noteProvider = []
        self.noResults()
        self.ui.listWidgetResults.clear()
        self.ui.textAbstract.setText(u'')
        self.ui.lineEditQuery.clear()
        self.ui.listWidgetResults.installEventFilter(self)
        if getConfig(u'noteProvider') == u'gnote':
            from libzotero._noteProvider.gnoteProvider import GnoteProvider
            print(u"qnotero.reInit(): using GnoteProvider")
            self.noteProvider = GnoteProvider(self)
        self.zotero = LibZotero(getConfig(u"zoteroPath"), self.noteProvider)
        if hasattr(self, u"sysTray"):
            self.sysTray.setIcon(self.theme.icon("qnotero", ".png"))

    def restoreState(self):

        """Restore the settings"""

        settings = QSettings(u"Qnotero", u"qnotero")
        settings.beginGroup(u"Qnotero")
        restoreConfig(settings)
        settings.endGroup()

    def saveState(self):

        """Save the settings"""

        settings = QSettings(u"Qnotero", u"qnotero")
        settings.beginGroup(u"Qnotero")
        saveConfig(settings)
        settings.endGroup()

    def search(self, setFocus=False):

        """
		Execute a search

		Keyword arguments:
		setFocus -- indicates whether the listWidgetResults needs to receive
					focus (default=False)
		"""

        self.ui.labelNoteAvailable.hide()
        self.ui.listWidgetResults.show()
        self.ui.listWidgetResults.clear()
        self.ui.lineEditQuery.needUpdate = False
        self.ui.lineEditQuery.timer.stop()
        query = self.ui.lineEditQuery.text()
        if len(query) < getConfig(u"minQueryLength"):
            self.noResults()
            return
        zoteroItemList = self.zotero.search(query)
        if len(zoteroItemList) == 0:
            self.noResults(query)
            return
        self.showResultMsg(u"%d results for %s" % (len(zoteroItemList), query))
        for zoteroItem in zoteroItemList:
            qnoteroItem = QnoteroItem(self, zoteroItem,
                                      self.ui.listWidgetResults)
            self.ui.listWidgetResults.addItem(qnoteroItem)
        if setFocus:
            self.ui.listWidgetResults.setFocus()

    def setSize(self, size):

        """
		Set the window size

		Arguments:
		size -- a QSize
		"""

        self.setMinimumSize(size)
        self.setMaximumSize(size)

    def setTheme(self):

        """Load a theme"""

        theme = getConfig(u'theme')
        self.app.setStyle(getConfig(u'appStyle'))
        mod = __import__(u'libqnotero._themes.%s' % theme.lower(), fromlist=[u'dummy'])
        cls = getattr(mod, theme.capitalize())
        self.theme = cls(self)

    def setupUi(self):

        """Setup the GUI"""

        self.ui.pushButtonSearch.setIcon(self.theme.icon(u"search"))
        self.ui.pushButtonSearch.clicked.connect(self.search)
        self.ui.lineEditQuery.qnotero = self
        self.ui.listWidgetResults.qnotero = self
        self.ui.listWidgetResults.setItemDelegate(QnoteroItemDelegate(self))
        self.ui.pushButtonOpenNote.hide()
        self.ui.pushButtonReturnFromNote.hide()
        self.ui.labelNoteAvailable.hide()
        self.ui.labelNote.hide()
        self.ui.pushButtonOpenNote.clicked.connect(self.openNote)
        if getConfig(u'showAbstract'):
            self.ui.textAbstract.show()
            self.ui.labelAbstract.show()
            self.ui.textAbstract.setFixedHeight(200)
        else:
            self.ui.textAbstract.hide()
            self.ui.labelAbstract.hide()

    def showNoteHint(self):

        """Indicate that a note is available"""

        self.ui.labelNoteAvailable.show()

    def showResultMsg(self, msg):

        """
		Shows a status message.

		Arguments:
		msg 	--	A message.
		"""

        self.ui.labelResultMsg.setText(u"<small><i>%s</i></small>" % msg)

    def eventFilter(self, source: 'QObject', e: 'QEvent') -> bool:
        if (e.type() == QtCore.QEvent.ContextMenu and source is
                self.ui.listWidgetResults):
            contextMenu = QMenu(self)
            actCopyAuthordate = contextMenu.addAction(u"Copy author(s) and year")
            actCopyDOI = contextMenu.addAction(u"Copy DOI")
            actCopyTitle = contextMenu.addAction(u"Copy title")
            actCopyAbs = contextMenu.addAction(u"Copy abstract")
            actCopyRef = contextMenu.addAction(u"Copy Reference")
            action = contextMenu.exec_(self.mapToGlobal(e.pos()))
            item = source.itemAt(e.pos())
            if (action is None) or (item is None):
                return True
            clipboard = QtGui.QApplication.clipboard()
            clipboard.clear(mode=clipboard.Clipboard)
            if action is actCopyAuthordate:
                clipboard.setText(item.zoteroItem.author_date_format(), mode=clipboard.Clipboard)
                return True
            elif action is actCopyDOI:
                if item.zoteroItem.doi is not None:
                    clipboard.setText(item.zoteroItem.doi, mode=clipboard.Clipboard)
                return True
            elif action is actCopyTitle:
                title = item.zoteroItem.format_title()
                if title is not None:
                    clipboard.setText(title, mode=clipboard.Clipboard)
                return True
            elif action is actCopyAbs:
                if item.zoteroItem.abstract is not None:
                    clipboard.setText(item.zoteroItem.abstract, mode=clipboard.Clipboard)
                return True
            elif action is actCopyRef:
                clipboard.setText(item.zoteroItem.full_format(), mode=clipboard.Clipboard)
                return True
        return QMainWindow.eventFilter(self, source, e)

    def updateCheck(self):

        """Checks for updates if update checking is on."""

        if not getConfig(u"autoUpdateCheck"):
            return True
        import urllib.request
        from distutils.version import LooseVersion
        print(u"qnotero.updateCheck(): opening %s" % getConfig(u"updateUrl"))
        try:
            fd = urllib.request.urlopen(getConfig(u"updateUrl"))
            mrv = fd.read().decode('utf-8').strip()
        except:
            print('qnotero.updateCheck(): failed to check for update')
            return
        print("qnotero.updateCheck(): most recent = %s, current = %s" \
              % (mrv, self.version))
        if LooseVersion(mrv) > LooseVersion(self.version):
            QMessageBox.information(self, 'Update found',
                                    ('A new version of Qnotero is available! Please visit '
                                     'http://www.cogsci.nl/qnotero for more information.'))
