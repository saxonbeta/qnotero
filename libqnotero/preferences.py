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

import os
import os.path
import pkgutil
import platform
import sys
from libqnotero.qt.QtGui import QDialog, QFileDialog, QMessageBox,\
    QApplication, QStyleFactory
from libqnotero.config import getConfig, setConfig
from libqnotero.uiloader import UiLoader
from libzotero.libzotero import valid_location


class Preferences(QDialog, UiLoader):
    """Qnotero preferences dialog"""

    def __init__(self, qnotero, firstRun=False):

        """
		Constructor

		Arguments:
		qnotero -- a Qnotero instance

		Keyword arguments:
		firstRun -- indicates if the first run message should be shown
					(default=False)
		"""

        QDialog.__init__(self)
        self.qnotero = qnotero
        self.loadUi('preferences')
        self.ui.labelLocatePath.hide()
        if not firstRun:
            self.ui.labelFirstRun.hide()
        self.ui.labelTitleMsg.setText(
            self.ui.labelTitleMsg.text().replace(u"[version]",
                                                 self.qnotero.version))
        self.ui.pushButtonZoteroPathAutoDetect.clicked.connect(
            self.zoteroPathAutoDetect)
        self.ui.pushButtonZoteroPathBrowse.clicked.connect(
            self.zoteroPathBrowse)
        self.ui.checkBoxAutoUpdateCheck.setChecked(getConfig(u"autoUpdateCheck"))
        self.ui.checkBoxShowAbstract.setChecked(getConfig(u'showAbstract'))
        self.ui.lineEditZoteroPath.setText(getConfig(u"zoteroPath"))
        i = 0
        pos = getConfig(u'pos')
        while True:
            self.ui.comboBoxPos.setCurrentIndex(i)
            if self.ui.comboBoxPos.currentText() == pos:
                break
            i += 1
        i = 0
        import libqnotero._themes
        themePath = os.path.dirname(libqnotero._themes.__file__)
        if platform.system() == 'Darwin' and hasattr(sys, 'frozen'):
            themePath = os.path.join(os.path.dirname(sys.executable), u'themes')
            for dirname in next(os.walk(themePath))[1]:
                self.ui.comboBoxTheme.addItem(dirname)
                if dirname == getConfig(u"theme").lower():
                    self.ui.comboBoxTheme.setCurrentIndex(i)
                i += 1
        else:
            for _, theme, _ in pkgutil.iter_modules([themePath]):
                self.ui.comboBoxTheme.addItem(theme)
                if theme == getConfig(u"theme").lower():
                    self.ui.comboBoxTheme.setCurrentIndex(i)
                i += 1
        i = 0
        for style in QStyleFactory.keys():
            self.ui.comboBoxStyle.addItem(style)
            if style == getConfig(u'appStyle'):
                self.ui.comboBoxStyle.setCurrentIndex(i)
            i += 1
        self.adjustSize()

    def accept(self):

        """Accept the changes"""

        if self.ui.labelLocatePath.isVisible():
            return
        print('saving!')
        setConfig(u"firstRun", False)
        setConfig(u"pos", self.ui.comboBoxPos.currentText())
        setConfig(u"autoUpdateCheck",
                  self.ui.checkBoxAutoUpdateCheck.isChecked())
        setConfig(u'showAbstract',
                  self.ui.checkBoxShowAbstract.isChecked())
        setConfig(u"zoteroPath", self.ui.lineEditZoteroPath.text())
        setConfig(u"theme", self.ui.comboBoxTheme.currentText().capitalize())
        setConfig(u'appStyle', self.ui.comboBoxStyle.currentText())
        self.qnotero.saveState()
        self.qnotero.reInit()
        self.qnotero.zotero.update(True)
        self.qnotero.sysTray.re_init()
        QDialog.accept(self)

    def locate(self, path, target):

        """
		Tries to find the location of a target file

		Arguments:
		path -- the path to search
		target -- the target file

		Returns:
		The full path to the target file or None if it wasn't found
		"""

        self.ui.labelLocatePath.setText(u"Scanning: ...%s" % path[-32:])
        QApplication.processEvents()
        # Don't scan filesystems that may contain recursions
        if u".gvfs" in path or u".wine" in path:
            return None
        for (dirpath, dirnames, filenames) in os.walk(path):
            for filename in filenames:
                if filename == target:
                    return dirpath
            for dirname in dirnames:
                location = self.locate(os.path.join(dirpath, dirname), target)
                if location is not None:
                    return location
        return None

    def reject(self):

        """Reject changes"""

        if not self.ui.labelLocatePath.isVisible():
            QDialog.reject(self)

    def setZoteroPath(self, path):

        """
		Validate and set the Zotero path

		Arguments:
		path -- the Zotero path
		"""

        if valid_location(path):
            self.ui.lineEditZoteroPath.setText(path)
        else:
            QMessageBox.information(self, u"Invalid Zotero path",
                                    u"The folder you selected does not contain 'zotero.sqlite'")

    def zoteroPathAutoDetect(self):

        """Auto-detect the Zotero folder"""

        self.ui.labelLocatePath.show()
        if platform.system() == u"Windows":
            home = os.environ[u"USERPROFILE"]
        elif platform.system() == u"Linux" or platform.system() == u'Darwin':
            home = os.environ[u"HOME"]
        zoteroPath = self.locate(os.path.join(home, u'Zotero'), u"zotero.sqlite")
        if zoteroPath is None:
            zoteroPath = self.locate(home, u"zotero.sqlite")
        if zoteroPath is None:
            QMessageBox.information(self, u"Unable to find Zotero",
                                    u"Unable to find Zotero. Please specify the Zotero folder manually.")
        else:
            self.ui.lineEditZoteroPath.setText(zoteroPath)
        self.ui.labelLocatePath.hide()

    def zoteroPathBrowse(self):

        """Select the Zotero folder manually"""

        path = QFileDialog.getExistingDirectory(self, u"Locate Zotero folder")
        if path != u"":
            self.setZoteroPath(path)
