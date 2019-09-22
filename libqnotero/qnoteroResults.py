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

from libqnotero.qt.QtGui import QListWidget
from libqnotero.qt.QtCore import Qt
import subprocess
import os
import platform


class QnoteroResults(QListWidget):
    """The Qnotero result list"""

    def __init__(self, qnotero):

        """
		Constructor

		Arguments:
		qnotero -- a Qnotero instance
		"""

        QListWidget.__init__(self, qnotero)
        self.itemDoubleClicked.connect(self.DoubleClicked)
        self.itemClicked.connect(self.Clicked)
        self.setMouseTracking(True)

    @staticmethod
    def DoubleClicked(item):

        """
		Open file attachment or URL

		Arguments:
		item -- a qnoteroItem
		"""

        if item is None or not hasattr(item, "zoteroItem"):
            return
        zoteroItem = item.zoteroItem
        if zoteroItem.fulltext is None and zoteroItem.url is None:
            print('qnoteroResults.mousePressEvent(): no file attachment nor url')
            return
        if zoteroItem.fulltext is None:
            path = zoteroItem.url
        else:
            path = zoteroItem.fulltext

        print("qnoteroResults.mousePressEvent(): prepare to open %s"
              % path)
        try:
            if platform.system() == 'Darwin':  # macOS
                subprocess.call(('open', path))
            elif platform.system() == 'Windows':  # Windows
                path = os.path.normpath(path)
                os.startfile(path)
            else:  # linux variants
                subprocess.call(('xdg-open', path))
            print("qnoteroResults.mousePressEvent(): file opened")
        except Exception as exc:
            print("qnoteroResults.mousePressEvent(): failed to open file or URL, sorry... %s" % exc)

    def keyPressEvent(self, e):

        """
		Handle key presses

		Arguments:
		e -- a QKeyEvent
		"""

        if (e.key() == Qt.Key_Up and self.currentRow() == 0) \
                or (e.key() == Qt.Key_F and Qt.ControlModifier & e.modifiers()):
            self.qnotero.ui.lineEditQuery.selectAll()
            self.qnotero.ui.lineEditQuery.setFocus()
            return
        QListWidget.keyPressEvent(self, e)

    def Clicked(self, item):
        if item is None or not hasattr(item, "zoteroItem"):
            return
        zoteroItem = item.zoteroItem
        self.qnotero.ui.textAbstract.setText(zoteroItem.abstract)
